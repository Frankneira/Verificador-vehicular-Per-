"""
main.py -- Orquestador principal del Verificador Vehicular (Fase 1 + Fase 2).

Uso:
    python main.py B1N553
    python main.py          (pedira la placa por teclado)

Bloques:
    Bloque 1 - Documentacion : SUNARP, SOAT, ITV, SPRL, SigueloPlus
    Bloque 2 - Deudas        : SUTRAN, ATU, SBS, Callao, GNV
    Bloque 3 - Regionales    : Trujillo, Piura, Chiclayo, Tarapoto,
                               Cajamarca, Chachapoyas, Huancayo,
                               Ica, Tacna, Arequipa
"""
import asyncio
import sys
import os
import re
import webbrowser

from playwright.async_api import async_playwright

# Fase 1
from scrapers import sunarp_vehicular, soat_apeseg, mtc_inspeccion
from scrapers import sutran, atu, sbs_accidentes

# Fase 2 - SUNARP avanzado
from scrapers import sunarp_sprl, sunarp_siguelo

# Fase 2 - Deudas adicionales
from scrapers import callao, gnv_fise

# Fase 2 - Papeletas regionales
from scrapers import (
    trujillo, piura, chiclayo, tarapoto,
    cajamarca, chachapoyas, huancayo,
    ica, tacna, arequipa
)

from reporter.generator import generar_reporte
from config import HEADLESS, TIMEOUT


class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    BLUE   = "\033[94m"
    GRAY   = "\033[90m"
    CYAN   = "\033[96m"


def imprimir_estado(nombre, estado):
    iconos = {
        "ok"         : C.GREEN  + "OK          " + C.RESET,
        "advertencia": C.YELLOW + "ADVERTENCIA " + C.RESET,
        "error"      : C.RED    + "ERROR       " + C.RESET,
        "sin_datos"  : C.GRAY   + "SIN DATOS   " + C.RESET,
    }
    print("  [{}]  {}".format(iconos.get(estado, "?"), nombre))


def extraer_datos_sprl(r_sprl):
    """Extrae (anio, numero, sede) del resultado de SUNARP SPRL."""
    titulo_anio = titulo_numero = sede = ""
    if r_sprl.estado in ("ok", "advertencia") and r_sprl.datos:
        titulo_raw = r_sprl.datos.get("Titulo", r_sprl.datos.get("Título", ""))
        if titulo_raw:
            partes = re.split(r"[\s\-]+", titulo_raw.strip())
            if len(partes) >= 2:
                titulo_anio   = partes[0].strip()
                titulo_numero = partes[-1].strip()
        sede = r_sprl.datos.get("Sede", r_sprl.datos.get("sede", "LIMA"))
    return titulo_anio, titulo_numero, sede


