"""
sutran.py — Consulta de récord de infracciones en SUTRAN.
URL: https://www.sutran.gob.pe/consultas/record-de-infracciones/record-de-infracciones/

Extrae: Listado de infracciones (código, descripción, fecha, monto, estado).
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    resultado = ResultadoConsulta(
        fuente="SUTRAN — Récord de Infracciones",
        url=URLS["sutran"]
    )

    try:
        await page.goto(URLS["sutran"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # Seleccionar criterio "Placa" si hay un selector de tipo
        tipo_selector = page.locator("select[name*='tipo' i], select[id*='tipo' i], select[id*='criterio' i]")
        if await tipo_selector.count() > 0:
            await tipo_selector.first.select_option(label="Placa")
            await asyncio.sleep(0.5)

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

        # Esperar resultado o mensaje "sin infracciones"
        await page.wait_for_selector(
            "table, .resultado, #resultado, .alert, .mensaje, p:has-text('No')",
            timeout=TIMEOUT
        )

        # Verificar mensaje "sin infracciones"
        texto_pagina = await page.content()
        palabras_sin_infraccion = [
            "no registra infracciones", "sin infracciones",
            "no tiene infracciones", "no se encontraron"
        ]
        if any(p in texto_pagina.lower() for p in palabras_sin_infraccion):
            resultado.marcar_ok({"infracciones": [], "resumen": "✅ Sin infracciones registradas"})
            return resultado

        # Extraer tabla de infracciones
        infracciones = []
        filas = await page.locator("table tbody tr").all()

        for fila in filas:
            celdas = await fila.locator("td").all()
            textos = [await c.inner_text() for c in celdas]
            textos = [t.strip() for t in textos if t.strip()]
            if textos:
                infracciones.append(textos)

        # Obtener encabezados de columnas
        headers = []
        ths = await page.locator("table thead th, table tr:first-child th").all()
        for th in ths:
            headers.append((await th.inner_text()).strip())

        # Convertir a lista de dicts si hay headers
        infracciones_dict = []
        if headers and infracciones:
            for fila in infracciones:
                item = {}
                for i, h in enumerate(headers):
                    item[h] = fila[i] if i < len(fila) else ""
                infracciones_dict.append(item)
        else:
            infracciones_dict = [{"detalle": " | ".join(f)} for f in infracciones]

        if infracciones_dict:
            resultado.marcar_advertencia(
                {"infracciones": infracciones_dict, "total": len(infracciones_dict)},
                f"⚠️ Se encontraron {len(infracciones_dict)} infracción(es) en SUTRAN."
            )
        else:
            resultado.marcar_ok({"infracciones": [], "resumen": "✅ Sin infracciones registradas"})

    except PWTimeout:
        resultado.marcar_error("Tiempo de espera agotado al consultar SUTRAN.")
    except Exception as exc:
        resultado.marcar_error(f"Error inesperado: {exc}")

    return resultado
