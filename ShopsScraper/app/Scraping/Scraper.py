from abc import ABC, abstractmethod
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading

class Scraper(ABC):
    def __init__(self, url):
        self.url = url
        self.driver = self.setup_driver()
        self.items = None
        self.result = None

    def scrape(self, phrase):
        thread = threading.Thread(target=self._scrape, args=(phrase,))
        thread.start()
        thread.join()
        return self.result

    def _scrape(self, phrase):
        try:
            url = self.get_url(phrase)
        finally:
            try:
                self.result = self.load_page(url)
            finally:
                self.close_driver()

    @abstractmethod
    def get_url(self, phrase):
        pass
    
    @abstractmethod
    def load_page(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    def setup_driver(self):
        options = Options()
        # options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
        # options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    def close_driver(self):
        self.driver.quit()
