"""
sunarp_sprl.py — Historial de propietarios en SUNARP SPRL.
URL: https://sprl.sunarp.gob.pe/sprl/main/partidas-base-grafica-registral

Proceso multi-paso:
  1. Login con usuario y contraseña
  2. Seleccionar Oficina Registral (obtenida de la consulta SUNARP vehicular)
  3. Área registral: Propiedad Vehicular
  4. Buscar por Placa
  5. Ver asientos → click en el último título (cuadro verde)
  6. Extraer: Título, Inscripción, Presentación, Rubro, Acto, Participantes
  7. Detectar alertas: "Embargo", "Prescripción de dominio"

Retorna también el número de título para uso en sunarp_siguelo.py.
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT, SUNARP_SPRL_USUARIO, SUNARP_SPRL_CLAVE
from scrapers.base import ResultadoConsulta


# Palabras clave que generan alerta legal
ALERTAS_LEGALES = [
    "prescripción de dominio", "embargo", "medida cautelar",
    "anotación de demanda", "hipoteca", "gravamen", "prohibición",
    "inmovilización", "bloqueo registral",
]


async def consultar(page: Page, placa: str, sede: str = "") -> ResultadoConsulta:
    """
    Args:
        page  : Página de Playwright (contexto compartido).
        placa : Placa del vehículo.
        sede  : Sede/Oficina registral (ej: "LIMA", obtenida de SUNARP vehicular).
                Si está vacía, se intenta con "LIMA" por defecto.
    """
    resultado = ResultadoConsulta(
        fuente="SUNARP SPRL — Historial de Propietarios",
        url=URLS["sunarp_sprl"]
    )

    if not SUNARP_SPRL_USUARIO or not SUNARP_SPRL_CLAVE:
        resultado.marcar_error(
            "Credenciales SUNARP SPRL no configuradas. "
            "Completa SUNARP_SPRL_USUARIO y SUNARP_SPRL_CLAVE en el archivo .env"
        )
        return resultado

    oficina = sede.strip().upper() if sede else "LIMA"

    try:
        # ── PASO 1: Navegar al portal SPRL ──────────────────────────────────
        await page.goto(URLS["sunarp_sprl"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # ── PASO 2: Login ────────────────────────────────────────────────────
        # Campo usuario
        campo_usuario = page.locator(
            "input[name*='user' i], input[id*='user' i], "
            "input[placeholder*='usuario' i], input[type='text']:first-of-type"
        )
        await campo_usuario.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo_usuario.first.fill(SUNARP_SPRL_USUARIO)

        # Campo contraseña
        campo_clave = page.locator("input[type='password']")
        await campo_clave.first.fill(SUNARP_SPRL_CLAVE)

        # Botón ingresar
        btn_login = page.locator(
            "button:has-text('Ingresar'), button:has-text('Iniciar'), "
            "input[type='submit'], button[type='submit']"
        )
        await btn_login.first.click()
        await asyncio.sleep(3)

        # Verificar login exitoso (esperar que desaparezca el formulario de login)
        try:
            await page.wait_for_selector(
                "input[type='password']",
                state="hidden",
                timeout=10_000
            )
        except PWTimeout:
            # Verificar si hay mensaje de error de login
            error_texto = await page.locator(".error, .alert-danger, .msg-error").first.inner_text() if await page.locator(".error, .alert-danger").count() > 0 else ""
            resultado.marcar_error(
                f"Login fallido en SUNARP SPRL. "
                f"Verifica usuario/contraseña en .env. {error_texto}".strip()
            )
            return resultado

        # ── PASO 3: Seleccionar Oficina Registral ────────────────────────────
        await asyncio.sleep(2)
        selector_oficina = page.locator(
            "select[id*='oficina' i], select[name*='oficina' i], "
            "select[id*='sede' i], select[name*='sede' i]"
        )
        if await selector_oficina.count() > 0:
            # Intentar seleccionar por texto de la sede
            try:
                await selector_oficina.first.select_option(label=oficina)
            except Exception:
                # Si no encuentra exacto, seleccionar la opción que contenga el texto
                opciones = await selector_oficina.first.locator("option").all()
                for op in opciones:
                    texto_op = (await op.inner_text()).upper()
                    if oficina in texto_op or "LIMA" in texto_op:
                        valor = await op.get_attribute("value")
                        await selector_oficina.first.select_option(value=valor)
                        break
            await asyncio.sleep(1)

        # ── PASO 4: Seleccionar Área Registral → Propiedad Vehicular ─────────
        selector_area = page.locator(
            "select[id*='area' i], select[name*='area' i], "
            "select[id*='registro' i]"
        )
        if await selector_area.count() > 0:
            try:
                await selector_area.first.select_option(label="Propiedad Vehicular")
            except Exception:
                try:
                    await selector_area.first.select_option(label="PROPIEDAD VEHICULAR")
                except Exception:
                    pass
            await asyncio.sleep(1)

        # ── PASO 5: Buscar por Placa ─────────────────────────────────────────
        # Seleccionar criterio "Placa"
        selector_criterio = page.locator(
            "select[id*='criterio' i], select[name*='criterio' i], "
            "select[id*='tipo' i], select[id*='buscar' i]"
        )
        if await selector_criterio.count() > 0:
            try:
                await selector_criterio.first.select_option(label="Placa")
            except Exception:
                try:
                    await selector_criterio.first.select_option(label="PLACA")
                except Exception:
                    pass
            await asyncio.sleep(0.5)

        # Ingresar placa
        campo_placa = page.locator(
            "input[id*='plac' i], input[name*='plac' i], "
            "input[placeholder*='plac' i], input[type='text']:last-of-type"
        )
        await campo_placa.first.wait_for(state="visible", timeout=TIMEOUT)
        await campo_placa.first.fill(placa.upper().strip())

        # Botón buscar
        btn_buscar = page.locator(
            "button:has-text('Buscar'), button:has-text('Consultar'), "
            "button[type='submit'], input[value*='Buscar' i]"
        )
        await btn_buscar.first.click()
        await asyncio.sleep(3)

        # ── PASO 6: Ver Asientos ─────────────────────────────────────────────
        btn_asientos = page.locator(
            "button:has-text('Ver asientos'), a:has-text('Ver asientos'), "
            "button:has-text('Asientos'), a:has-text('Asientos'), "
            ".btn-asientos, [title*='asiento' i]"
        )
        await btn_asientos.first.wait_for(state="visible", timeout=TIMEOUT)
        await btn_asientos.first.click()
        await asyncio.sleep(3)

        # ── PASO 7: Click en el último título (cuadro verde) ─────────────────
        # Los títulos aparecen como filas — tomar el último
        titulos = page.locator(
            "table tr.green, table tr.titulo, .titulo-item, "
            ".cuadro-verde, tr[class*='green'], tr[class*='titulo']"
        )
        count = await titulos.count()

        if count == 0:
            # Intentar con cualquier fila de tabla y tomar la última
            titulos = page.locator("table tbody tr")
            count = await titulos.count()

        if count == 0:
            resultado.marcar_sin_datos(
                "No se encontraron títulos registrales para esta placa en SUNARP SPRL."
            )
            return resultado

        # Guardar cantidad de títulos
        total_titulos = count

        # Click en el último título — abre popup o nueva ventana
        ultimo_titulo = titulos.nth(count - 1)

        # Manejar nueva ventana/popup
        async with page.context.expect_page() as nueva_pagina_info:
            await ultimo_titulo.click()
            await asyncio.sleep(1)

        nueva_pagina = await nueva_pagina_info.value
        await nueva_pagina.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(2)

        # ── PASO 8: Extraer datos del asiento ────────────────────────────────
        contenido_total = await nueva_pagina.content()
        texto_total = await nueva_pagina.locator("body").inner_text()

        datos = {
            "Total de títulos registrados": str(total_titulos),
        }

        # Extraer campos específicos por su label
        campos_objetivo = [
            "Título", "Inscripción", "Presentación", "Rubro",
            "Acto", "Participantes Naturales", "Participantes Jurídicos",
        ]

        filas = await nueva_pagina.locator("table tr, .field-row, dl dt").all()
        for fila in filas:
            texto = await fila.inner_text()
            partes = [p.strip() for p in texto.split("\n") if p.strip()]
            if len(partes) >= 2:
                clave = partes[0].rstrip(":")
                valor = " ".join(partes[1:]).strip()
                datos[clave] = valor

        # Si no se obtuvo nada de las filas, parsear el texto plano
        if len(datos) <= 1:
            import re
            for campo in campos_objetivo:
                patron = rf"{campo}\s*[:\-]?\s*(.+?)(?=\n|$)"
                m = re.search(patron, texto_total, re.IGNORECASE)
                if m:
                    datos[campo] = m.group(1).strip()

        # ── PASO 9: Detectar alertas legales ─────────────────────────────────
        alertas_encontradas = [
            alerta.title() for alerta in ALERTAS_LEGALES
            if alerta in texto_total.lower()
        ]

        await nueva_pagina.close()

        if alertas_encontradas:
            resultado.marcar_advertencia(
                datos,
                f"🚨 ALERTA LEGAL detectada en el registro: "
                f"{', '.join(alertas_encontradas)}. "
                f"Consulta a un abogado antes de proceder con la compra."
            )
        else:
            resultado.marcar_ok(datos)

    except PWTimeout:
        resultado.marcar_error(
            "Tiempo de espera agotado en SUNARP SPRL. "
            "El portal puede estar lento o requiere resolver un CAPTCHA."
        )
    except Exception as exc:
        resultado.marcar_error(f"Error en SUNARP SPRL: {exc}")

    return resultado
