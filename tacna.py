"""
soat_apeseg.py — Consulta de vigencia del SOAT en APESEG.
URL: https://www.apeseg.org.pe/consultas-soat/

Extrae: Estado, Vigente desde, Vigente hasta.
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    resultado = ResultadoConsulta(
        fuente="APESEG — Consulta SOAT",
        url=URLS["soat_apeseg"]
    )

    try:
        await page.goto(URLS["soat_apeseg"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(2)  # JS inicial

        # Campo placa — APESEG usa un input visible en el formulario de consulta
        campo = page.locator(
            "input[placeholder*='placa' i], input[name*='placa' i], "
            "input[id*='placa' i], input[type='text']"
        )
        await campo.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo.first.fill(placa.upper().strip())

        # Botón consultar
        btn = page.locator(
            "button:has-text('Consultar'), button:has-text('Buscar'), "
            "button[type='submit'], input[type='submit']"
        )
        await btn.first.click()
        await asyncio.sleep(2)

        # Esperar resultado
        await page.wait_for_selector(
            ".resultado, table, .soat-info, #resultado, .card-body",
            timeout=TIMEOUT
        )

        # Extraer datos
        datos = {}
        campos_mapa = {
            "Estado"        : ["estado", "vigente", "situacion"],
            "Vigente desde" : ["vigente desde", "inicio", "fecha inicio", "desde"],
            "Vigente hasta" : ["vigente hasta", "fin", "fecha fin", "hasta", "vencimiento"],
            "Compañía"      : ["compañia", "empresa", "aseguradora"],
        }

        # Buscar en tabla
        filas = await page.locator("table tr").all()
        for fila in filas:
            texto = await fila.inner_text()
            partes = [p.strip() for p in texto.split("\t") if p.strip()]
            if len(partes) < 2:
                partes = [p.strip() for p in texto.split("\n") if p.strip()]
            if len(partes) >= 2:
                clave = partes[0].rstrip(":").strip()
                valor = " ".join(partes[1:]).strip()
                datos[clave] = valor

        # Buscar por texto si la tabla no dio resultados
        if not datos:
            for nombre, variantes in campos_mapa.items():
                for variante in variantes:
                    try:
                        el = page.locator(f"*:has-text('{variante}')").last
                        if await el.count() > 0:
                            texto = await el.inner_text()
                            lineas = [l.strip() for l in texto.split("\n") if l.strip()]
                            if len(lineas) >= 2:
                                datos[nombre] = lineas[-1]
                                break
                    except Exception:
                        continue

        # Determinar estado del SOAT
        estado_soat = datos.get("Estado", datos.get("estado", "")).lower()
        if "vigente" in estado_soat or "activo" in estado_soat:
            resultado.marcar_ok(datos)
        elif "vencido" in estado_soat or "expirado" in estado_soat:
            resultado.marcar_advertencia(datos, "⚠️ El SOAT está VENCIDO. El vehículo no puede circular legalmente.")
        elif datos:
            resultado.marcar_ok(datos)
        else:
            resultado.marcar_sin_datos("No se encontró información del SOAT para esta placa.")

    except PWTimeout:
        resultado.marcar_error("Tiempo de espera agotado al consultar APESEG.")
    except Exception as exc:
        resultado.marcar_error(f"Error inesperado: {exc}")

    return resultado
