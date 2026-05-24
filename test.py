from scrapers.amazon import AmazonScraper
from scrapers.base import BaseScraper



scraper = AmazonScraper(urls=["https://www.amazon.fr/JBL-Bluetooth-dautonomie-r%C3%A9sistante-Multi-Enceintes/dp/B0DXKNBQS6/ref=sr_1_2?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3IT0AW9WBQKBK&dib=eyJ2IjoiMSJ9.3_kM8PY9WMmk3HouK4opztGFACNNcodOlFosywUnqsJ8fI7FXENgiqYDbanZK_PofUysgQ7L3X6FobCcCPxchxwgC7OpEdzZokJa2INOeyFT57BvHWmWQD0g8HWyQGIzs7ZypkGIJNwgAdAVLwuskSE4KlFJd0Qy-htHBZOtz2q8asY5BOocYS9sLCvMIwyTSJzDiSobcOtoFGR0CbgcJ1mx5R52ZQbBFgTyN6JCOWsakO2P1tYo7EbfZ_FhTIkGvLkf_8kOqLo82VDKooVN05beuRWPAqmSEGPPSafeZ3Y.l7e3isGLWX9iK_4UqTJo2NOFxGM3wkvKPGA908GUYvY&dib_tag=se&keywords=JBL%2BCharge%2B6&qid=1779096571&sprefix=jbl%2Bcharge%2B%2Caps%2C149&sr=8-2&ufe=app_do%3Aamzn1.fos.9ad51ef1-4f85-497e-abf8-79138a00c9e5&th=1"])
produtos = scraper.fetch(url="https://www.amazon.fr/JBL-Bluetooth-dautonomie-r%C3%A9sistante-Multi-Enceintes/dp/B0DXKNBQS6/ref=sr_1_2?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3IT0AW9WBQKBK&dib=eyJ2IjoiMSJ9.3_kM8PY9WMmk3HouK4opztGFACNNcodOlFosywUnqsJ8fI7FXENgiqYDbanZK_PofUysgQ7L3X6FobCcCPxchxwgC7OpEdzZokJa2INOeyFT57BvHWmWQD0g8HWyQGIzs7ZypkGIJNwgAdAVLwuskSE4KlFJd0Qy-htHBZOtz2q8asY5BOocYS9sLCvMIwyTSJzDiSobcOtoFGR0CbgcJ1mx5R52ZQbBFgTyN6JCOWsakO2P1tYo7EbfZ_FhTIkGvLkf_8kOqLo82VDKooVN05beuRWPAqmSEGPPSafeZ3Y.l7e3isGLWX9iK_4UqTJo2NOFxGM3wkvKPGA908GUYvY&dib_tag=se&keywords=JBL%2BCharge%2B6&qid=1779096571&sprefix=jbl%2Bcharge%2B%2Caps%2C149&sr=8-2&ufe=app_do%3Aamzn1.fos.9ad51ef1-4f85-497e-abf8-79138a00c9e5&th=1")




