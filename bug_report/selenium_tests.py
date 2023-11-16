from selenium import webdriver

# Configura el controlador del navegador (ejemplo con Chrome)
driver = webdriver.Chrome(executable_path='bug_report/chromedriver_win32/chromedriver.exe')

# Realiza pruebas
try:
    # Abre una página web
    driver.get('http://127.0.0.1:8000/accounts/login/?next=/login')

    # Verifica resultados utilizando afirmaciones (assertions)
    # Encuentra los elementos de entrada de usuario y contraseña
    username_input = driver.find_element_by_name('username')
    password_input = driver.find_element_by_name('password')

    # Ingresa tus credenciales (usuario y contraseña)
    username_input.send_keys('tu_usuario')
    password_input.send_keys('tu_contraseña')

    # Encuentra el botón de inicio de sesión y haz clic en él
    login_button = driver.find_element_by_name('Iniciar sesión')
    login_button.click()

    # Verifica si el inicio de sesión fue exitoso
    assert 'Bienvenido' in driver.page_source


except Exception as e:
    print(f'Error: {str(e)}')

# Cierra el navegador al finalizar
driver.quit()
