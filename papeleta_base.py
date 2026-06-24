"""
chachapoyas.py — Papeletas Municipalidad de Chachapoyas.
URL: https://app.munichachapoyas.gob.pe/servicios/consulta_papeletas/app/papeletas.php
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["chachapoyas"], ciudad="Chachapoyas", placa=placa,
        selector_placa="input[name*='plac' i], input[id*='plac' i], input[name='NRO_PLACA'], input[type='text']",
        espera_extra=2.0,
    )
