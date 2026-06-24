"""
atu.py — Consulta de multas ATU por placa.
URL: https://pasarela.atu.gob.pe/

Extrae: Listado de multas (número, descripción, monto, estado).
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    resultado = ResultadoConsulta(
        fuente="ATU — Multas de Transporte Urbano",
        url=URLS["atu"]
    )

    try:
        await page.goto(URLS["atu"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(3)  # ATU usa React/SPA — necesita más tiempo

        # ATU tiene una SPA (Single Page App), buscar campo de placa
        campo = page.locator(
            "input[placeholder*='placa' i], input[id*='placa' i], "
            "input[name*='placa' i], input[type='text']"
        )
        await campo.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo.first.fill(placa.upper().strip())

        # Botón buscar
        btn = page.locator(
            "button:has-text('Buscar'), button:has-text('Consultar'), "
            "button[type='submit'], input[type='submit']"
        )
        await btn.first.click()
        await asyncio.sleep(4)  # Esperar respuesta API interna

        # Esperar resultado
        await page.wait_for_selector(
            "table, .resultado, .multa-item, .card, .alert, "
            "p:has-text('No'), div:has-text('sin multas')",
            timeout=TIMEOUT
        )

        # Verificar sin multas
        texto_pagina = (await page.content()).lower()
        palabras_sin_multa = [
            "no tiene multas", "sin multas", "no registra multas",
            "no se encontraron", "no hay multas"
        ]
        if any(p in texto_pagina for p in palabras_sin_multa):
            resultado.marcar_ok({"multas": [], "resumen": "✅ Sin multas ATU registradas"})
            return resultado

        # Extraer multas de la tabla
        multas = []
        filas = await page.locator("table tbody tr, .multa-row, .resultado-item").all()

        for fila in filas:
            texto = await fila.inner_text()
            if texto.strip():
                celdas = await fila.locator("td, .col").all()
                valores = [(await c.inner_text()).strip() for c in celdas if (await c.inner_text()).strip()]
                if valores:
                    multas.append({"detalle": " | ".join(valores)})

        # Obtener headers
        headers = []
        ths = await page.locator("table thead th").all()
        for th in ths:
            h = (await th.inner_text()).strip()
            if h:
                headers.append(h)

        if multas:
            resultado.marcar_advertencia(
                {"multas": multas, "total": len(multas)},
                f"⚠️ Se encontraron {len(multas)} multa(s) en ATU."
            )
        else:
            resultado.marcar_ok({"multas": [], "resumen": "✅ Sin multas ATU registradas"})

    except PWTimeout:
        resultado.marcar_error("Tiempo de espera agotado al consultar ATU.")
    except Exception as exc:
        resultado.marcar_error(f"Error inesperado: {exc}")

    return resultado
