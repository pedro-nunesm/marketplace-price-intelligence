from scrapers.base import BaseScraper
import requests
from bs4 import BeautifulSoup
import time
import logging 
from typing import List, Dict, Optional
import os 
import urllib.parse

logger = logging.getLogger(__name__)


class MediaMarktScraper(BaseScraper):
    def get_soup(self, url:str) -> Optional[BeautifulSoup]:
        target_url = urllib.parse.quote_plus(url)
        new_url = f"https://api.scrape.do/?token={self.scrap_key}&url={target_url}&geoCode={self.geo_code}&super={self.super_mode}&render={self.render}"
        
        # CHECKPOINT 1: Confirma que o método foi chamado e mostra a URL exata
        print(f"\n---> [Mediamarkt] Iniciando requisição para: {url}")
        print(f"---> [Mediamarkt] URL enviada ao Scrape.Do: {new_url}")
        
        try:
            reponse = self.session.get(new_url, timeout=self.REQUEST_TIMEOUT)
            
            # CHECKPOINT 2: Mostra o código de status que o Scrape.do devolveu
            print(f"---> [Mediamarkt] Resposta recebida! Status Code: {reponse.status_code}")
            
            reponse.raise_for_status()
            return BeautifulSoup(reponse.text, 'html.parser')
        
        except requests.exceptions.RequestException as e:
            # Usando print para garantir que o erro apareça na tela, ignorando o logger
            print(f"!!! ERRO DE REQUISIÇÃO [Mediamarkt]: {e}")
        except Exception as e:
            print(f"!!! ERRO INESPERADO [Mediamarkt]: {e}")

        return None

    def fetch(self, url: str) -> dict:
        soup = self.get_soup(url)
        product_title = self.safe_get_text(soup.find("h1", class_="tw-text-5xl"))
        product_price = self.safe_get_text(soup.find("span", class_="price-item price-item--regular"))
        discount = self.safe_get_text(soup.find("span", class_="discount-badge"))  # NOT ALWAYS PRESENT
        stock = self.safe_get_text(soup.find("div", class_="limitedStockAlert_text"))
        reviews = self.safe_get_text(soup.find("div",class_="jdgm-rev-widg__summary-text"), default="No reviews")
        rating = self.safe_get_text(soup.find("span", class_="jdgm-rev-widg__summary-average"))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "title": product_title,
            "price": product_price,
            "discount": discount,
            "reviews": reviews,
            "rating": rating,
            "timestamp": timestamp,
            "stock": stock
        }
        