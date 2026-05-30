from scrapers.base import BaseScraper
import requests
from bs4 import BeautifulSoup
import time


class MediaMarktScraper(BaseScraper):
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
        