async def ejecutar_consultas(placa):
    print("\n" + "=" * 60)
    print("  VERIFICADOR VEHICULAR -- Placa: {}".format(placa.upper()))
    print("=" * 60 + "\n")

    resultados_doc = []
    resultados_deudas = []
    resultados_regiones = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=HEADLESS,
            args=["--start-maximized"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )

        # --- BLOQUE 1: Documentacion ---
        print(C.BOLD + "BLOQUE 1 -- Documentacion del vehiculo" + C.RESET)
        print("-" * 50)

        page = await context.new_page()
        print("  Consultando SUNARP vehicular...")
        r = await sunarp_vehicular.consultar(page, placa)
        await page.close()
        imprimir_estado(r.fuente, r.estado)
        resultados_doc.append(r)
        sede_vehiculo = r.datos.get("Sede", "") if r.estado in ("ok", "advertencia") else ""

        page = await context.new_page()
        print("  Consultando SOAT APESEG...")
        r = await soat_apeseg.consultar(page, placa)
        await page.close()
        imprimir_estado(r.fuente, r.estado)
        resultados_doc.append(r)

        page = await context.new_page()
        print("  Consultando MTC Inspeccion Tecnica...")
        r = await mtc_inspeccion.consultar(page, placa)
        await page.close()
        imprimir_estado(r.fuente, r.estado)
        resultados_doc.append(r)

        page = await context.new_page()
        print("  Consultando SUNARP SPRL (historial propietarios)...")
        r_sprl = await sunarp_sprl.consultar(page, placa, sede=sede_vehiculo)
        await page.close()
        imprimir_estado(r_sprl.fuente, r_sprl.estado)
        resultados_doc.append(r_sprl)

        titulo_anio, titulo_numero, sede = extraer_datos_sprl(r_sprl)
        page = await context.new_page()
        print("  Consultando SUNARP SigueloPlus (monto pagado)...")
        r = await sunarp_siguelo.consultar(
            page,
            titulo_numero=titulo_numero,
            titulo_anio=titulo_anio,
            oficina_registral=sede or "LIMA"
        )
        await page.close()
        imprimir_estado(r.fuente, r.estado)
        resultados_doc.append(r)

        # --- BLOQUE 2: Deudas e Infracciones ---
        print("\n" + C.BOLD + "BLOQUE 2 -- Deudas e Infracciones" + C.RESET)
        print("-" * 50)

        for nombre, modulo in [
            ("SUTRAN infracciones",  sutran),
            ("ATU multas",           atu),
            ("SBS accidentes SOAT",  sbs_accidentes),
            ("Callao papeletas",     callao),
            ("FISE GNV deuda",       gnv_fise),
        ]:
            page = await context.new_page()
            print("  Consultando {}...".format(nombre))
            r = await modulo.consultar(page, placa)
            await page.close()
            imprimir_estado(r.fuente, r.estado)
            resultados_deudas.append(r)

        # --- BLOQUE 3: Papeletas Regionales ---
        print("\n" + C.BOLD + "BLOQUE 3 -- Papeletas Regionales" + C.RESET)
        print("-" * 50)

        scrapers_regionales = [
            ("Trujillo",   trujillo),
            ("Piura",      piura),
            ("Chiclayo",   chiclayo),
            ("Tarapoto",   tarapoto),
            ("Cajamarca",  cajamarca),
            ("Chachapoyas",chachapoyas),
            ("Huancayo",   huancayo),
            ("Ica",        ica),
            ("Tacna",      tacna),
            ("Arequipa",   arequipa),
        ]

        for nombre, modulo in scrapers_regionales:
            page = await context.new_page()
            print("  Consultando {}...".format(nombre))
            r = await modulo.consultar(page, placa)
            await page.close()
            imprimir_estado(r.fuente, r.estado)
            resultados_regiones.append(r)

        await browser.close()

    return resultados_doc, resultados_deudas, resultados_regiones


def main():
    if len(sys.argv) > 1:
        placa = sys.argv[1].strip().upper()
    else:
        placa = input("\n  Ingresa la PLACA del vehiculo a consultar: ").strip().upper()

    if not placa:
        print(C.RED + "Error: debes ingresar una placa." + C.RESET)
        sys.exit(1)

    try:
        resultados_doc, resultados_deudas, resultados_regiones = asyncio.run(
            ejecutar_consultas(placa)
        )
    except KeyboardInterrupt:
        print("\n" + C.YELLOW + "Consulta cancelada por el usuario." + C.RESET)
        sys.exit(0)

    print("\nGenerando reporte HTML...")
    ruta_reporte = generar_reporte(
        placa=placa,
        resultados_doc=resultados_doc,
        resultados_deudas=resultados_deudas,
        resultados_regiones=resultados_regiones,
    )
    print("  Reporte guardado en: " + ruta_reporte)

    webbrowser.open("file:///" + ruta_reporte.replace(os.sep, "/"))

    todos = resultados_doc + resultados_deudas + resultados_regiones
    ok          = sum(1 for r in todos if r.estado == "ok")
    advertencia = sum(1 for r in todos if r.estado == "advertencia")
    error       = sum(1 for r in todos if r.estado == "error")
    sin_datos   = sum(1 for r in todos if r.estado == "sin_datos")

    print("\n" + "=" * 60)
    print("  RESUMEN FINAL -- {}".format(placa))
    print("=" * 60)
    print(C.GREEN  + "  Sin problemas  : {}".format(ok)          + C.RESET)
    print(C.YELLOW + "  Advertencias   : {}".format(advertencia) + C.RESET)
    print(C.RED    + "  Errores        : {}".format(error)       + C.RESET)
    print(C.GRAY   + "  Sin datos      : {}".format(sin_datos)   + C.RESET)
    print(C.CYAN   + "  Total consultas: {}".format(len(todos))  + C.RESET)

    if advertencia > 0:
        print("\n" + C.YELLOW + "  Hay advertencias -- revisa el reporte antes de comprar." + C.RESET)
    elif error == 0 and advertencia == 0:
        print("\n" + C.GREEN + "  Sin problemas detectados." + C.RESET)
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
