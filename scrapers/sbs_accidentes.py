"""
sbs_accidentes.py — Consulta de accidentes cubiertos por SOAT en SBS.
URL: https://servicios.sbs.gob.pe/reportesoat/ReporteCentralRiesgo

Extrae: Número de accidentes registrados por pólizas SOAT en los últimos 5 años.
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    resultado = ResultadoConsulta(
        fuente="SBS — Accidentes Coberturados por SOAT",
        url=URLS["sbs_accidentes"]
    )

    try:
        await page.goto(URLS["sbs_accidentes"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # Campo placa
        campo = page.locator(
            "input[id*='plac' i], input[name*='plac' i], "
            "input[placeholder*='plac' i], input[type='text']"
        )
        await campo.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo.first.fill(placa.upper().strip())

        # Botón consultar
        btn = page.locator(
            "button:has-text('Consultar'), button:has-text('Buscar'), "
            "input[type='submit'], button[type='submit']"
        )
        await btn.first.click()
        await asyncio.sleep(3)

        # Esperar resultado
        await page.wait_for_selector(
            "table, .resultado, #resultado, p, .alert",
            timeout=TIMEOUT
        )

        # Extraer el texto completo del resultado
        contenido = await page.locator("main, #content, .container, body").first.inner_text()

        # Buscar el número de accidentes en el texto
        import re
        datos = {}

        # Patrón: "cuenta con X accidente(s)" o similar
        patron_accidentes = re.search(
            r'(\d+)\s*accidente[s]?\s*coberturado[s]?',
            contenido, re.IGNORECASE
        )
        if patron_accidentes:
            num = int(patron_accidentes.group(1))
            datos["Accidentes en últimos 5 años"] = str(num)
            datos["Fuente"] = "Pólizas SOAT"
            if num == 0:
                resultado.marcar_ok({**datos, "resumen": "✅ Sin accidentes registrados"})
            elif num <= 2:
                resultado.marcar_advertencia(
                    datos,
                    f"⚠️ El vehículo tiene {num} accidente(s) registrado(s) en los últimos 5 años."
                )
            else:
                resultado.marcar_advertencia(
                    datos,
                    f"🚨 El vehículo tiene {num} accidente(s) — historial alto de siniestros."
                )
        else:
            # Sin patrón numérico: extraer el párrafo relevante
            lineas_relevantes = [
                l.strip() for l in contenido.split("\n")
                if any(k in l.lower() for k in ["accidente", "cobertura", "soat", "siniestro", "placa"])
            ]
            if lineas_relevantes:
                datos["Resultado"] = " | ".join(lineas_relevantes[:3])
                resultado.marcar_ok(datos)
            else:
                resultado.marcar_sin_datos(
                    "No se encontró información de accidentes para esta placa."
                )

    except PWTimeout:
        resultado.marcar_error("Tiempo de espera agotado al consultar SBS.")
    except Exception as exc:
        resultado.marcar_error(f"Error inesperado: {exc}")

    return resultado
