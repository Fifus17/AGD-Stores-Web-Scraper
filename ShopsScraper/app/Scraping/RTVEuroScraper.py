from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

from .Scraper import Scraper

class RTVEuroScraper(Scraper):
    def __init__(self):
        super().__init__("https://www.euro.com.pl/")

    def get_url(self, phrase):
        self.driver.get(self.url)

        # accept cookies
        try:
            accept_button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            accept_button.click()
        except Exception as e:
            print(f"Failed to click 'ZAAKCEPTUJ' button: {e}")

        # Locate the search input field and enter the search phrase
        search_input = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'text-input__input')
            )
        )

        search_input.send_keys(phrase)

        # Locate and click the search button
        search_button = self.driver.find_element("css selector", 'button[class="search-container__search-button reference"]')
        search_button.click()

        time.sleep(0.5)

        # Return the current URL after performing the search
        return self.driver.current_url
    
    def load_page(self, url):
        self.driver.get(url)

        # accept cookies
        try:
            accept_button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            accept_button.click()
        except Exception as e:
            print(f"Failed to click 'ZAAKCEPTUJ' button: {e}")

        # Simulate scrolling to load additional content
        body = self.driver.find_element(By.TAG_NAME, 'body')
        for _ in range(3):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        while True:
            try:
                load_more_button = self.driver.find_element(By.XPATH, '//a[contains(@class, "list-load-more__button")]')  # Adjust based on the actual class of the button
                ActionChains(self.driver).move_to_element(load_more_button).click().perform()
                time.sleep(0.5)  # Wait for the content to load
            except Exception as e:
                print(f"No more 'Load More' buttons found. Exiting.")
                break

        return self.get_items(self.driver.page_source)
    

    def get_items(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        product_containers = soup.find_all('ems-euro-mobile-product-medium-box')

        items = []

        for product_container in product_containers:
            product_name = product_container.find('a', class_='box-medium__link').text.strip()
            product_price_element = product_container.find('span', class_='price-template__large--total')

            if product_price_element:
                product_price = product_price_element.text.strip()
            else:
                product_price = 'Price not available'

            product_photo = product_container.find('img')['src']
            product_link = 'https://www.euro.com.pl' + product_container.find('a', class_='box-medium__link')['href']
            product_avg_review = product_container.find('span', class_='client-rate__rate').text.strip() if product_container.find('span', class_='client-rate__rate') else 'No reviews'

            items.append({
                'name': product_name,
                'price': product_price,
                'photo': product_photo,
                'link': product_link,
                'review': product_avg_review,
                'shop': "https://www.euro.com.pl/static-assets/logo.webp"
            })

        print(items)
        return items