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
        scrap_key = self.scrap_key
        target_url = urllib.parse.quote_plus(url)
        render = self.render
        geo_code =self.geo_code
        super_mode = self.super_mode
        new_url = url = f"https://api.scrape.do/?token={scrap_key}&url={target_url}&geoCode={geo_code}&super={super_mode}"
        
        try:
            reponse = requests.request("GET", new_url)
            return BeautifulSoup(reponse.text, 'html.parser')
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {e}")

        except Exception as e:
            logger.exception(f"Unexpected error for {url}: {e}")

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
        