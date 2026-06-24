"""
cajamarca.py — Papeletas SAT Cajamarca.
URL: https://www.satcajamarca.gob.pe/#/
El portal usa Angular (SPA) — requiere más tiempo de carga.
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["cajamarca"], ciudad="Cajamarca (SAT)", placa=placa,
        selector_placa=(
            "input[placeholder*='plac' i], input[id*='plac' i], "
            "input[ng-model*='plac' i], input[type='text']"
        ),
        espera_extra=4.0,  # Angular SPA necesita más tiempo
    )
