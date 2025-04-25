
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os

os.makedirs('screenshots', exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.mercadolibre.com")
time.sleep(2)
driver.save_screenshot('screenshots/01_home.png')

try:
    mexico_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='mercadolibre.com.mx']"))
    )
    mexico_button.click()
except:
    pass
time.sleep(2)
driver.save_screenshot('screenshots/02_mexico_selected.png')

search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "as_word"))
)
search_box.send_keys("playstation 5")
search_box.send_keys(Keys.RETURN)
time.sleep(2)
driver.save_screenshot('screenshots/03_search_playstation5.png')

try:
    nuevo_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Nuevo')]"))
    )
    nuevo_filter.click()
except:
    pass
time.sleep(2)
driver.save_screenshot('screenshots/04_filter_new.png')

try:
    location_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Ciudad de México')]"))
    )
    location_filter.click()
except:
    pass
time.sleep(2)
driver.save_screenshot('screenshots/05_filter_cdmx.png')

try:
    sort_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "andes-dropdown__trigger"))
    )
    sort_dropdown.click()
    high_price_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@class='andes-list__item']//span[contains(text(),'Mayor precio')]"))
    )
    high_price_option.click()
except:
    pass
time.sleep(2)
driver.save_screenshot('screenshots/06_sorted_by_high_price.png')

products = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-layout__item"))
)

product_list = []
for product in products[:5]:
    try:
        name = product.find_element(By.CSS_SELECTOR, "h2.ui-search-item__title").text
        price = product.find_element(By.CSS_SELECTOR, "span.price-tag-fraction").text
        product_list.append({'Nombre': name, 'Precio': price})
    except:
        continue

for idx, item in enumerate(product_list, 1):
    print(f"{idx}. {item['Nombre']} - ${item['Precio']} MXN")

df = pd.DataFrame(product_list)
os.makedirs('output', exist_ok=True)
df.to_csv('output/results.csv', index=False)
driver.quit()
