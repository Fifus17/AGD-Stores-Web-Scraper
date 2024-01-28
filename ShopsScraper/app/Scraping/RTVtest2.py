from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def search_on_euro(url, search_phrase):
    # Set up the Chrome driver
    driver = webdriver.Chrome()

    try:
        # Open the website
        driver.get(url)

        try:
            accept_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            accept_button.click()
        except Exception as e:
            print(f"Failed to click 'ZAAKCEPTUJ' button: {e}")

        # Locate the search input field and enter the search phrase
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'text-input__input')
            )
        )

        search_input.send_keys(search_phrase)

        # Locate and click the search button
        search_button = driver.find_element("css selector", 'button[class="search-container__search-button reference"]')
        search_button.click()

        # Wait for a moment to allow the page to load
        time.sleep(2)

        # Return the current URL after performing the search
        return driver.current_url

    finally:
        # Close the browser window
        driver.quit()

# Example usage
search_url = "https://www.euro.com.pl"
search_result_url = search_on_euro(search_url, "suszarka")
print("Search result URL:", search_result_url)
