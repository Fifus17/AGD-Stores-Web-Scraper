from abc import ABC, abstractmethod
from selenium import webdriver
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
        options = webdriver.ChromeOptions()
        options.headless = True
        return webdriver.Chrome(options=options)

    def close_driver(self):
        self.driver.quit()
