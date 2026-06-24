"""
trujillo.py -- Papeletas SAT Trujillo (SATT).
URL: https://satt.gob.pe/servicios/record-de-infracciones

Flujo de 2 pasos:
  Paso 1: Ingresar DNI + Celular + Correo  -> Click "CONSULTAR"
  Paso 2: En la pagina "RECORD DE INFRACCIONES - SATT"
          Ingresar PLACA -> Click "BUSCAR"
          Extraer listado de infracciones.

Credenciales en .env:
  TRUJILLO_DNI      = 45975202
  TRUJILLO_CELULAR  = 969762557
  TRUJILLO_CORREO   = informesautoescuela@gmail.com
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT, TRUJILLO_DNI, TRUJILLO_CELULAR, TRUJILLO_CORREO
from scrapers.base import ResultadoConsulta


# Palabras que indican que NO hay infracciones
PALABRAS_LIMPIO = [
    "no registra", "sin infracciones", "no tiene infracciones",
    "no se encontraron", "no hay infracciones", "0 infraccion",
    "sin multas", "no presenta", "sin papeletas",
]

# Palabras que indican que SI hay infracciones
PALABRAS_INFRACCION = [
    "infraccion", "infracción", "multa", "papeleta",
    "monto", "deuda", "s/.", "pendiente", "fecha",
]


async def consultar(page: Page, placa: str) -> ResultadoConsulta:
    """Consulta papeletas en SAT Trujillo usando flujo de 2 pasos."""

    resultado = ResultadoConsulta(
        fuente="Papeletas -- Trujillo (SATT)",
        url=URLS["trujillo"]
    )

    # Validar credenciales antes de intentar
    if not TRUJILLO_DNI or not TRUJILLO_CELULAR or not TRUJILLO_CORREO:
        resultado.marcar_sin_datos(
            "Credenciales SAT Trujillo no configuradas. "
            "Agrega TRUJILLO_DNI, TRUJILLO_CELULAR y TRUJILLO_CORREO en .env"
        )
        return resultado

    placa_upper = placa.upper().strip()

    try:
        # ── PASO 1: Formulario de identificacion ──────────────────────────────
        await page.goto(URLS["trujillo"], timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(2.5)

        # Detectar captcha
        captcha = await page.locator("iframe[src*='recaptcha'], div.g-recaptcha").count()
        if captcha > 0:
            print("  [TRUJILLO] CAPTCHA detectado -- resuelve manualmente y espera...")
            await asyncio.sleep(30)

        # Campo DNI
        sel_dni = (
            "input[id*='dni' i], input[name*='dni' i], "
            "input[placeholder*='dni' i], input[placeholder*='documento' i]"
        )
        dni_campo = page.locator(sel_dni)
        if await dni_campo.count() == 0:
            resultado.marcar_error("No se encontro el campo DNI en SATT Trujillo.")
            return resultado
        await dni_campo.first.fill("")
        await dni_campo.first.fill(str(TRUJILLO_DNI))
        await asyncio.sleep(0.4)

        # Campo Celular
        sel_cel = (
            "input[id*='celular' i], input[name*='celular' i], "
            "input[placeholder*='celular' i], input[placeholder*='telefono' i], "
            "input[id*='phone' i], input[type='tel']"
        )
        cel_campo = page.locator(sel_cel)
        if await cel_campo.count() > 0:
            await cel_campo.first.fill("")
            await cel_campo.first.fill(str(TRUJILLO_CELULAR))
            await asyncio.sleep(0.4)

        # Campo Correo
        sel_email = (
            "input[id*='correo' i], input[name*='correo' i], "
            "input[placeholder*='correo' i], input[type='email'], "
            "input[id*='email' i], input[name*='email' i]"
        )
        email_campo = page.locator(sel_email)
        if await email_campo.count() > 0:
            await email_campo.first.fill("")
            await email_campo.first.fill(str(TRUJILLO_CORREO))
            await asyncio.sleep(0.4)

        # Boton CONSULTAR (paso 1)
        sel_btn_consultar = (
            "button:has-text('Consultar'), "
            "button:has-text('CONSULTAR'), "
            "input[value*='Consultar' i], "
            "button[type='submit'], "
            "input[type='submit']"
        )
        btn_consultar = page.locator(sel_btn_consultar)
        if await btn_consultar.count() == 0:
            resultado.marcar_error("No se encontro el boton CONSULTAR en SATT Trujillo.")
            return resultado

        await btn_consultar.first.click()
        await asyncio.sleep(3.5)  # Esperar carga de la segunda pantalla

        # ── PASO 2: Busqueda por placa ────────────────────────────────────────
        # Verificar que llegamos a la pagina de RECORD DE INFRACCIONES
        url_actual = page.url
        titulo_pagina = await page.title()
        texto_pagina  = (await page.locator("body").inner_text()).lower()

        # Detectar si hay error de autenticacion
        if any(p in texto_pagina for p in ["error", "invalido", "incorrecto", "no valido"]):
            if not any(p in texto_pagina for p in ["placa", "infracc", "buscar"]):
                resultado.marcar_error(
                    "Error de autenticacion en SATT Trujillo. "
                    "Verifica DNI/Celular/Correo en .env"
                )
                return resultado

        # Campo de placa (segunda pantalla)
        sel_placa = (
            "input[id*='plac' i], input[name*='plac' i], "
            "input[placeholder*='plac' i], "
            "input[id*='nro' i], input[name*='nro' i], "
            "input[id*='vehic' i], input[type='text']"
        )
        placa_campo = page.locator(sel_placa)

        # Esperar que aparezca el campo placa (puede tardar un poco)
        try:
            await placa_campo.first.wait_for(state="visible", timeout=15000)
        except PWTimeout:
            resultado.marcar_error(
                "No aparecio el campo de placa en SATT Trujillo. "
                "Posible error de autenticacion o CAPTCHA pendiente."
            )
            return resultado

        await placa_campo.first.fill("")
        await placa_campo.first.fill(placa_upper)
        await asyncio.sleep(0.5)

        # Boton BUSCAR (paso 2)
        sel_btn_buscar = (
            "button:has-text('Buscar'), "
            "button:has-text('BUSCAR'), "
            "input[value*='Buscar' i], "
            "button[type='submit'], "
            "input[type='submit'], "
            "a:has-text('Buscar')"
        )
        btn_buscar = page.locator(sel_btn_buscar)
        if await btn_buscar.count() == 0:
            resultado.marcar_error("No se encontro el boton BUSCAR en SATT Trujillo.")
            return resultado

        await btn_buscar.first.click()
        await asyncio.sleep(4.0)  # Esperar carga de resultados

        # ── EXTRACCION DE RESULTADOS ──────────────────────────────────────────
        texto_resultado = (await page.locator("body").inner_text()).lower()

        # Verificar si no hay infracciones
        sin_infraccion = any(p in texto_resultado for p in PALABRAS_LIMPIO)
        con_infraccion = any(p in texto_resultado for p in PALABRAS_INFRACCION)

        if sin_infraccion and not con_infraccion:
            resultado.marcar_ok({
                "Ciudad"  : "Trujillo (SATT)",
                "Placa"   : placa_upper,
                "Estado"  : "Sin infracciones",
                "Resumen" : "El vehiculo no registra infracciones en el SAT Trujillo.",
            })
            return resultado

        # Intentar extraer tabla de infracciones
        infracciones = []

        # Obtener cabeceras
        headers = []
        ths = await page.locator("table thead th, table tr:first-child th").all()
        for th in ths:
            h = (await th.inner_text()).strip()
            if h:
                headers.append(h)

        # Obtener filas
        filas = await page.locator("table tbody tr").all()
        for fila in filas:
            celdas = await fila.locator("td").all()
            valores = [(await c.inner_text()).strip() for c in celdas]
            valores = [v for v in valores if v]  # quitar vacios
            if not valores:
                continue
            if headers and len(headers) == len(valores):
                infracciones.append(dict(zip(headers, valores)))
            elif valores:
                # Mapeo generico si no hay cabeceras
                claves_gen = [
                    "Numero", "Fecha", "Codigo", "Descripcion",
                    "Monto", "Estado", "Placa"
                ]
                fila_dict = {}
                for idx, val in enumerate(valores):
                    clave = claves_gen[idx] if idx < len(claves_gen) else "Col{}".format(idx+1)
                    fila_dict[clave] = val
                infracciones.append(fila_dict)

        if infracciones:
            resultado.marcar_advertencia(
                {
                    "Ciudad"       : "Trujillo (SATT)",
                    "Placa"        : placa_upper,
                    "infracciones" : infracciones,
                    "total"        : len(infracciones),
                },
                "El vehiculo tiene {} infraccion(es) registrada(s) en SAT Trujillo.".format(
                    len(infracciones)
                )
            )

        elif con_infraccion:
            # Hay texto de infraccion pero no tabla estructurada
            lineas = [
                l.strip()
                for l in (await page.locator("body").inner_text()).split("\n")
                if any(p in l.lower() for p in PALABRAS_INFRACCION) and l.strip()
            ]
            resultado.marcar_advertencia(
                {
                    "Ciudad"  : "Trujillo (SATT)",
                    "Placa"   : placa_upper,
                    "detalle" : " | ".join(lineas[:8]),
                },
                "Se detectaron posibles infracciones en SAT Trujillo. Verifica el portal."
            )

        else:
            resultado.marcar_sin_datos(
                "No se pudo determinar el estado de infracciones en SAT Trujillo. "
                "Verifica el portal directamente: {}".format(URLS["trujillo"])
            )

    except PWTimeout:
        resultado.marcar_error(
            "Tiempo de espera agotado en SAT Trujillo. "
            "El portal puede estar lento o requerir CAPTCHA manual."
        )
    except Exception as exc:
        resultado.marcar_error("Error en SAT Trujillo: {}".format(str(exc)[:300]))

    return resultado
