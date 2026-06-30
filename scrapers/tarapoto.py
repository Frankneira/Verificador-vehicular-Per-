"""
tarapoto.py — Papeletas SAT Tarapoto.
URL: https://www.sat-t.gob.pe/
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["tarapoto"], ciudad="Tarapoto (SAT)", placa=placa,
        espera_extra=2.5,
    )
