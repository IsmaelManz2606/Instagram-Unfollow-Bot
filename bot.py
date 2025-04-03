from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import time
import os

# Cargar variables del archivo .env
load_dotenv()
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# Configurar opciones del navegador para usar tu perfil de Chrome
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/USUARIOPERSONAL/AppData/Local/Google/Chrome/User Data/Profile 1")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# --------------------
# Opcional: Cookies e inicio de sesión (descomentar si es necesario)
# --------------------
# try:
#     reject_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Rechazar')]")))
#     reject_btn.click()
#     print("✅ Cookies rechazadas")
#     time.sleep(2)
# except:
#     print("ℹ️ No apareció el botón de rechazar cookies")
#
# try:
#     user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
#     user_input.send_keys(USERNAME)
#     pass_input = driver.find_element(By.NAME, "password")
#     pass_input.send_keys(PASSWORD)
#     login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
#     login_btn.click()
#     print("✅ Login enviado")
# except Exception as e:
#     print("❌ Error en el login:", e)
#
# --------------------

profile_url = f"https://www.instagram.com/{USERNAME}/"
processed = set()

def get_new_accounts():
    new_urls = set()
    try:
        following_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following')]")))
        following_link.click()
        print("✅ Modal de 'Siguiendo' abierto")
        time.sleep(2)
    except Exception as e:
        print("❌ No se pudo abrir el modal de 'Siguiendo':", e)
        return new_urls

    # Buscar el contenedor scrollable
    try:
        scroll_container = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'x1rife3k')]")
        ))
        print("✅ Contenedor scrollable identificado correctamente.")
    except:
        print("❌ No se encontró el contenedor scrollable por clase. Intentando usar el modal completo.")
        try:
            scroll_container = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@role='dialog']")
            ))
        except:
            print("🚫 No se pudo encontrar ningún contenedor scrollable.")
            return new_urls

    print("⏬ Iniciando scroll dinámico hasta el final...")

    consecutive_no_change = 0
    previous_count = 0
    max_no_change = 3  # Parar después de 3 intentos sin que cambie el número de cuentas

    while consecutive_no_change < max_no_change:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
        time.sleep(2.5)

        current_count = len(scroll_container.find_elements(By.XPATH, ".//a[starts-with(@href, '/') and string-length(@href) > 1]"))

        if current_count == previous_count:
            consecutive_no_change += 1
        else:
            consecutive_no_change = 0  # Reiniciar si se cargaron más
            previous_count = current_count

    print("✅ Scroll completado. Se cargaron todas las cuentas visibles.")

    # Recoger todos los enlaces de las cuentas
    elements = scroll_container.find_elements(By.XPATH, ".//a[starts-with(@href, '/') and string-length(@href) > 1]")
    for elem in elements:
        href = elem.get_attribute("href")
        full_url = "https://www.instagram.com" + href if href.startswith("/") else href
        if full_url not in processed:
            new_urls.add(full_url)

    print(f"🔍 Se han encontrado {len(new_urls)} cuentas nuevas tras hacer scroll completo.")

    # Cerrar el modal
    try:
        close_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(@aria-label, 'Cerrar')]/ancestor::button")))
        driver.execute_script("arguments[0].click();", close_btn)
        print("✅ Modal de 'Siguiendo' cerrado")
    except Exception as e:
        print("❌ Error al cerrar el modal de 'Siguiendo':", e)

    return new_urls


def process_account(url):
    print("\nProcesando cuenta:", url)
    driver.get(url)
    time.sleep(3)

    # ✅ Comprobar si tiene más de 50.000 seguidores
    try:
        followers_span = wait.until(EC.presence_of_element_located((
            By.XPATH, "//a[contains(@href, '/followers/')]/span/span[@title]"
        )))
        followers_text = followers_span.get_attribute("title").replace(".", "").replace(",", "").strip()
        followers_count = int(followers_text)

        if followers_count >= 10000:
            print(f"🚨 Cuenta con {followers_count} seguidores. Se considera famosa. Saltando.")
            return
        else:
            print(f"👤 Cuenta con {followers_count} seguidores. Continuando proceso.")
    except Exception as e:
        print("⚠️ No se pudo obtener la cantidad de seguidores. Continuando por precaución.")

    
    # Abrir el modal de "Seguidos" del perfil de esa cuenta
    try:
        seguidos_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following/')]")))
        seguidos_link.click()
        print("✅ Modal de seguidos abierto")
        time.sleep(2)
    except Exception as e:
        print("❌ No se pudo abrir el modal de seguidos para", url, ":", e)
        return

    # Buscar la barra de búsqueda en el modal
    try:
        modal_container = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']")))
        search_input = modal_container.find_element(By.XPATH, ".//input[@aria-label='Buscar entrada']")
    except Exception as e:
        print("🚫 No se encontró la barra de búsqueda en el modal para", url, ". Se asume cuenta famosa/restringida.")
        try:
            close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@aria-label, 'Cerrar')]/ancestor::button")))
            driver.execute_script("arguments[0].click();", close_btn)
            print("✅ Modal de seguidos cerrado")
        except Exception as e_close:
            print("❌ Error al cerrar el modal:", e_close)
        return

    # Filtrar por tu username en el modal de "Seguidos"
    try:
        ActionChains(driver).move_to_element(search_input).click().perform()
        search_input.clear()
        ActionChains(driver).send_keys(USERNAME).perform()
        time.sleep(2)
        
        filtered_results = modal_container.find_elements(By.XPATH, ".//a")
        user_found = any(result.text.strip().lower() == USERNAME.lower() for result in filtered_results)
        
        if user_found:
            print("🤝 La cuenta nos sigue. No se procede a dejar de seguir.")
        else:
            print("🚫 Nuestro usuario no se encontró en los resultados filtrados. Procediendo a dejar de seguir.")
            try:
                # Pulsar el botón "Siguiendo"
                unfollow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Siguiendo')]")))
                driver.execute_script("arguments[0].scrollIntoView(true);", unfollow_btn)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", unfollow_btn)
                print("Clic en botón 'Siguiendo' realizado.")
                
                # Pulsar el elemento de confirmación "Dejar de seguir"
                confirm_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='button' and .//span[text()='Dejar de seguir']]")
                ))
                driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", confirm_btn)
                print("Clic en 'Dejar de seguir' realizado.")
                
                wait.until(lambda d: "Seguir" in d.find_element(By.XPATH, "//*[contains(@role, 'button') and contains(., 'Seguir')]").text)
                print("✅ Se ha dejado de seguir a la cuenta.")
            except Exception as unfollow_e:
                print("❌ Error al intentar dejar de seguir la cuenta:", unfollow_e)
    except Exception as search_e:
        print("❌ Error durante la búsqueda en el modal para", url, ":", search_e)
    
    # Cerrar el modal de "Seguidos"
    try:
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@aria-label, 'Cerrar')]/ancestor::button")))
        driver.execute_script("arguments[0].click();", close_btn)
        print("✅ Modal de seguidos cerrado")
    except Exception as e:
        print("❌ Error al cerrar el modal de seguidos:", e)

# Bucle externo: seguir procesando nuevas cuentas mientras haya
while True:
    driver.get(profile_url)
    time.sleep(3)
    new_urls = get_new_accounts()
    if not new_urls:
        print("No quedan cuentas nuevas por procesar. Fin del proceso.")
        break
    print("Nuevas cuentas encontradas:", len(new_urls))
    for url in new_urls:
        process_account(url)
        processed.add(url)
    # Después de procesar, volver a cargar el modal para intentar cargar más cuentas
    time.sleep(2)

driver.quit()
# Cerrar el navegador al finalizar  