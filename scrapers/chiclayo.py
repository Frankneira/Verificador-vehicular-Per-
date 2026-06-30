"""
chiclayo.py — Papeletas SAT Chiclayo.
URL: https://virtualsatch.satch.gob.pe/virtualsatch/record_infracciones/buscar_placa_
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["chiclayo"], ciudad="Chiclayo (SAT)", placa=placa,
        espera_extra=2.0,
    )
