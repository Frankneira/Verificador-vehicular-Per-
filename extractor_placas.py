"""
sunarp_vehicular.py — Consulta de propiedad del vehículo en SUNARP.
URL: https://consultavehicular.sunarp.gob.pe/consulta-vehicular/inicio

Extrae: N° de placa, Marca, Modelo, Sede, Año modelo, Propietario(s).
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.base import ResultadoConsulta


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    resultado = ResultadoConsulta(
        fuente="SUNARP — Consulta Vehicular",
        url=URLS["sunarp_vehicular"]
    )

    try:
        await page.goto(URLS["sunarp_vehicular"], timeout=TIMEOUT, wait_until="domcontentloaded")

        # Esperar campo de placa
        campo_placa = page.locator("input[placeholder*='placa' i], input[name*='placa' i], input#placa, input[id*='placa' i]")
        await campo_placa.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo_placa.first.fill(placa.upper().strip())

        # Botón de búsqueda
        btn = page.locator("button[type='submit'], button:has-text('Consultar'), button:has-text('Buscar'), input[type='submit']")
        await btn.first.click()

        # --- Manejo de CAPTCHA ---
        # Si la página tiene CAPTCHA, esperamos hasta 60 segundos para resolución manual
        try:
            # Intentar detectar CAPTCHA visible
            captcha = page.locator("iframe[src*='recaptcha'], .g-recaptcha, #captcha")
            if await captcha.count() > 0:
                print("\n  ⚠️  CAPTCHA detectado en SUNARP. Por favor, resuélvelo en el navegador.")
                print("      El sistema esperará hasta 60 segundos...")
                # Esperar a que desaparezca el CAPTCHA o aparezcan resultados
                await page.wait_for_selector(
                    ".resultado, table, .datos-vehiculo, #resultado",
                    timeout=60_000
                )
        except PWTimeout:
            pass

        # Esperar resultados
        await page.wait_for_selector(
            "table, .resultado, .card, .datos-vehiculo, #datos",
            timeout=TIMEOUT
        )
        await asyncio.sleep(1)

        # Extraer datos — los campos pueden variar según la versión del portal
        datos = {}

        # Estrategia 1: tabla con pares clave-valor
        filas = await page.locator("table tr, .field-row, .dato-item").all()
        for fila in filas:
            texto = await fila.inner_text()
            partes = [p.strip() for p in texto.split("\n") if p.strip()]
            if len(partes) >= 2:
                clave = partes[0].rstrip(":").strip()
                valor = partes[1].strip()
                datos[clave] = valor

        # Estrategia 2: buscar campos específicos por texto
        campos_objetivo = {
            "Placa"        : ["placa", "n° de placa", "numero de placa"],
            "Marca"        : ["marca"],
            "Modelo"       : ["modelo"],
            "Sede"         : ["sede", "oficina registral"],
            "Año modelo"   : ["año", "año modelo", "año fabricacion"],
            "Propietario"  : ["propietario", "titular", "nombre"],
        }

        for nombre, variantes in campos_objetivo.items():
            if nombre not in datos:
                for variante in variantes:
                    locator = page.locator(f"*:has-text('{variante.capitalize()}')")
                    try:
                        count = await locator.count()
                        if count > 0:
                            parent = locator.first
                            texto = await parent.inner_text()
                            # Tomar el texto que viene después del label
                            lineas = [l.strip() for l in texto.split("\n") if l.strip()]
                            if len(lineas) >= 2:
                                datos[nombre] = lineas[1]
                                break
                    except Exception:
                        continue

        if datos:
            resultado.marcar_ok(datos)
        else:
            # Último recurso: capturar todo el texto visible de la sección de resultado
            contenido = await page.locator("main, #content, .container").first.inner_text()
            resultado.marcar_sin_datos(
                f"Se cargó la página pero no se pudieron extraer campos estructurados. "
                f"Contenido obtenido:\n{contenido[:500]}"
            )

    except PWTimeout:
        resultado.marcar_error(
            "Tiempo de espera agotado. El sitio SUNARP puede estar lento o requiere CAPTCHA manual."
        )
    except Exception as exc:
        resultado.marcar_error(f"Error inesperado: {exc}")

    return resultado
