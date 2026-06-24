"""
sunarp_siguelo.py — Consulta de monto pagado por el vehículo en SUNARP SigueloPlus.
URL: https://sigueloplus.sunarp.gob.pe/siguelo/

Proceso:
  1. Navegar al portal SigueloPlus
  2. Ingresar Oficina Registral, Año del título y Número del título
     (estos datos provienen del resultado de sunarp_sprl.py)
  3. Click en "Acceder al asiento de inscripción y TIVE"
  4. Click en el ícono verde
  5. Extraer: Acto, Precio, Monto pagado, Fecha, Fecha de asiento

NOTA: Este scraper necesita el número de título obtenido de SUNARP SPRL.
Si no se dispone del título, se marca como sin_datos.
"""
import asyncio
import re
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(
    page: Page,
    titulo_numero: str = "",
    titulo_anio: str = "",
    oficina_registral: str = "LIMA"
) -> ResultadoConsulta:
    """
    Args:
        page              : Página de Playwright.
        titulo_numero     : Número de título obtenido de SUNARP SPRL (ej: "00735749").
        titulo_anio       : Año del título (ej: "2024").
        oficina_registral : Oficina registral (ej: "LIMA").
    """
    resultado = ResultadoConsulta(
        fuente="SUNARP SigueloPlus — Monto Pagado por el Vehículo",
        url=URLS["sunarp_siguelo"]
    )

    # Validar que tenemos el número de título
    if not titulo_numero or not titulo_anio:
        resultado.marcar_sin_datos(
            "No se dispone del número de título registral. "
            "Este dato es obtenido automáticamente de la consulta SUNARP SPRL (paso 4). "
            "Si el SPRL falló, esta consulta no puede ejecutarse."
        )
        return resultado

    try:
        await page.goto(URLS["sunarp_siguelo"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # ── PASO 1: Seleccionar Oficina Registral ────────────────────────────
        selector_oficina = page.locator(
            "select[id*='oficina' i], select[name*='oficina' i], "
            "select[id*='sede' i], select:first-of-type"
        )
        if await selector_oficina.count() > 0:
            try:
                await selector_oficina.first.select_option(label=oficina_registral)
            except Exception:
                opciones = await selector_oficina.first.locator("option").all()
                for op in opciones:
                    if oficina_registral.upper() in (await op.inner_text()).upper():
                        await selector_oficina.first.select_option(
                            value=await op.get_attribute("value")
                        )
                        break
            await asyncio.sleep(0.5)

        # ── PASO 2: Año del título ────────────────────────────────────────────
        campo_anio = page.locator(
            "input[id*='anio' i], input[name*='anio' i], input[id*='año' i], "
            "input[placeholder*='año' i], input[placeholder*='anio' i]"
        )
        if await campo_anio.count() > 0:
            await campo_anio.first.fill(titulo_anio.strip())
        await asyncio.sleep(0.3)

        # ── PASO 3: Número del título ─────────────────────────────────────────
        campo_numero = page.locator(
            "input[id*='numero' i], input[name*='numero' i], "
            "input[placeholder*='número' i], input[placeholder*='titulo' i], "
            "input[type='text']:last-of-type"
        )
        await campo_numero.first.fill(titulo_numero.strip())

        # ── PASO 4: Botón Buscar ──────────────────────────────────────────────
        btn_buscar = page.locator(
            "button:has-text('Buscar'), input[type='submit'], "
            "button[type='submit'], button:has-text('Consultar')"
        )
        await btn_buscar.first.click()
        await asyncio.sleep(3)

        # ── PASO 5: Click en "Acceder al asiento de inscripción y TIVE" ──────
        btn_acceder = page.locator(
            "a:has-text('Acceder'), button:has-text('Acceder'), "
            "a:has-text('asiento'), a:has-text('TIVE'), "
            ".btn-acceder, [title*='asiento' i]"
        )
        await btn_acceder.first.wait_for(state="visible", timeout=TIMEOUT)
        await btn_acceder.first.click()
        await asyncio.sleep(2)

        # ── PASO 6: Click en ícono verde ─────────────────────────────────────
        icono_verde = page.locator(
            ".btn-success, .btn-green, button.green, a.green, "
            "img[src*='green'], .icon-green, td.green a, "
            "button:has-text('Ver'), a[title*='ver' i]"
        )
        if await icono_verde.count() > 0:
            # Manejar posible nueva ventana/popup
            try:
                async with page.context.expect_page(timeout=5_000) as nueva_p_info:
                    await icono_verde.first.click()
                nueva_pagina = await nueva_p_info.value
                await nueva_pagina.wait_for_load_state("domcontentloaded")
                await asyncio.sleep(2)
                texto_resultado = await nueva_pagina.locator("body").inner_text()
                await nueva_pagina.close()
            except Exception:
                await icono_verde.first.click()
                await asyncio.sleep(2)
                texto_resultado = await page.locator("body").inner_text()
        else:
            texto_resultado = await page.locator("body").inner_text()

        # ── PASO 7: Extraer datos ─────────────────────────────────────────────
        datos = {
            "Año / Título": f"{titulo_anio} — {titulo_numero}",
            "Oficina Registral": oficina_registral,
        }

        campos_a_extraer = ["Acto", "Precio", "Monto pagado", "Fecha", "Fecha de asiento"]
        for campo in campos_a_extraer:
            patron = rf"{campo}\s*[:\-]?\s*(.+?)(?=\n|$)"
            m = re.search(patron, texto_resultado, re.IGNORECASE)
            if m:
                datos[campo] = m.group(1).strip()

        # Extraer también de tabla si existe
        filas = await page.locator("table tr").all()
        for fila in filas:
            texto = await fila.inner_text()
            partes = [p.strip() for p in texto.split("\n") if p.strip()]
            if len(partes) >= 2:
                datos[partes[0].rstrip(":")] = " ".join(partes[1:])

        if len(datos) > 2:  # Más que solo los campos base
            resultado.marcar_ok(datos)
        else:
            resultado.marcar_sin_datos(
                "Se ejecutó la consulta pero no se pudo extraer el monto. "
                "Es posible que el portal haya cambiado su estructura."
            )

    except PWTimeout:
        resultado.marcar_error("Tiempo de espera agotado en SUNARP SigueloPlus.")
    except Exception as exc:
        resultado.marcar_error(f"Error en SigueloPlus: {exc}")

    return resultado
