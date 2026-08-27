import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from scrapers.amazon import AmazonScraper
from scrapers.fnac import FnacScraper
from scrapers.mediamarkt import MediaMarktScraper
from pipeline.storage import upload_to_s3

import requests
import logging

load_dotenv() 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) 

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def process_scrapper(scraper_name: str, scraper_instance, date_folder: str):
    #Execute the scraper and load the data to S3
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    try:
        logger.info(f"Starting {scraper_name} scraper...")
        data = scraper_instance.run()

        if not data:
            raise ValueError(f"No data returned from {scraper_name} scraper.")

        json_content = scraper_instance.save_to_json(data, f"temp_{scraper_name}.json")
        s3_key = f"{date_folder}/{scraper_name}_{current_time}.json"
        upload_to_s3(json_content, BUCKET_NAME, s3_key)

        logger.info(f"{scraper_name} scraper completed successfully. Data uploaded to S3 at {s3_key}.")

    except Exception as e:
        logger.error(f"Error in {scraper_name} scraper: {e}")

        #Save the error to S3
        error_data = {"error": str(e), "scraper": scraper_name, "timestamp": current_time}
        error_content = json.dumps(error_data, ensure_ascii=False, indent=4)
        error_key = f"{date_folder}/ERROR_{scraper_name}_{current_time}.json"

        upload_to_s3(error_content, BUCKET_NAME, error_key)
        logger.info(f"Error details uploaded to S3 at {error_key}.")


scrapers = {
    "Amazon": AmazonScraper(urls=["https://www.amazon.fr/Google-Pixel-9a-Smartphone-Volcanique/dp/B0DSWJDNY4/ref=sr_1_5?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3J5BV860O33QN&dib=eyJ2IjoiMSJ9.4H2mSG4tvEhB5PCCCN04OZfL7xpLawv9ofdvKpuxwUi2R5YykmV8-ue-GQCgOHCGaScwR5XcOGIrx5jcIjJsWg6wlxrhGzhvc8bdzoYQxbYx6OhdnBNocl-TT0Icg2fJMiCp5iiOSaVCIrsDidVYoYsUhcB7_j_Fbfb9l0TCxwER-kv_6sE8eNrbPRYuaUfoHi66rwfJvduCeP9vvK9_hmYt9ABQRLLxDHViSCiMHdCHYTP-rkSIXZ6NuS8shPf8Dg-RKBz_JbJGacArQeV2UwQ98e0B3xHIjrwlDggTzrc.gbsbWEb5YvxLnbvJ2TuXkTrrHk8oi66N27700KrLs6I&dib_tag=se&keywords=Google%2BPixel%2B9a&qid=1779098522&sprefix=google%2Bpixel%2B9a%2Caps%2C137&sr=8-5&th=1",
                                  "https://www.amazon.fr/NINTENDO-Switch-Console-Portables-Tactile/dp/B098TVDYZ3/ref=sr_1_2?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1PKQWYKU6I1UO&dib=eyJ2IjoiMSJ9.WYGeypF_CCvkyvDSiZZOiRVZ0N0TLmgkEmv_7xkOe9hIVpDSE6Q7KfaqpFQ_QGYnjCX99ZNMNClDfZZQjKQhkoMhAIEsFLLBKGQSdvnCYdcrud8j2QPD3YFCq0vzC3JDRTJbBycapzIoSbt7j3Cwnt4_YN1Z6fw0GhTTEVUAjY91ZMfMPG4GBQX_sk675Y5rGCUwcmRfZddHMMfX5gvvNY-ggYS01zEcGAuw__CfLQ7mbd9gKvXrqqKAR64VOho16XNxsmxMiZ0GL-eXPGjHF79YV9M6TSBkpe3CeJQeEkI.Q9usFQ5XiCEI3FGtOmmVbD68IY_Bc7nIREj7rTk8Dks&dib_tag=se&keywords=Nintendo+Switch+OLED&qid=1779098813&sprefix=google+pixel+9a%2Caps%2C248&sr=8-2"]),
    "Fnac": FnacScraper(urls=["https://www.fnac.com/Ecran-PC-gaming-Samsung-Odyssey-G80SD-32-4K-UHD-Argent/a20611346/w-4",
    "https://www.fnac.com/Apple-AirPods-Pro-3-Blanc/a18241004/w-4"])
}

for scraper_name, scraper_instance in scrapers.items():
    date_folder = datetime.now().strftime("%Y-%m-%d")
    process_scrapper(scraper_name, scraper_instance, date_folder)