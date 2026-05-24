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
    soup = BeautifulSoup(html_content, 'html.parser')
    product_title = soup.find('h1', class_='a-size-large a-spacing-none').get_text()
    product_price_whole = soup.find('span', class_='a-price-whole').get_text()
    product_price_fraction = soup.find('span', class_='a-price-fraction').get_text()
    reviews = soup.find(id='acrCustomerReviewText').get_text()[1:-1]

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "title": product_title,
        "reviews": reviews,
        "timestamp": timestamp
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
    url = "https://www.amazon.fr/Google-Pixel-9a-Smartphone-Volcanique/dp/B0DSWJDNY4/ref=sr_1_5?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3J5BV860O33QN&dib=eyJ2IjoiMSJ9.4H2mSG4tvEhB5PCCCN04OZfL7xpLawv9ofdvKpuxwUi2R5YykmV8-ue-GQCgOHCGaScwR5XcOGIrx5jcIjJsWg6wlxrhGzhvc8bdzoYQxbYx6OhdnBNocl-TT0Icg2fJMiCp5iiOSaVCIrsDidVYoYsUhcB7_j_Fbfb9l0TCxwER-kv_6sE8eNrbPRYuaUfoHi66rwfJvduCeP9vvK9_hmYt9ABQRLLxDHViSCiMHdCHYTP-rkSIXZ6NuS8shPf8Dg-RKBz_JbJGacArQeV2UwQ98e0B3xHIjrwlDggTzrc.gbsbWEb5YvxLnbvJ2TuXkTrrHk8oi66N27700KrLs6I&dib_tag=se&keywords=Google%2BPixel%2B9a&qid=1779098522&sprefix=google%2Bpixel%2B9a%2Caps%2C137&sr=8-5&th=1"
    df = pd.DataFrame()
    conn = create_connection()
    setup_database(conn)

    while True:
        html_content = get_page_content(url)
        if html_content:
            product_info = parse_content(html_content)
            save_to_db(conn, product_info)
            print("Data saved to database:", product_info)
        else:
            print("Failed to retrieve or parse the page content.")
        time.sleep(10)


