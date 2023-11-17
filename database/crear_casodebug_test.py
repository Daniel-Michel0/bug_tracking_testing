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
# Como administrador del sistema, quiero poder añadir casos de bugs y asignarlos a un programador para que sean resueltos.

# Path al driver de Chrome
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

    # Ir a la página de casos de bugs
    driver.get('http://127.0.0.1:8000/admin/database/bug/')

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Hacer clic en el botón "Añadir caso de bug"
    add_bug_button = wait_for_element(driver, By.LINK_TEXT, 'AÑADIR CASO DE BUG')
    add_bug_button.click()

    # Esperar 2 segundos para procesar
    time.sleep(2)

    # Rellenar el formulario para añadir un caso de bug
    titulo_bug_input = wait_for_element(driver, By.NAME, 'titulo')
    descripcion_bug_input = wait_for_element(driver, By.NAME, 'descripcion')
    id_proyecto_bug_dropdown = wait_for_element(driver, By.NAME, 'id_proyecto')
    estado_bug_dropdown = wait_for_element(driver, By.NAME, 'estado')
    prioridad_bug_dropdown = wait_for_element(driver, By.NAME, 'prioridad')
    id_programador_bug_dropdown = wait_for_element(driver, By.NAME, 'id_programador')

    titulo_bug_input.send_keys('Título del caso de bug')  # Cambiar según sea necesario
    time.sleep(1)
    descripcion_bug_input.send_keys('Descripción del caso de bug')  # Cambiar según sea necesario
    time.sleep(1)
    
    select_id_proyecto_bug = Select(id_proyecto_bug_dropdown)
    select_id_proyecto_bug.select_by_index(2)  # Por ejemplo, seleccionar el segundo proyecto
    time.sleep(1)
    
    select_estado_bug = Select(estado_bug_dropdown)
    select_estado_bug.select_by_visible_text('bug recien asignado')  # Por ejemplo, seleccionar 'ABIERTO'
    time.sleep(1)
    
    select_prioridad_bug = Select(prioridad_bug_dropdown)
    select_prioridad_bug.select_by_visible_text('bug de alta prioridad')  # Por ejemplo, seleccionar 'ALTA'
    time.sleep(1)
    
    select_id_programador_bug = Select(id_programador_bug_dropdown)
    select_id_programador_bug.select_by_index(2)  # Por ejemplo, seleccionar el segundo programador
    time.sleep(1)
    
    # Hacer clic en el botón "Guardar"
    submit_button = driver.find_element(By.NAME, '_save')
    submit_button.click()

    time.sleep(2)
    
    expected_pattern = re.compile(r'El caso de bug “(.+?)” fue agregado correctamente.')
    match = expected_pattern.search(driver.page_source)

    if not match:
        raise AssertionError('No se encontró el mensaje de aprobación esperado.')

# Manejar errores
except Exception as e:
    print(f'Error: {str(e)}')
    traceback.print_exc()

# Cerrar el navegador
driver.quit()
