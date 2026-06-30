"""
huancayo.py — Papeletas SAT Huancayo.
URL: http://sathuancayo.fortiddns.com:888/VentanillaVirtual/ConsultaPIT.aspx
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["huancayo"], ciudad="Huancayo (SAT)", placa=placa,
        espera_extra=3.0,
    )
