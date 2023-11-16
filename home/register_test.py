from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

import traceback

# Path al driver de chrome
chromedriver_path = 'bug_report/chromedriver-win64/chromedriver.exe'

# Se crean las opciones para el ejecutable
chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_service = Service(chromedriver_path)

# Se configura el driver del navegador
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Realizar pruebas
try:
    # Abrir la página web
    driver.get('http://127.0.0.1:8000/signup')

    # Encontrar las entradas
    username_input = driver.find_element(By.NAME, 'username')
    password1_input = driver.find_element(By.NAME, 'password1')
    password2_input = driver.find_element(By.NAME, 'password2')
    email_input = driver.find_element(By.NAME, 'email')
    submit_button = driver.find_element(By.CSS_SELECTOR, '.button[type="submit"]')

    # Ingresar datos de prueba
    username_input.send_keys('testuser2')
    password1_input.send_keys('testpassword')
    password2_input.send_keys('testpassword')
    email_input.send_keys('test@example.com')

    # Enviar el formulario
    submit_button.click()
    # Esperar 2 segundos para que se procese
    time.sleep(2)

    # Verificar si la página después de enviar el formulario contiene 'Iniciar sesión'
    assert 'Iniciar sesión' in driver.page_source

# Manejar excepciones
except Exception as e:
    print(f'Error: {str(e)}')
    traceback.print_exc()

# Cerrar el navegador al finalizar
driver.quit()
