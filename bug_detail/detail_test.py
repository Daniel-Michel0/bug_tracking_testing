from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

""" 

    US: 
    Como usuario quiero que se muestre el estado de mi reporte para visualizar su proceso.

    Criterios de aceptación:
    - En la vista del usuario registrado se muestra la lista de reportes creados por él, 
    donde se puede acceder al detalle de un bug en caso de que ya haya sido asignado haciendo 
    click en él.
    - En la vista del detalle del bug se puede ver el estado del bug junto a otro detalles

    Precondiciones:
    - El usuario debe estar registrado
    - El usuario debe haber creado un reporte
    - El reporte ya debe estar asignado un bug

    Pasos:
    1. El usuario inicia sesión
    2. El usuario desde la vista principal hace click en el reporte que desea ver
    3. El usuario es redirigido a la vista de detalle del reporte
    4. El usuario verifica que el reporte sea el que el envió
    5. El usuario verifica que el estado del reporte sea 'En proceso'

"""

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

    # Esperar a que el elemento sea visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'username')))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.button[type="submit"]')))

    # Insertar la data de prueba
    username_input.send_keys('testadmin')
    password_input.send_keys('adminpass123')

    # Enviar el formulario
    submit_button.click()

    # Esperar hasta que el elemento contenga el string 'Bienvenido'
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, 'welcome-message'),'Bienvenido Testadmin'))

    # Esperar hasta que el elemento contenga el string 'Tus reportes enviados'
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, 'title-report-table'),'Tus reportes enviados'))

    #Esperar 2 segundos para procesar
    time.sleep(2)

    # Hacer click en el primer reporte de la tabla con id 'report-table' y guardar el id del reporte, con el titulo
    report_id = driver.find_element(By.CSS_SELECTOR, '#report-table > tbody > tr:nth-child(1) > td:nth-child(1)').text
    report_title = driver.find_element(By.CSS_SELECTOR, '#report-table > tbody > tr:nth-child(1) > td:nth-child(2)').text
    driver.find_element(By.CSS_SELECTOR, '#report-table > tbody > tr:nth-child(1)').click()

    # Esperar hasta que la clase reporte container sea visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'ticket-table')))

    #print('Pagina de detalle encontrada')

    # Revisar que el id y el titulo del reporte se encuentren en la tabla de tickets de la página
    assert report_id in driver.page_source
    assert report_title in driver.page_source

    # Encontrar los elementos span bajo la clase 'id-fecha' y obtener sus textos
    subido_por_elements = driver.find_elements(By.CSS_SELECTOR, '.id-fecha .text-2.subido + .text-usuario')

    # Revisar que el ticket subido sea el que subio el usuario
    assert subido_por_elements[0].text in driver.page_source

    # Revisar que el estado del reporte sea 'En proceso'
    assert 'En proceso' in driver.page_source

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # fin test

except Exception as e:
    print(f'Error: {str(e)}')

finally:
    driver.quit()

