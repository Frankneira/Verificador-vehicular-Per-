"""
ica.py — Papeletas SAT Ica.
URL: https://m.satica.gob.pe/consultapapeletas.php
Proceso: Seleccionar "PAPELETAS" → ingresar placa → buscar.
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    # El portal de Ica puede tener un menú previo para seleccionar "Papeletas"
    resultado = await consultar_papeleta(
        page=page, url=URLS["ica"], ciudad="Ica (SAT)", placa=placa,
        selector_buscar=(
            "button:has-text('Consultar'), button:has-text('Buscar'), "
            "input[type='submit'], button[type='submit']"
        ),
        espera_extra=3.0,
    )
    return resultado
