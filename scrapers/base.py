from abc import ABC, abstractmethod
from typing import List, Dict, Optional

import logging 
import requests

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os 
from dotenv import load_dotenv

load_dotenv() 

logger = logging.getLogger(__name__)

class BaseScraper(ABC):

    DEFAULT_HEADERS = {"User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
        }
    REQUEST_TIMEOUT = 60
    RETRY_STATUS_CODES = [429, 500, 502, 503, 504]

    def __init__(self, urls: List[str]):
        self.urls = urls
        self.session = self._create_session()
        self.scrap_key = os.getenv("SCRAPE_TOKEN")
        self.render = "true"
        self.geo_code = "fr"
        self.super_mode = "true"


    #SESSIONS
    def _create_session(self) -> requests.Session:
        session = requests.Session()

        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=self.RETRY_STATUS_CODES, allowed_methods=["GET"])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session
    
    #REQUEST
    def get_soup(self, url:str) -> Optional[BeautifulSoup]:

        try:
            reponse = self.session.get(url, headers=self.DEFAULT_HEADERS, timeout=self.REQUEST_TIMEOUT)
            reponse.raise_for_status()
            return BeautifulSoup(reponse.text, 'html.parser')
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {e}")

        except Exception as e:
            logger.exception(f"Unexpected error for {url}: {e}")

        return None

    def safe_get_text(self, element, default=None):
        if element:
            return element.get_text()
        else:
            return default
        
    #CREATE JSON
    def save_to_json(self, data: List[Dict], filename: str):
        json_content = json.dumps(data, ensure_ascii=False, indent=4)
        return json_content


    @abstractmethod

    def fetch(self, url:str) -> Dict:
        pass

    def run(self) -> List[Dict]:
        results = []

        for url in self.urls:

            try:

                data = self.fetch(url)

                if data:
                    results.append(data)

            except Exception as e:
                logger.exception(f"Error fetching data from {url}: {e}")



        return results