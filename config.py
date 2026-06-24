"""
app.py -- Aplicacion web Flask del Verificador Vehicular Peru.

Rutas individuales:
  GET  /                        -> Pagina principal
  POST /consultar               -> Inicia consulta individual
  GET  /verificando/<sid>       -> Progreso en tiempo real (SSE)
  GET  /api/stream/<sid>        -> SSE individual
  POST /api/recomendaciones     -> Veredicto y recomendaciones
  GET  /reporte/<sid>           -> Descarga reporte HTML

Rutas masivas:
  POST /masivo/cargar           -> Sube archivo y devuelve placas detectadas
  POST /masivo/iniciar          -> Inicia procesamiento en lote
  GET  /masivo/<bid>            -> Dashboard de progreso masivo
  GET  /api/masivo/stream/<bid> -> SSE masivo
"""

import os
import sys
import re
import json
import asyncio
import threading
import uuid
import time
import queue
from pathlib import Path
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, Response, jsonify, send_file, abort
)

# Asegurar que el directorio raiz este en el path
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from config import HEADLESS, TIMEOUT
from playwright.async_api import async_playwright

# Scrapers - Bloque 1
from scrapers import sunarp_vehicular, soat_apeseg, mtc_inspeccion
from scrapers import sunarp_sprl, sunarp_siguelo

# Scrapers - Bloque 2
from scrapers import sutran, atu, sbs_accidentes, callao, gnv_fise

# Scrapers - Bloque 3
from scrapers import (
    trujillo, piura, chiclayo, tarapoto,
    cajamarca, chachapoyas, huancayo,
    ica, tacna, arequipa
)

from reporter.generator import generar_reporte
from inspeccion.recomendaciones import generar as generar_recomendaciones
from inspeccion.checklist import CHECKLIST, CATEGORIAS, NOMBRES_CATEGORIA
from utils.extractor_placas import extraer_placas


# ── Flask app ──────────────────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "web" / "templates"),
    static_folder=str(BASE_DIR / "web" / "static"),
)
app.secret_key = os.getenv("SECRET_KEY", "vehicular-peru-2024")

# ── Almacen de sesiones individuales ─────────────────────────────────────────
sesiones = {}

# ── Almacen de lotes masivos ──────────────────────────────────────────────────
lotes = {}


# ── Helpers ───────────────────────────────────────────────────────────────────

def extraer_datos_sprl(r_sprl):
    titulo_anio = titulo_numero = sede = ""
    if r_sprl.estado in ("ok", "advertencia") and r_sprl.datos:
        titulo_raw = r_sprl.datos.get("Titulo", r_sprl.datos.get("Titulo", ""))
        if titulo_raw:
            partes = re.split(r"[\s\-]+", titulo_raw.strip())
            if len(partes) >= 2:
                titulo_anio   = partes[0].strip()
                titulo_numero = partes[-1].strip()
        sede = r_sprl.datos.get("Sede", r_sprl.datos.get("sede", "LIMA"))
    return titulo_anio, titulo_numero, sede


def resultado_a_dict(r):
    return {
        "fuente" : r.fuente,
        "url"    : r.url,
        "estado" : r.estado,
        "datos"  : r.datos,
        "mensaje": r.mensaje,
    }


# ── Definicion de pasos de scraping ───────────────────────────────────────────
PASOS = [
    (1, "SUNARP Vehicular",           "sunarp_vehicular"),
    (1, "SOAT APESEG",                "soat_apeseg"),
    (1, "MTC Inspeccion Tecnica",     "mtc_inspeccion"),
    (1, "SUNARP SPRL (propietarios)", "sunarp_sprl"),
    (1, "SUNARP SigueloPlus",         "sunarp_siguelo"),
    (2, "SUTRAN Infracciones",        "sutran"),
    (2, "ATU Multas",                 "atu"),
    (2, "SBS Accidentes SOAT",        "sbs_accidentes"),
    (2, "Callao Papeletas",           "callao"),
    (2, "GNV FISE Deuda",             "gnv_fise"),
    (3, "Trujillo",                   "trujillo"),
    (3, "Piura",                      "piura"),
    (3, "Chiclayo",                   "chiclayo"),
    (3, "Tarapoto",                   "tarapoto"),
    (3, "Cajamarca",                  "cajamarca"),
    (3, "Chachapoyas",                "chachapoyas"),
    (3, "Huancayo",                   "huancayo"),
    (3, "Ica",                        "ica"),
    (3, "Tacna",                      "tacna"),
    (3, "Arequipa",                   "arequipa"),
]

