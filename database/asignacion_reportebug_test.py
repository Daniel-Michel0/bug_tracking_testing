from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
import traceback
import time

# US:
# Como administrador del sistema quiero poder asignar reportes de bugs a casos de bugs existentes y cambiar su estado para evitar la duplicación de bugs.

# Path al driver de chrome
chromedriver_path = 'bug_report/chromedriver-win64/chromedriver.exe'

# Se crean las opciones para el ejecutable
chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_service = Service(chromedriver_path)

# Se configura el driver del navegador
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Función para esperar hasta que un elemento sea visible
def wait_for_element(driver, by, value):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, value)))

#* Pruebas de aceptación
try:
    # Abrir la página web
    driver.get('http://127.0.0.1:8000/admin')

    # Iniciar sesión como administrador 
     # Encontrar las entradas de inicio de sesión
    username_input = wait_for_element(driver, By.NAME, 'username')
    password_input = wait_for_element(driver, By.NAME, 'password')
    submit_button = wait_for_element(driver, By.CSS_SELECTOR, 'input[type="submit"]')

    # Insertar las credenciales de prueba
    username_input.send_keys('admin')  # Cambiar a tu usuario administrador
    password_input.send_keys('admin')  # Cambiar a tu contraseña administrador

    # Enviar el formulario
    submit_button.click()
    time.sleep(2)

    # Ir a la página de reportes de bugs
    driver.get('http://127.0.0.1:8000/admin/database/reportebug/')

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Encontrar el primer reporte de bug y hacer clic en él
    reporte_bug_link = wait_for_element(driver, By.LINK_TEXT, '1')  # Cambiar según el reporte específico
    reporte_bug_link.click()

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Encontrar el campo de caso de bug en el formulario de reporte de bug
    id_bug_dropdown = wait_for_element(driver, By.NAME, 'id_bug')

    # Crear un objeto Select para el campo de caso de bug
    select_id_bug = Select(id_bug_dropdown)

    # Seleccionar el caso de bug deseado por el índice 
    select_id_bug.select_by_index(2)  # Por ejemplo, seleccionar el segundo caso de bug

    time.sleep(2)

    # Encontrar el campo de estado en el formulario de reporte de bug
    estado_reporte_bug_dropdown = wait_for_element(driver, By.NAME, 'estado')

    # Crear un objeto Select para el campo de estado del reporte de bug
    select_estado_reporte_bug = Select(estado_reporte_bug_dropdown)

    # Seleccionar el estado deseado 
    select_estado_reporte_bug.select_by_value('APROBADO')  # Seleccionar 'APROBADO'

    time.sleep(2)

    # Hacer clic en el botón "Guardar"
    submit_button = driver.find_element(By.NAME, '_save')
    submit_button.click()

    time.sleep(2)
    
    expected_pattern = re.compile(r'El reporte de bug “(.+?)” se cambió correctamente.')
    match = expected_pattern.search(driver.page_source)

    if not match:
        raise AssertionError('No se encontró el mensaje de aprobación esperado.')

# Manejar errores
except Exception as e:
    print(f'Error: {str(e)}')
    traceback.print_exc()

# Cerrar el navegador
driver.quit()
