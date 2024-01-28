from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

url = "https://www.euro.com.pl/miksery.bhtml"

# Use a headless browser for automated scraping
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

total_products = [0]

def scrape_page(page_source, total_products):
    soup = BeautifulSoup(page_source, 'html.parser')
    product_containers = soup.find_all('ems-euro-mobile-product-medium-box')

    for product_container in product_containers:
        product_name = product_container.find('a', class_='box-medium__link').text.strip()
        product_price_element = product_container.find('span', class_='price-template__large--total')

        if product_price_element:
            product_price = product_price_element.text.strip()
        else:
            product_price = 'Price not available'

        product_photo = product_container.find('img')['src']
        product_link = 'https://www.euro.com.pl' + product_container.find('a', class_='box-medium__link')['href']

        print(f"Product Name: {product_name}")
        print(f"Product Price: {product_price}")
        print(f"Product Photo: {product_photo}")
        print(f"Product Link: {product_link}")
        print("\n")

    total_products[0] += len(product_containers)

# Open the initial page
driver.get(url)

# Click the "ZAAKCEPTUJ" button if it exists
try:
    accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    accept_button.click()
except Exception as e:
    print(f"Failed to click 'ZAAKCEPTUJ' button: {e}")

# Wait for the dark filter to disappear
# WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'onetrust-pc-dark-filter')))

# Simulate scrolling to load additional content
body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(3):  # You may need to adjust the number of scrolls based on the website
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)  # Wait for the content to load

# Get the updated page source after scrolling
page_source = driver.page_source
# scrape_page(page_source, total_products)

# Check for and click the "Load More" button until it's no longer available
while True:
    try:
        load_more_button = driver.find_element(By.XPATH, '//a[contains(@class, "list-load-more__button")]')  # Adjust based on the actual class of the button
        ActionChains(driver).move_to_element(load_more_button).click().perform()
        time.sleep(0.5)  # Wait for the content to load
    except Exception as e:
        print(f"No more 'Load More' buttons found. Exiting.")
        break

page_source = driver.page_source
scrape_page(page_source, total_products)
driver.quit()
print(f"Total products: {total_products[0]}")