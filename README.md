# Proyecto Fundamentos de Testing y aseguramiento de calidad
grupo 4

### Requisitos previos:
Se debe tener instalado postgresql y python.

Se recomienda crear y ejecutar todo el código en un ambiente virtual, este se puede crear con:
<br>
```python venv .venv```
<br>
Luego se activa el ambiente virtual con el comando (en windows):
<br>
```.\.venv\Scrips\activate```

### Instalación de dependencias
Para instalar las dependencias se utiliza el comando:
<br>
```pip install -r requirements.txt```

### Ejecutar el software
Con los requisitos anteriores, se deben ejecutar los siguientes comandos:
Para crear la base de datos postgreSQL:
<br>
```python manage.py makemigrations``` y ```python manage.py migrate```
<br>
Para inicializar el servidor:
<br>
```python manage.py runserver```
<br>
Esto iniciará el servidor y en la consola de comandos se mostrará la URL de donde está el servidor.

### Ejecutar los tests unitarios
Para ejecutar los tests unitarios:
```python manage.py test```
<br>
Notar que no es necesario tener el servidor funcionando para realizar los tests, tampoco tener datos en la base de datos ya que estos se crean y borran al hacer los tests.
<br>
### Ejecutar los tests de integración
Se recomienda ejecutar los tests de integración en un navegador chrome versión >= 119.0.6045 (no es necesario tener el navegador activo al ejecutar los tests).
<br>
Se pueden ejecutar todos los test de integración con el comando:
<br>
```python run_integration_tests.py```
<br>
Donde se tiene que agregar el path a python en 'python path' (linea 4).




### Enlaces útiles
[Chrome latest versions](https://googlechromelabs.github.io/chrome-for-testing/#stable)
