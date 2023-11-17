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
# Como administrador del sistema quiero tener la capacidad de aprobar las reasignaciones de Bugs propuestas por los programadores, para poder asignar esos Bugs a programadores más adecuados que puedan abordarlos de manera efectiva. 

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
    # Ir a la página de reasignaciones pendientes
    driver.get('http://127.0.0.1:8000/admin/database/reasignacion/')

    # Esperar 2 segundos para procesar
    time.sleep(2)

   # Encontrar la primera solicitud de reasignación y hacer clic en ella
    reasignacion_link = wait_for_element(driver, By.LINK_TEXT, '1')  # Cambiar según la reasignación específica
    reasignacion_link.click()

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Encontrar el campo de programador final en el formulario de reasignación
    programador_final_dropdown = wait_for_element(driver, By.NAME, 'id_programador_final')

    # Crear un objeto Select para el campo de programador final
    select_programador_final = Select(programador_final_dropdown)

    # Seleccionar el programador deseado por el índice 
    select_programador_final.select_by_index(2)  # Por ejemplo, seleccionar el segundo programador

    time.sleep(2)
    # Encontrar el campo de estado en el formulario de reasignación
    estado_reasignacion_dropdown = wait_for_element(driver, By.NAME, 'estado')

    # Crear un objeto Select para el campo de estado de la reasignación
    select_estado_reasignacion = Select(estado_reasignacion_dropdown)

    # Seleccionar el estado deseado 
    select_estado_reasignacion.select_by_value('APROBADO')  # Seleccionar 'APROBADO'
    
    time.sleep(2)

    # Hacer clic en el botón "Guardar"
    submit_button = driver.find_element(By.NAME, '_save')
    submit_button.click()
    
    time.sleep(2)
    
    expected_pattern = re.compile(r'El reasignación “(.+?)” se cambió correctamente.')
    match = expected_pattern.search(driver.page_source)

    if not match:
        raise AssertionError('No se encontró el mensaje de aprobación esperado.')

# Manejar errores
except Exception as e:
    print(f'Error: {str(e)}')
    traceback.print_exc()

# Cerrar el navegador
driver.quit()