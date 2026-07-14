# Urban Routes - Sprint 9

## Descripción del proyecto

Este proyecto contiene pruebas automatizadas para la aplicación web Urban Routes utilizando Selenium WebDriver y Pytest. 
Las pruebas verifican el flujo de solicitud de un taxi, desde la selección de la ruta hasta la confirmación del pedido.

## Objetivo del Sprint

Implementar pruebas automatizadas para la aplicación Urban Routes utilizando Selenium WebDriver, Pytest y el patrón 
Page Object Model (POM), organizando el proyecto en archivos separados para mejorar la reutilización y el mantenimiento 
del código.

## Dependencias

- Python 3
- Selenium
- Pytest
- Chrome
- ChromeDriver

## Estructura del proyecto

- data.py
- pages.py
- helpers.py
- main.py
- README.md

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
- Confirmación del código SMS
- Esperar la información del conductor

## Cómo ejecutar las pruebas

1. Clona el repositorio.
2. Instala las dependencias:

```bash
pip install selenium pytest
```

3. Ejecuta las pruebas:

```bash
pytest main.py -v
```

4. Ejecuta una prueba específica:

```bash
pytest main.py -v -k test_add_card
```

## Autor

Carlos Eduardo Allard Vidal