TOTAL_PASOS = len(PASOS)

MODULOS = {
    "sunarp_vehicular": sunarp_vehicular,
    "soat_apeseg"     : soat_apeseg,
    "mtc_inspeccion"  : mtc_inspeccion,
    "sunarp_sprl"     : None,  # logica especial
    "sunarp_siguelo"  : None,  # logica especial
    "sutran"          : sutran,
    "atu"             : atu,
    "sbs_accidentes"  : sbs_accidentes,
    "callao"          : callao,
    "gnv_fise"        : gnv_fise,
    "trujillo"        : trujillo,
    "piura"           : piura,
    "chiclayo"        : chiclayo,
    "tarapoto"        : tarapoto,
    "cajamarca"       : cajamarca,
    "chachapoyas"     : chachapoyas,
    "huancayo"        : huancayo,
    "ica"             : ica,
    "tacna"           : tacna,
    "arequipa"        : arequipa,
}


# ── Motor de scraping (async) ─────────────────────────────────────────────────

async def _scraping_async(sid, placa, cola):
    """Corrutina: ejecuta los 20 scrapers y envia eventos via cola."""

    def enviar(tipo, datos_extra=None):
        ev = {"tipo": tipo}
        if datos_extra:
            ev.update(datos_extra)
        cola.put(json.dumps(ev, ensure_ascii=False))

    sesion = sesiones[sid]

    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(
                headless=HEADLESS,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--start-maximized"]
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            )

            paso_actual    = 0
            sede_vehiculo  = ""
            r_sprl_global  = None

            for bloque, nombre, clave in PASOS:
                paso_actual += 1
                pct = int((paso_actual - 1) / TOTAL_PASOS * 100)
                enviar("progreso", {
                    "paso"  : paso_actual,
                    "total" : TOTAL_PASOS,
                    "pct"   : pct,
                    "nombre": nombre,
                    "bloque": bloque,
                })

                page = await context.new_page()
                try:
                    if clave == "sunarp_vehicular":
                        r = await sunarp_vehicular.consultar(page, placa)
                        if r.estado in ("ok", "advertencia"):
                            sede_vehiculo = r.datos.get("Sede", "")

                    elif clave == "sunarp_sprl":
                        r = await sunarp_sprl.consultar(page, placa, sede=sede_vehiculo)
                        r_sprl_global = r

                    elif clave == "sunarp_siguelo":
                        ta, tn, sed = extraer_datos_sprl(r_sprl_global) if r_sprl_global else ("", "", "")
                        r = await sunarp_siguelo.consultar(
                            page,
                            titulo_numero=tn,
                            titulo_anio=ta,
                            oficina_registral=sed or "LIMA"
                        )
                    else:
                        r = await MODULOS[clave].consultar(page, placa)

                except Exception as ex:
                    from scrapers.base import ResultadoConsulta
                    r = ResultadoConsulta(fuente=nombre, url="")
                    r.marcar_error("Error inesperado: {}".format(str(ex)[:200]))

                finally:
                    try:
                        await page.close()
                    except Exception:
                        pass

                if bloque == 1:
                    sesion["resultados_doc"].append(r)
                elif bloque == 2:
                    sesion["resultados_deudas"].append(r)
                else:
                    sesion["resultados_regiones"].append(r)

                enviar("resultado", {
                    "bloque"   : bloque,
                    "resultado": resultado_a_dict(r),
                    "pct"      : int(paso_actual / TOTAL_PASOS * 100),
                })

            await browser.close()

        todos = (
            sesion["resultados_doc"]
            + sesion["resultados_deudas"]
            + sesion["resultados_regiones"]
        )
        ruta = generar_reporte(
            placa=placa,
            resultados_doc=sesion["resultados_doc"],
            resultados_deudas=sesion["resultados_deudas"],
            resultados_regiones=sesion["resultados_regiones"],
        )
        sesion["ruta_reporte"] = ruta
        sesion["estado"] = "done"

        ok     = sum(1 for r in todos if r.estado == "ok")
        warn   = sum(1 for r in todos if r.estado == "advertencia")
        errors = sum(1 for r in todos if r.estado == "error")

        enviar("listo", {"pct": 100, "ok": ok, "warn": warn, "errors": errors, "total": len(todos)})

    except Exception as ex:
        sesion["estado"] = "error"
        enviar("error_fatal", {"mensaje": str(ex)[:400]})

    finally:
        cola.put(None)


