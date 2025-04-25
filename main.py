import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración inicial del navegador
CHROMEDRIVER_PATH = "chromedriver.exe"
BASE_URL = "https://www.mercadolibre.com"

# Crear carpetas necesarias
os.makedirs('screenshots', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Inicializar el navegador
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

def take_screenshot(filename):
    driver.save_screenshot(f'screenshots/{filename}')

def safe_click(xpath, delay=1):
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()
        time.sleep(delay)
    except Exception as e:
        print(f"⚠️ No se pudo hacer clic en el elemento: {xpath}\n{e}")

def close_banner(xpath):
    try:
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        close_btn.click()
        time.sleep(1)
    except:
        pass

def main():
    # Paso 1: Entrar a MercadoLibre
    driver.get(BASE_URL)
    time.sleep(4)
    take_screenshot('01_home.png')

    # Paso 2: Seleccionar México
    try:
        mexico_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='mercadolibre.com.mx']")))
        mexico_button.click()
        time.sleep(4)
    except Exception as e:
        print("🔎 México ya seleccionado o no fue necesario:", e)
    take_screenshot('02_mexico_selected.png')

    # Cerrar banner de ubicación
    close_banner("//span[contains(text(),'Más tarde')]")

    # Cerrar cookies
    close_banner("//button[contains(text(), 'Aceptar') or contains(text(), 'Cerrar')]")

    # Paso 3: Buscar producto
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
    search_box.send_keys("playstation 5")
    search_box.send_keys(Keys.RETURN)
    time.sleep(4)
    take_screenshot('03_search_playstation5.png')

    # Paso 4: Filtro por "Nuevo"
    safe_click("//span[contains(@class, 'ui-search-filter-name') and contains(text(), 'Nuevo')]/ancestor::a")
    take_screenshot('04_filter_new.png')

    # Paso 5: Filtro por ubicación "Estado De México"
    safe_click("//span[contains(@class, 'ui-search-filter-name') and contains(text(), 'Estado De México')]/ancestor::a")
    take_screenshot('05_filter_cdmx.png')

    # Paso 6: Ordenar por "Mayor precio"
    try:
        sort_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'andes-visually-hidden') and contains(text(), 'Más relevantes')]/ancestor::button")))
        sort_dropdown.click()
        time.sleep(2)
        high_price_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Mayor precio']/ancestor::div[contains(@class, 'andes-list__item-text')]")))
        high_price_option.click()
        time.sleep(4)
        take_screenshot('06_sorted_by_high_price.png')
    except Exception as e:
        print("❌ No se pudo ordenar por mayor precio:", e)

    # Paso 6b: Hacer scroll hasta productos visibles
    try:
        for product_name, screenshot in [
            ("Consola Sony Playstation 5 Pro Digital 2 Tb Blanco", '07_sorted_by_high_products.png'),
            ("Consola Sony Playstation 5 Digital Edición 30º Aniversario 1 TB Gris", '08_sorted_by_high_products.png')
        ]:
            scroll_product = wait.until(
                EC.presence_of_element_located((By.XPATH, f".//a[contains(text(), '{product_name}')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", scroll_product)
            time.sleep(3)
            take_screenshot(screenshot)
    except Exception as e:
        print("❌ No se pudo hacer scroll:", e)

    # Paso 7: Extraer nombre y precio de los primeros 5 productos
    product_list = []
    try:
        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-layout__item")))
        for product in products[:5]:
            try:
                name = product.find_element(By.CSS_SELECTOR, "h3.poly-component__title-wrapper > a.poly-component__title").text
                price = product.find_element(By.XPATH, ".//span[not(ancestor::s)]/span[@class='andes-money-amount__fraction']").text
                product_list.append({'Nombre': name, 'Precio': price})
            except Exception as e:
                print("⚠️ Error al extraer producto:", e)
    except Exception as e:
        print("❌ No se encontraron productos:", e)

    # Mostrar y guardar resultados
    print("\n📦 Productos encontrados:")
    for idx, item in enumerate(product_list, 1):
        print(f"{idx}. {item['Nombre']} - ${item['Precio']} MXN")

    df = pd.DataFrame(product_list)
    df.to_csv('output/results.csv', index=False)

    # Cerrar navegador
    driver.quit()

if __name__ == "__main__":
    main()
