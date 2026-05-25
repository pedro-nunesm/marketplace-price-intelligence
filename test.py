from scrapers.amazon import AmazonScraper
from scrapers.base import BaseScraper
from pipeline.storage import upload_to_s3



scraper = AmazonScraper(urls=["https://www.amazon.fr/JBL-Bluetooth-dautonomie-r%C3%A9sistante-Multi-Enceintes/dp/B0DXKNBQS6/ref=sr_1_2?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3IT0AW9WBQKBK&dib=eyJ2IjoiMSJ9.3_kM8PY9WMmk3HouK4opztGFACNNcodOlFosywUnqsJ8fI7FXENgiqYDbanZK_PofUysgQ7L3X6FobCcCPxchxwgC7OpEdzZokJa2INOeyFT57BvHWmWQD0g8HWyQGIzs7ZypkGIJNwgAdAVLwuskSE4KlFJd0Qy-htHBZOtz2q8asY5BOocYS9sLCvMIwyTSJzDiSobcOtoFGR0CbgcJ1mx5R52ZQbBFgTyN6JCOWsakO2P1tYo7EbfZ_FhTIkGvLkf_8kOqLo82VDKooVN05beuRWPAqmSEGPPSafeZ3Y.l7e3isGLWX9iK_4UqTJo2NOFxGM3wkvKPGA908GUYvY&dib_tag=se&keywords=JBL%2BCharge%2B6&qid=1779096571&sprefix=jbl%2Bcharge%2B%2Caps%2C149&sr=8-2&ufe=app_do%3Aamzn1.fos.9ad51ef1-4f85-497e-abf8-79138a00c9e5&th=1",
                              "https://www.amazon.fr/Samsung-Gaming-Odyssey-3440x2160-1000000/dp/B0D3FF5QL2/ref=sr_1_5?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=SHNT2FAP6GHW&dib=eyJ2IjoiMSJ9.1Rinz2wi3seUj9EdfYHaayRGNM8uHDA1en1yTOCm0EZ_LIWkMR-5lcfyEXJ8WbUfPBmvl5aYsYBG6jUyfBdECw0JfShlW9kRDpKepCjcgmjTUsxBPyjIbP1lJf6RfGlLyN6UHz8UVcKpryVlynMJOkECLeO7_wy-8HFH253i8AmnM3Y70tVGi1cznawsZtqlPYPkwDzZ6hxWjZ2HK7NQtbmq8boVJFePw5NvRTIgUID0cZIhiefDSFi12KKIxv1qCSJQPNntydTVNTJ1NQzenTEa075-9Qq2rnjZRN4HMek.SrpgbfbCp6-EHmDUOdyRkC44unjcePFj8TBN37alO44&dib_tag=se&keywords=Samsung+Odyssey+G8&qid=1779097055&sprefix=samsung+odyssey+g%2Caps%2C152&sr=8-5&ufe=app_do%3Aamzn1.fos.49fccda8-a887-4188-817b-b9a64bb30e43",
                              "https://www.amazon.fr/Samsung-Interne-Vitesse-bureautique-MZ-V9S4T0BW/dp/B0DGH2FH7T/ref=sr_1_2_sspa?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1RYQC6XVN12MI&dib=eyJ2IjoiMSJ9.m_F6IfSLfePENZNshBXhbgEgWb5OWaHPTF8BBfnd-PgxlcyVP8MZ_n2Q7kQR-xRrUbkeZi8Q0rj9kyfreXeA-vaFIgvDkDK8WJLoFKz9lTqYNHINqMNb_7J5alr21tF1wOJS96Lfv2zWHmkGza7bXpng7iMCuM_yc5rWsSWrs9bJS3-hiz5HF0KV0oQRR-lUw7rDIlBe6b7Lu-gRgmqJylf42P0AEb4W8NBsRiDpPjh9wFrPFxMa7daCiYMDWvwmqiMjr_9nevcg-YlRCGhqJXf6K157E6NqbQNem1pLtMQ.r1CtT7r1IhdQdRVT7vbuqZ8tk-Ike4Q5daE4qKOekh4&dib_tag=se&keywords=Samsung%2B990%2BPlus%2B1tb&qid=1779097382&sprefix=samsung%2B990%2Bplus%2B1tb%2Caps%2C170&sr=8-2-spons&ufe=app_do%3Aamzn1.fos.49fccda8-a887-4188-817b-b9a64bb30e43&aref=Ht28WNl5sI&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"])
produtos = scraper.run()
json = scraper.save_to_json(produtos, "products.json")
upload_to_s3(json, "price-intelligence-storage", "products.json")