def _thread_scraping(sid, placa, cola):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_scraping_async(sid, placa, cola))
    finally:
        loop.close()


# ── Rutas individuales ────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/consultar", methods=["POST"])
def consultar():
    placa = request.form.get("placa", "").strip().upper()
    placa = re.sub(r"[^A-Z0-9]", "", placa)
    if not placa or len(placa) < 5:
        return render_template("index.html", error="Placa invalida. Ejemplos: B1N553, ABC123")

    sid  = str(uuid.uuid4())
    cola = queue.Queue()

    sesiones[sid] = {
        "placa"              : placa,
        "estado"             : "running",
        "cola"               : cola,
        "resultados_doc"     : [],
        "resultados_deudas"  : [],
        "resultados_regiones": [],
        "ruta_reporte"       : None,
        "ts"                 : time.time(),
    }

    threading.Thread(target=_thread_scraping, args=(sid, placa, cola), daemon=True).start()
    return redirect(url_for("verificando", sid=sid))


@app.route("/verificando/<sid>")
def verificando(sid):
    if sid not in sesiones:
        return redirect(url_for("index"))
    placa = sesiones[sid]["placa"]
    return render_template("verificando.html", sid=sid, placa=placa,
                           checklist=CHECKLIST, categorias=CATEGORIAS,
                           nombres_cat=NOMBRES_CATEGORIA, total_pasos=TOTAL_PASOS)


