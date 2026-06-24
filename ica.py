"""
callao.py — Papeletas Municipalidad del Callao.
URL: https://pagopapeletascallao.pe/

El portal del Callao puede requerir un código de seguridad (captcha visual).
Se ejecuta en modo visible para que el usuario lo resuelva manualmente.
"""
import asyncio
from playwright.async_api import Page, TimeoutError as PWTimeout
from config import URLS, TIMEOUT
from scrapers.papeleta_base import consultar_papeleta


async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page,
        url=URLS["callao"],
        ciudad="Callao",
        placa=placa,
        selector_placa=(
            "input[id*='plac' i], input[name*='plac' i], "
            "input[placeholder*='plac' i], input[type='text']"
        ),
        selector_buscar=(
            "button:has-text('Consultar'), button:has-text('Buscar'), "
            "input[type='submit'], button[type='submit']"
        ),
        espera_extra=3.0,  # El Callao tarda un poco más
    )
