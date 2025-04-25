import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Asegúrate de tener chromedriver.exe en la misma carpeta
service = Service("chromedriver.exe")

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

# Crear carpetas necesarias
os.makedirs('screenshots', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Iniciar el navegador
driver = webdriver.Chrome(service=service, options=options)

# Paso 1: Entrar a MercadoLibre
driver.get("https://www.mercadolibre.com")
time.sleep(4)
driver.save_screenshot('screenshots/01_home.png')


# Paso 2: Seleccionar México
try:
    mexico_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='mercadolibre.com.mx']"))
    )
    mexico_button.click()
    time.sleep(4)
except Exception as e:
    print("🔎 México ya seleccionado o no fue necesario:", e)
driver.save_screenshot('screenshots/02_mexico_selected.png')


# clic MAs tarde ubi

try:
    # Esperar hasta que el banner esté presente y luego cerrarlo si es visible
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "andes-button__content"))
    )
    close_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Más tarde')]")
    close_btn.click()
    time.sleep(1)  # Esperar un momento para que desaparezca
except:
    pass  # Si no aparece el banner, continuar normalmente


#Aceptar cookis  o no

try:
    # Esperar hasta que el banner esté presente y luego cerrarlo si es visible
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cookie-consent-banner-opt-out__container"))
    )
    close_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Aceptar') or contains(text(), 'Cerrar')]")
    close_btn.click()
    time.sleep(1)  # Esperar un momento para que desaparezca
except:
    pass  # Si no aparece el banner, continuar normalmente



# Paso 3: Buscar "playstation 5"
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "as_word"))
)
search_box.send_keys("playstation 5")
search_box.send_keys(Keys.RETURN)
time.sleep(4)
driver.save_screenshot('screenshots/03_search_playstation5.png')

# Paso 4: Filtro por "Nuevo"
try:
    nuevo_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ui-search-filter-name') and contains(text(), 'Nuevo')]/ancestor::a"))
)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nuevo_link)
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable(nuevo_link)).click()

    time.sleep(4)
    driver.save_screenshot('screenshots/04_filter_new.png')
except Exception as e:
    print("❌ No se pudo aplicar filtro de 'Nuevo':", e)

# Paso 5: Filtro por ubicación "CDMX"
try:
    cdmx_option =WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ui-search-filter-name') and contains(text(), 'Estado De México')]/ancestor::a"))
)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cdmx_option)
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable(cdmx_option)).click()
    time.sleep(2)
    time.sleep(4)
    driver.save_screenshot('screenshots/05_filter_cdmx.png')
except Exception as e:
    print("❌ No se pudo aplicar filtro de 'CDMX':", e)

# Paso 6: Ordenar por "Mayor precio"
try:
    sort_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'andes-visually-hidden') and contains(text(), 'Más relevantes')]/ancestor::button"))
    )
    sort_dropdown.click()
    time.sleep(2)
    high_price_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Mayor precio']/ancestor::div[contains(@class, 'andes-list__item-text')]"))
    )
    high_price_option.click()
    time.sleep(4)
    driver.save_screenshot('screenshots/06_sorted_by_high_price.png')

except Exception as e:
    print("❌ No se pudo ordenar por mayor precio:", e)

try:
    scroll_product23 =WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, ".//a[contains(text(), 'Consola Sony Playstation 5 Pro Digital 2 Tb Blanco')]"))
)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",scroll_product23)
    time.sleep(5)
    driver.save_screenshot('screenshots/07_sorted_by_high_products.png')

    scroll_product45 =WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, ".//a[contains(text(), 'Consola Sony Playstation 5 Digital Edición 30º Aniversario 1 TB Gris')]"))
)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",scroll_product45)
    time.sleep(5)
    driver.save_screenshot('screenshots/08_sorted_by_high_products.png')

except Exception as e:
    print("❌ No se pudo hacer scroll:", e)

# Paso 7: Extraer nombre y precio de los primeros 5 productos
product_list = []
try:
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-layout__item"))
    )
    for product in products[:5]:
        try:
            name = product.find_element(By.CSS_SELECTOR, "h3.poly-component__title-wrapper > a.poly-component__title").text
            price = product.find_element(By.XPATH, ".//span[not(ancestor::s)]/span[@class='andes-money-amount__fraction']").text
            product_list.append({'Nombre': name, 'Precio': price})
        except Exception as e:
            print("⚠️ Error al extraer producto:", e)
except Exception as e:
    print("❌ No se encontraron productos:", e)

# Mostrar productos en consola
print("\n📦 Productos encontrados:")
for idx, item in enumerate(product_list, 1):
    print(f"{idx}. {item['Nombre']} - ${item['Precio']} MXN")

# Guardar en CSV
df = pd.DataFrame(product_list)
df.to_csv('output/results.csv', index=False)

# Cerrar navegador
driver.quit()