@app.route("/api/stream/<sid>")
def api_stream(sid):
    if sid not in sesiones:
        abort(404)
    cola = sesiones[sid]["cola"]

    def generar():
        while True:
            try:
                msg = cola.get(timeout=90)
                if msg is None:
                    yield "data: {}\n\n".format(json.dumps({"tipo": "fin"}))
                    break
                yield "data: {}\n\n".format(msg)
            except queue.Empty:
                yield "data: {}\n\n".format(json.dumps({"tipo": "ping"}))

    return Response(generar(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/api/recomendaciones", methods=["POST"])
def api_recomendaciones():
    data = request.get_json(force=True)
    sid  = data.get("sid", "")
    if sid not in sesiones:
        return jsonify({"error": "Sesion no encontrada"}), 404
    sesion = sesiones[sid]
    todos  = sesion["resultados_doc"] + sesion["resultados_deudas"] + sesion["resultados_regiones"]
    return jsonify(generar_recomendaciones(todos, data.get("respuestas") or None))


@app.route("/reporte/<sid>")
def descargar_reporte(sid):
    if sid not in sesiones:
        abort(404)
    ruta = sesiones[sid].get("ruta_reporte")
    if not ruta or not os.path.exists(ruta):
        abort(404)
    return send_file(ruta, as_attachment=False, mimetype="text/html")


# ── Rutas masivas ─────────────────────────────────────────────────────────────

@app.route("/masivo/cargar", methods=["POST"])
def masivo_cargar():
    if "archivo" not in request.files:
        return jsonify({"error": "No se recibio ningun archivo."}), 400
    archivo = request.files["archivo"]
    if not archivo.filename:
        return jsonify({"error": "Nombre de archivo vacio."}), 400
    contenido = archivo.read()
    try:
        placas = extraer_placas(archivo.filename, contenido)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if not placas:
        return jsonify({
            "error": "No se detectaron placas. "
                     "Asegurate de que el archivo contenga placas en formato ABC123 o ABC-123."
        }), 400
    return jsonify({"placas": placas, "total": len(placas)})


async def _scraping_una_placa(placa, bid, cola_lote):
    """Ejecuta scraping completo para una placa dentro del lote."""
    sid       = str(uuid.uuid4())
    cola_ind  = queue.Queue()
    sesiones[sid] = {
        "placa": placa, "estado": "running", "cola": cola_ind,
        "resultados_doc": [], "resultados_deudas": [], "resultados_regiones": [],
        "ruta_reporte": None, "ts": time.time(),
    }
    await _scraping_async(sid, placa, cola_ind)

    todos = (
        sesiones[sid]["resultados_doc"]
        + sesiones[sid]["resultados_deudas"]
        + sesiones[sid]["resultados_regiones"]
    )
    resumen = {
        "sid"         : sid,
        "placa"       : placa,
        "ok"          : sum(1 for r in todos if r.estado == "ok"),
        "advertencia" : sum(1 for r in todos if r.estado == "advertencia"),
        "error"       : sum(1 for r in todos if r.estado == "error"),
        "sin_datos"   : sum(1 for r in todos if r.estado == "sin_datos"),
        "ruta_reporte": sesiones[sid].get("ruta_reporte", ""),
    }
    lotes[bid]["resultados"].append(resumen)
    cola_lote.put(json.dumps({"tipo": "placa_lista", "resumen": resumen}, ensure_ascii=False))


async def _lote_async(bid, placas, cola_lote):
    total = len(placas)
    for idx, placa in enumerate(placas):
        cola_lote.put(json.dumps({
            "tipo" : "iniciando",
            "placa": placa,
            "num"  : idx + 1,
            "total": total,
            "pct"  : int(idx / total * 100),
        }, ensure_ascii=False))
        try:
            await _scraping_una_placa(placa, bid, cola_lote)
        except Exception as ex:
            lotes[bid]["resultados"].append({
                "sid": "", "placa": placa,
                "ok": 0, "advertencia": 0, "error": 1, "sin_datos": 0,
                "ruta_reporte": "", "error_msg": str(ex)[:200],
            })
            cola_lote.put(json.dumps({
                "tipo"   : "placa_lista",
                "resumen": {"placa": placa, "error_msg": str(ex)[:200],
                            "ok": 0, "advertencia": 0, "error": 1, "sin_datos": 0, "sid": ""},
            }, ensure_ascii=False))

    lotes[bid]["estado"] = "done"
    cola_lote.put(json.dumps({"tipo": "lote_listo", "total": total, "pct": 100}, ensure_ascii=False))
    cola_lote.put(None)


def _thread_lote(bid, placas, cola_lote):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_lote_async(bid, placas, cola_lote))
    finally:
        loop.close()


@app.route("/masivo/iniciar", methods=["POST"])
def masivo_iniciar():
    data   = request.get_json(force=True)
    placas = data.get("placas", [])
    placas = [re.sub(r"[^A-Z0-9]", "", p.upper()) for p in placas if p.strip()]
    placas = list(dict.fromkeys(placas))
    if not placas:
        return jsonify({"error": "No hay placas validas para procesar."}), 400
    if len(placas) > 100:
        return jsonify({"error": "Maximo 100 placas por lote."}), 400

    bid       = str(uuid.uuid4())
    cola_lote = queue.Queue()
    lotes[bid] = {
        "placas": placas, "estado": "running",
        "cola": cola_lote, "resultados": [], "ts": time.time(),
    }
    threading.Thread(target=_thread_lote, args=(bid, placas, cola_lote), daemon=True).start()
    return jsonify({"bid": bid, "total": len(placas)})


@app.route("/masivo/<bid>")
def masivo_dashboard(bid):
    if bid not in lotes:
        return redirect(url_for("index"))
    lote = lotes[bid]
    return render_template("masivo.html", bid=bid, placas=lote["placas"], total=len(lote["placas"]))


@app.route("/api/masivo/stream/<bid>")
def api_masivo_stream(bid):
    if bid not in lotes:
        abort(404)
    cola = lotes[bid]["cola"]

    def generar():
        while True:
            try:
                msg = cola.get(timeout=600)
                if msg is None:
                    yield "data: {}\n\n".format(json.dumps({"tipo": "fin"}))
                    break
                yield "data: {}\n\n".format(msg)
            except queue.Empty:
                yield "data: {}\n\n".format(json.dumps({"tipo": "ping"}))

    return Response(generar(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    print("\n  Verificador Vehicular Peru -- http://localhost:{}\n".format(port))
    app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)
