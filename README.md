# Conversor de Divisas

Programa de consola desarrollado en Python que permite ingresar un monto en pesos argentinos (ARS), consultar las cotizaciones del dólar oficial y blue mediante una API pública y calcular el equivalente en dólares utilizando la cotización de venta.

## Integrante

- Agustin Piacentino

## Requisitos

- Python 3.9 o superior.
- Conexión a Internet.
- pip.
# Conversor de Divisas

Programa de consola desarrollado en Python que permite ingresar un monto en pesos argentinos (ARS), consultar las cotizaciones del dólar oficial y blue mediante una API pública y calcular el equivalente en dólares utilizando la cotización de venta.

## Integrante

- Agustin Piacentino

## Requisitos

- Python 3.9 o superior.
- Conexión a Internet.
- pip, el gestor de paquetes de Python.

## Crear el entorno virtual

Desde una terminal ubicada en la carpeta del proyecto, ejecutar:

```powershell
python -m venv .venv
```

## Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

En Windows CMD:

```bat
.venv\Scripts\activate.bat
```

Si PowerShell bloquea la ejecución de scripts, puede ser necesario ejecutar el siguiente comando:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Instalar las dependencias

Con el entorno virtual activado, ejecutar:

```powershell
python -m pip install -r requirements.txt
```

## Ejecutar el programa

Desde la carpeta del proyecto y con el entorno virtual activado:

```powershell
python conversor.py
```

El programa solicita un monto positivo en pesos argentinos. Se puede ingresar un número entero o decimal, por ejemplo `75000` o `75000,50`.

## Librerías utilizadas

- **requests:** realiza la petición HTTP para consultar las cotizaciones de la API.
- **tabulate:** presenta los resultados en una tabla en la terminal.

## API utilizada

- **DolarAPI:** https://dolarapi.com/v1/dolares

La información depende de la disponibilidad del servicio y de las cotizaciones publicadas por la API.

## Archivos del proyecto

- `conversor.py`: código fuente del programa.
- `requirements.txt`: dependencias y versiones instaladas.
- `.gitignore`: archivos y carpetas que Git debe ignorar.
- `README.md`: documentación e instrucciones de instalación y ejecución.

El entorno virtual `.venv/` se crea localmente y no debe subirse al repositorio.

## Publicación

El proyecto se encuentra en un repositorio público de GitHub para facilitar su revisión y evaluación.
