from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

"""

    US: Como usuario quiero poder navegar entre los bugs reportados que están siendo atendidos para informarme de que otros problemas existen

    Criterios de aceptación:
    - En la vista de la lista de bugs se muestra una lista de los bugs que están siendo atendidos
    - En la vista de la lista de bugs se muestran botones para navegar entre las páginas de bugs

    Precondiciones:
    - Deben existir bugs reportados

    Pasos:
    1. El usuario ingresa a la vista de la lista de bugs
    2. El usuario hace click en el botón de la página siguiente
    3. El usuario verifica que el contenido de la página haya cambiado
    4. El usuario hace click en el botón de la página anterior
    5. El usuario verifica que el contenido de la página haya cambiado
    6. El usuario hace click en el botón de la última página
    7. El usuario verifica que el contenido de la página haya cambiado
    8. El usuario hace click en el botón de la primera página
    9. El usuario verifica que el contenido de la página haya cambiado

"""


# Path al driver de chrome
chromedriver_path = 'bug_report/chromedriver-win64/chromedriver.exe'

# Se crean las opciones para el ejecutable
chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_service = Service(chromedriver_path)

# Se configura el driver del navegador
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:

    # Abrir la página web
    driver.get('http://127.0.0.1:8000/buglist')

    # Esperar a que el elemento sea visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'bug-table')))
    
    # Obtener el número total de páginas
    total_pages = 4
    #print(f'Número total de páginas: {total_pages}')

    # Obtener el contenido de la página actual
    current_page_content = driver.find_element(By.ID, 'bug-table').text

    # Iterar a través de todas las páginas
    for page_number in range(1, total_pages + 1):
        
        # Hacer clic en el enlace de la página correspondiente
        link_selector = f'.pagination.bug-pagination #arrow-page-next' if page_number != '...' else '.ellipsis'
        link = driver.find_element(By.CSS_SELECTOR, link_selector)
        link.click()

        # Esperar a que la nueva página se cargue completamente
        WebDriverWait(driver, 10).until(EC.staleness_of(link))

        # Obtener el contenido de la nueva página
        new_page_content = driver.find_element(By.ID, 'bug-table').text

        # Verificar que el contenido de la nueva página es diferente al contenido de la página anterior
        assert current_page_content != new_page_content, f'El contenido de la página {page_number + 1} no cambió al hacer clic en el enlace.'

        # Actualizar el contenido de la página actual
        current_page_content = new_page_content

    #Iterar desde la ultima pagina hasta la primera
    for page_number in range(total_pages, 0, -1):
        
        # Hacer clic en el enlace de la página correspondiente
        link_selector = f'.pagination.bug-pagination #arrow-page-prev' if page_number != '...' else '.ellipsis'
        link = driver.find_element(By.CSS_SELECTOR, link_selector)
        link.click()

        # Esperar a que la nueva página se cargue completamente
        WebDriverWait(driver, 10).until(EC.staleness_of(link))

        # Obtener el contenido de la nueva página
        new_page_content = driver.find_element(By.ID, 'bug-table').text

        # Verificar que el contenido de la nueva página es diferente al contenido de la página anterior
        assert current_page_content != new_page_content, f'El contenido de la página {page_number + 1} no cambió al hacer clic en el enlace.'

        # Actualizar el contenido de la página actual
        current_page_content = new_page_content
    

    #Ir directamente a la ultima pagina
    link = driver.find_element(By.CSS_SELECTOR, '.pagination.bug-pagination #arrow-page-last')
    link.click()

    # Esperar a que la nueva página se cargue completamente
    WebDriverWait(driver, 10).until(EC.staleness_of(link))

    # Obtener el contenido de la nueva página
    new_page_content = driver.find_element(By.ID, 'bug-table').text

    # Verificar que el contenido de la nueva página es diferente al contenido de la página anterior
    assert current_page_content != new_page_content, f'El contenido de la página {total_pages} no cambió al hacer clic en el enlace.'

    # Actualizar el contenido de la página actual
    current_page_content = new_page_content

    #Ir directamente a la primera pagina
    link = driver.find_element(By.CSS_SELECTOR, '.pagination.bug-pagination #arrow-page-first')
    link.click()

    # Esperar a que la nueva página se cargue completamente
    WebDriverWait(driver, 10).until(EC.staleness_of(link))

    # Obtener el contenido de la nueva página
    new_page_content = driver.find_element(By.ID, 'bug-table').text

    # Verificar que el contenido de la nueva página es diferente al contenido de la página anterior
    assert current_page_content != new_page_content, f'El contenido de la página 1 no cambió al hacer clic en el enlace.'

    # Actualizar el contenido de la página actual
    current_page_content = new_page_content

    print('Prueba exitosa')

except Exception as e:
    print(f'Error: {str(e)}')

finally:
    driver.quit()
