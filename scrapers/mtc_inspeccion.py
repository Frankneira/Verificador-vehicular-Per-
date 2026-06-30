"""
mtc_inspeccion.py — Consulta de Inspección Técnica Vehicular en MTC.
URL: https://rec.mtc.gob.pe/Citv/ArConsultaCitv

Extrae: Estado de inspección, Fecha inicio, Fecha fin (vigencia).
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    resultado = ResultadoConsulta(
        fuente="MTC — Inspección Técnica Vehicular (ITV)",
        url=URLS["mtc_inspeccion"]
    )

    try:
        await page.goto(URLS["mtc_inspeccion"], timeout=TIMEOUT, wait_until="domcontentloaded")
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
            "table, .resultado, #resultado, .grid, .panel-body",
            timeout=TIMEOUT
        )

        datos = {}

        # Extraer de tabla
        filas = await page.locator("table tr").all()
        for fila in filas:
            celdas = await fila.locator("td, th").all()
            textos = [await c.inner_text() for c in celdas]
            textos = [t.strip() for t in textos if t.strip()]
            if len(textos) >= 2:
                datos[textos[0].rstrip(":")] = " ".join(textos[1:])

        # Buscar campos específicos por label
        if not datos:
            for label_text in ["Estado", "Inicio", "Fin", "Resultado", "Vigencia"]:
                try:
                    el = page.locator(f"label:has-text('{label_text}'), td:has-text('{label_text}')")
                    if await el.count() > 0:
                        parent = el.first.locator("..").locator("td, span, input").last
                        valor = await parent.inner_text()
                        datos[label_text] = valor.strip()
                except Exception:
                    continue

        # Determinar estado de ITV
        estado = datos.get("Estado", datos.get("Resultado", "")).lower()
        if "aprobado" in estado or "vigente" in estado or "favorable" in estado:
            resultado.marcar_ok(datos)
        elif "desaprobado" in estado or "vencido" in estado or "rechazado" in estado:
            resultado.marcar_advertencia(
                datos,
                "⚠️ La Inspección Técnica Vehicular está VENCIDA o DESAPROBADA."
            )
        elif datos:
            resultado.marcar_ok(datos)
        else:
            resultado.marcar_sin_datos(
                "No se encontró registro de Inspección Técnica para esta placa."
            )

    except PWTimeout:
        resultado.marcar_error("Tiempo de espera agotado al consultar MTC.")
    except Exception as exc:
        resultado.marcar_error(f"Error inesperado: {exc}")

    return resultado
