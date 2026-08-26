from scrapers.base import BaseScraper
import requests
from bs4 import BeautifulSoup
import time
import logging 
from typing import List, Dict, Optional
import os 
import urllib.parse

logger = logging.getLogger(__name__)



class FnacScraper(BaseScraper):
    def get_soup(self, url:str) -> Optional[BeautifulSoup]:
        target_url = urllib.parse.quote_plus(url)
        
        # URL sem o render=true, voltando ao comportamento original que funcionava para a Fnac
        new_url = f"https://api.scrape.do/?token={self.scrap_key}&url={target_url}&geoCode={self.geo_code}&super={self.super_mode}"
        
        print(f"\n---> [Fnac] Iniciando requisição para: {url}")
        
        try:
            reponse = self.session.get(new_url, timeout=self.REQUEST_TIMEOUT)
            print(f"---> [Fnac] Resposta recebida! Status Code: {reponse.status_code}")
            reponse.raise_for_status()
            return BeautifulSoup(reponse.text, 'html.parser')
        
        except requests.exceptions.RequestException as e:
            print(f"!!! ERRO DE REQUISIÇÃO [Fnac]: {e}")
        except Exception as e:
            print(f"!!! ERRO INESPERADO [Fnac]: {e}")

        return None

    def fetch(self, url: str) -> dict:
        soup = self.get_soup(url)
        product_title = self.safe_get_text(soup.find("h1", class_="f-productHeader__heading"))
        product_price = self.safe_get_text(soup.find("span", class_="f-faPriceBox__price"))
        old_price = self.safe_get_text(soup.select_one("strong.f-faPriceBox__price--striked"))  # NOT ALWAYS PRESENT
        discount = self.safe_get_text(soup.find("span", class_="f-faPriceBox__stimuliOpcLabel stimuliOPC-label stimuliOPC-label--red"))  # NOT ALWAYS PRESENT
        reviews = self.safe_get_text(soup.select_one("span.customerReviewsRating__countTotal"), default="No reviews")
        rating = self.safe_get_text(soup.select_one("b.customerReviewsRating__score"))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "title": product_title,
            "price": product_price,
            "old_price": old_price,
            "discount": discount,
            "reviews": reviews,
            "rating": rating,
            "timestamp": timestamp,
        }
        