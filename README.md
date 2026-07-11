# Urban Routes - Sprint 9

## Descripción del proyecto

Este proyecto contiene pruebas automatizadas para la aplicación web Urban Routes utilizando Selenium WebDriver y Pytest. 
Las pruebas verifican el flujo de solicitud de un taxi, desde la selección de la ruta hasta la confirmación del pedido.

## Tecnologías y técnicas utilizadas

- Python 3
- Selenium WebDriver
- Pytest
- ChromeDriver
- Page Object Model (POM)
- Localizadores XPath, CSS Selector, ID y Class Name
- Esperas explícitas (WebDriverWait)
- Git y GitHub

## Pruebas incluidas

- Selección de origen y destino
- Selección de la tarifa Comfort
- Agregar número de teléfono
- Agregar tarjeta de crédito
- Agregar mensaje para el conductor
- Solicitar manta y pañuelos
- Agregar dos helados
- Solicitar un taxi

## Cómo ejecutar las pruebas

1. Clona el repositorio.
2. Instala las dependencias:

-terminal-
pip install -r requirements.txt

3. Ejecuta las pruebas:

-terminal-
pytest main.py -v

4. Ejecuta una prueba específica:

-terminal-
pytest main.py -v -k test_add_card