from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

#* Tests
try:
    # Abrir la página web
    driver.get('http://127.0.0.1:8000/login')

    # Encontrar las entradas
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.CSS_SELECTOR, '.button[type="submit"]')

    # Insertar la data de prueba
    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')

    # Enviar el formulario
    submit_button.click()
    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Verificar si la siguiente página tiene el string 'Bienvenido'
    assert 'Bienvenido' in driver.page_source

    #* Tests para enviar reporte de bug

    # Abrir la página web (ya logeados)
    driver.get('http://127.0.0.1:8000/report')

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Encontrar las entradas
    report_title_input = driver.find_element(By.NAME, 'titulo')
    report_description_input = driver.find_element(By.NAME, 'reporte')
    submit_report_button = driver.find_element(By.ID, 'submitButton')
    # Find the 'Proyecto asociado' dropdown
    project_dropdown = Select(driver.find_element(By.NAME, 'nombre_proyecto'))

    # Select the 'test' option
    project_dropdown.select_by_visible_text('test')

    # Insertar la data
    report_title_input.send_keys('Reporte de prueba')
    report_description_input.send_keys('Este es un reporte de prueba.')

    # Enviar el formulario
    submit_report_button.click()

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Verificar que se encuentre el string 'Reporte enviado'
    assert 'Reporte enviado' in driver.page_source

# Manejar errores
except Exception as e:
    print(f'Error: {str(e)}')
    traceback.print_exc()

# Cerrar el navegador
driver.quit()