import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import pandas as pd

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None



def parse_content(html_content):
    #values can be missing, so we need to handle that with try-except or conditional checks
    soup = BeautifulSoup(html_content, 'html.parser')
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

def save_to_db(connection, data):
    new_row = pd.DataFrame([data])
    new_row.to_sql('products', connection, if_exists='append', index=False)


def create_connection(db_name="products.db"):
    connection = sqlite3.connect(db_name)
    return connection

def setup_database(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            title TEXT,
            reviews INTEGER,
            timestamp TEXT
        )
    ''')
    connection.commit()

if __name__ == "__main__":
    url = "https://www.amazon.fr/JBL-Bluetooth-dautonomie-r%C3%A9sistante-Multi-Enceintes/dp/B0DXKNBQS6/ref=sr_1_2?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3IT0AW9WBQKBK&dib=eyJ2IjoiMSJ9.3_kM8PY9WMmk3HouK4opztGFACNNcodOlFosywUnqsJ8fI7FXENgiqYDbanZK_PofUysgQ7L3X6FobCcCPxchxwgC7OpEdzZokJa2INOeyFT57BvHWmWQD0g8HWyQGIzs7ZypkGIJNwgAdAVLwuskSE4KlFJd0Qy-htHBZOtz2q8asY5BOocYS9sLCvMIwyTSJzDiSobcOtoFGR0CbgcJ1mx5R52ZQbBFgTyN6JCOWsakO2P1tYo7EbfZ_FhTIkGvLkf_8kOqLo82VDKooVN05beuRWPAqmSEGPPSafeZ3Y.l7e3isGLWX9iK_4UqTJo2NOFxGM3wkvKPGA908GUYvY&dib_tag=se&keywords=JBL%2BCharge%2B6&qid=1779096571&sprefix=jbl%2Bcharge%2B%2Caps%2C149&sr=8-2&ufe=app_do%3Aamzn1.fos.9ad51ef1-4f85-497e-abf8-79138a00c9e5&th=1"
    df = pd.DataFrame()
    #conn = create_connection()
    #setup_database(conn)

    while True:
        html_content = get_page_content(url)
        if html_content:
            product_info = parse_content(html_content)
            print(product_info)
        else:
            print("Failed to retrieve or parse the page content.")
        time.sleep(10)


