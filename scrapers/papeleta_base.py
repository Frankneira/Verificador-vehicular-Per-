"""
papeleta_base.py — Función genérica para consulta de papeletas municipales.

La mayoría de municipalidades tienen el mismo patrón:
  1. Ir a la URL
  2. Ingresar la placa
  3. Hacer click en Buscar
  4. Extraer resultados o confirmar "sin papeletas"

Para casos especiales (login, selector de tipo, campos adicionales),
cada scraper específico extiende este comportamiento.
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import TIMEOUT
from scrapers.base import ResultadoConsulta


PALABRAS_SIN_DEUDA = [
    "no registra", "sin multas", "sin papeletas", "no tiene",
    "no se encontraron", "no hay", "no presenta", "0 resultado",
    "sin infracciones", "no existe", "not found", "sin deuda",
]

PALABRAS_CON_DEUDA = [
    "monto", "deuda", "infracción", "multa", "papeleta",
    "pendiente", "s/.", "sol", "fecha de infracción",
]


async def consultar_papeleta(
    page: Page,
    url: str,
    ciudad: str,
    placa: str,
    *,
    selector_placa: str = None,
    selector_buscar: str = None,
    selector_tipo: str = None,
    valor_tipo: str = "Placa",
    campos_extra: dict = None,
    espera_extra: float = 2.0,
    selector_resultado: str = None,
) -> ResultadoConsulta:
    """
    Consulta genérica de papeletas por placa.

    Args:
        page             : Página Playwright.
        url              : URL del portal municipal.
        ciudad           : Nombre de la ciudad (para el reporte).
        placa            : Placa del vehículo.
        selector_placa   : CSS selector del campo placa (usa heurísticas si None).
        selector_buscar  : CSS selector del botón buscar (usa heurísticas si None).
        selector_tipo    : CSS selector del select de tipo de búsqueda (opcional).
        valor_tipo       : Valor a seleccionar en el select tipo (ej: "Placa").
        campos_extra     : Dict {selector: valor} para campos adicionales.
        espera_extra     : Segundos extra de espera después del click.
        selector_resultado: CSS selector donde aparece el resultado.
    """
    resultado = ResultadoConsulta(
        fuente=f"Papeletas — {ciudad}",
        url=url
    )

    # Selectores heurísticos por defecto
    sel_placa = selector_placa or (
        "input[id*='plac' i], input[name*='plac' i], "
        "input[placeholder*='plac' i], input[id*='nro_plac' i], "
        "input[type='text']"
    )
    sel_buscar = selector_buscar or (
        "button:has-text('Buscar'), button:has-text('Consultar'), "
        "input[type='submit'], button[type='submit'], "
        "a:has-text('Buscar'), button:has-text('Ver')"
    )
    sel_resultado = selector_resultado or (
        "table, .resultado, #resultado, .alert, .mensaje, "
        ".infracciones, .papeleta, p, div.content"
    )

    try:
        await page.goto(url, timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # Seleccionar tipo si aplica
        if selector_tipo:
            sel = page.locator(selector_tipo)
            if await sel.count() > 0:
                try:
                    await sel.first.select_option(label=valor_tipo)
                except Exception:
                    try:
                        await sel.first.select_option(value=valor_tipo.lower())
                    except Exception:
                        pass
                await asyncio.sleep(0.5)

        # Campos extra (DNI, correo, etc.)
        if campos_extra:
            for sel_extra, val_extra in campos_extra.items():
                campo = page.locator(sel_extra)
                if await campo.count() > 0:
                    await campo.first.fill(str(val_extra))
                    await asyncio.sleep(0.3)

        # Ingresar placa
        campo = page.locator(sel_placa)
        await campo.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo.first.fill(placa.upper().strip())

        # Buscar
        btn = page.locator(sel_buscar)
        await btn.first.click()
        await asyncio.sleep(espera_extra + 1)

        # Esperar resultado
        try:
            await page.wait_for_selector(sel_resultado, timeout=TIMEOUT)
        except PWTimeout:
            pass  # Continuar e intentar extraer de todos modos

        # Leer texto completo de la página
        texto = (await page.locator("body").inner_text()).lower()

        # Determinar si hay deuda
        sin_deuda = any(p in texto for p in PALABRAS_SIN_DEUDA)
        con_deuda = any(p in texto for p in PALABRAS_CON_DEUDA)

        if sin_deuda and not con_deuda:
            resultado.marcar_ok({
                "Ciudad": ciudad,
                "Estado": "Sin papeletas / deudas",
                "Resumen": "✅ No registra papeletas en esta jurisdicción."
            })
            return resultado

        # Intentar extraer tabla de papeletas
        papeletas = []
        filas = await page.locator("table tbody tr").all()
        headers = []
        ths = await page.locator("table thead th, table tr:first-child th").all()
        for th in ths:
            h = (await th.inner_text()).strip()
            if h:
                headers.append(h)

        for fila in filas:
            celdas = await fila.locator("td").all()
            valores = [(await c.inner_text()).strip() for c in celdas]
            valores = [v for v in valores if v]
            if valores:
                if headers and len(headers) == len(valores):
                    papeletas.append(dict(zip(headers, valores)))
                else:
                    papeletas.append({"detalle": " | ".join(valores)})

        if papeletas:
            resultado.marcar_advertencia(
                {"Ciudad": ciudad, "papeletas": papeletas, "total": len(papeletas)},
                f"⚠️ Se encontraron {len(papeletas)} papeleta(s) en {ciudad}."
            )
        elif con_deuda:
            # Hay indicios de deuda pero no tabla estructurada
            lineas_deuda = [
                l.strip() for l in (await page.locator("body").inner_text()).split("\n")
                if any(p in l.lower() for p in PALABRAS_CON_DEUDA) and l.strip()
            ]
            resultado.marcar_advertencia(
                {"Ciudad": ciudad, "detalle": " | ".join(lineas_deuda[:5])},
                f"⚠️ Se detectó posible deuda en {ciudad}. Verifica manualmente."
            )
        else:
            resultado.marcar_sin_datos(
                f"No se pudo determinar el estado de papeletas en {ciudad}. "
                f"Verifica el portal directamente: {url}"
            )

    except PWTimeout:
        resultado.marcar_error(f"Tiempo de espera agotado al consultar {ciudad}.")
    except Exception as exc:
        resultado.marcar_error(f"Error consultando {ciudad}: {exc}")

    return resultado
