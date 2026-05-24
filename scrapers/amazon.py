from scrapers.base import BaseScraper
import requests
from bs4 import BeautifulSoup
import time


class AmazonScraper(BaseScraper):
    def fetch(self, url: str) -> dict:
        soup = self.get_soup(url)
        product_title = soup.find('h1', class_='a-size-large a-spacing-none').get_text()
        product_price = soup.find('span', class_='a-price-whole').get_text()
        product_price_fraction = soup.find('span', class_='a-price-fraction').get_text()
        old_price = soup.select_one("span.a-offscreen").get_text() #NOT ALWAYS PRESENT
        discount = soup.select_one("span.savingsPercentage").get_text() #NOT ALWAYS PRESENT
        stock = soup.select_one("span.primary-availability-message").get_text()
        currency = soup.find('span', class_='a-price-symbol').get_text()
        reviews = soup.find(id='acrCustomerReviewText').get_text()[1:-1]
        brand = soup.select_one("span.a-size-base.po-break-word").get_text()
        rating = soup.select_one('span[data-hook="rating-out-of-text"]').get_text()
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
        