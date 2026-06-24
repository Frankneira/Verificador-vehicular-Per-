"""
gnv_fise.py — Consulta de deuda de gas GNV en FISE/MINEM.
URL: https://fise.minem.gob.pe:23308/consulta-taller/pages/consultaTaller/inicio

Extrae: si el vehículo tiene deuda GNV pendiente o no tiene información.
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    resultado = ResultadoConsulta(
        fuente="FISE/MINEM — Deuda Gas GNV",
        url=URLS["gnv_fise"]
    )

    try:
        await page.goto(URLS["gnv_fise"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(3)  # Portal GNV suele ser lento

        # Campo placa
        campo = page.locator(
            "input[id*='plac' i], input[name*='plac' i], "
            "input[placeholder*='plac' i], input[type='text']"
        )
        await campo.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo.first.fill(placa.upper().strip())

        # Botón buscar
        btn = page.locator(
            "button:has-text('Consultar'), button:has-text('Buscar'), "
            "input[type='submit'], button[type='submit']"
        )
        await btn.first.click()
        await asyncio.sleep(4)

        # Esperar resultado
        try:
            await page.wait_for_selector(
                "table, .resultado, .alert, .mensaje, p, div.content",
                timeout=TIMEOUT
            )
        except PWTimeout:
            pass

        texto = (await page.locator("body").inner_text()).lower()

        # Determinar estado
        if any(p in texto for p in ["no existe", "no registra", "sin deuda", "no tiene deuda", "no se encontró"]):
            resultado.marcar_ok({
                "Estado GNV": "Sin deuda registrada",
                "Resumen": "✅ El vehículo no tiene deuda GNV en FISE."
            })
        elif any(p in texto for p in ["deuda", "monto", "pendiente", "saldo"]):
            # Extraer monto si está disponible
            datos = {"Estado GNV": "Posible deuda detectada"}
            filas = await page.locator("table tr").all()
            for fila in filas:
                texto_fila = await fila.inner_text()
                partes = [p.strip() for p in texto_fila.split("\n") if p.strip()]
                if len(partes) >= 2:
                    datos[partes[0].rstrip(":")] = " ".join(partes[1:])
            resultado.marcar_advertencia(
                datos,
                "⚠️ Se detectó deuda GNV en FISE. Verifica el monto antes de comprar."
            )
        else:
            resultado.marcar_sin_datos(
                "No se encontró información de GNV para esta placa. "
                "Es posible que el vehículo no esté registrado con GNV."
            )

    except PWTimeout:
        resultado.marcar_error("Tiempo de espera agotado al consultar FISE GNV.")
    except Exception as exc:
        resultado.marcar_error(f"Error en FISE GNV: {exc}")

    return resultado
