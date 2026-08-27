from scrapers.base import BaseScraper
import requests
from bs4 import BeautifulSoup
import time


class AmazonScraper(BaseScraper):
    def fetch(self, url: str) -> dict:
        soup = self.get_soup(url)
        product_title = self.safe_get_text(soup.find('h1', class_='a-size-large a-spacing-none'))
        product_price = self.safe_get_text(soup.find('span', class_='a-price-whole'))
        product_price_fraction = self.safe_get_text(soup.find('span', class_='a-price-fraction'))
        old_price = self.safe_get_text(soup.select_one("span.a-offscreen"))  # NOT ALWAYS PRESENT
        discount = self.safe_get_text(soup.select_one("span.savingsPercentage"))  # NOT ALWAYS PRESENT
        stock = self.safe_get_text(soup.select_one("span.primary-availability-message"))
        currency = self.safe_get_text(soup.find('span', class_='a-price-symbol'))
        reviews = self.safe_get_text(soup.find(id='acrCustomerReviewText'), default="No reviews")
        brand = self.safe_get_text(soup.select_one("span.a-size-base.po-break-word"))
        rating = self.safe_get_text(soup.select_one('span[data-hook="rating-out-of-text"]'))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "title": product_title,
            "price": product_price,
            "price_fraction": product_price_fraction,
            "old_price": old_price,
            "discount": discount,
            "currency": currency,
            "reviews": reviews,
            "rating": rating,
            "timestamp": timestamp,
            "brand": brand,
            "stock": stock
        }
        