"""
Conversor de divisas: pesos argentinos a dólares.
Consulta las cotizaciones del dólar oficial y blue desde una API pública.
"""

from typing import Any

import requests
from tabulate import tabulate


URL_API = "https://dolarapi.com/v1/dolares"
TIPOS_DOLAR = ("oficial", "blue")


def ingresar_monto() -> float:
    """Solicita y valida un monto positivo en pesos argentinos.

    Returns:
        El monto ingresado por el usuario como número decimal.
    """
    while True:
        try:
            entrada = input(
                "Ingresá el monto en pesos argentinos (ej. 100000): "
            )
            monto = float(entrada.replace(",", "."))

            if monto <= 0:
                print("Error: el monto debe ser mayor que cero.")
                continue

            return monto

        except ValueError:
            print(
                "Error: ingresá un número válido, por ejemplo "
                "100000 o 100000,50."
            )


def obtener_cotizaciones() -> list[dict[str, Any]]:
    """Consulta la API y devuelve las cotizaciones oficial y blue.

    Returns:
        Una lista con nombre, compra y venta de ambos tipos de dólar.

    Raises:
        RuntimeError: Si falla la conexión, la respuesta o los datos.
    """
    try:
        respuesta = requests.get(URL_API, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        if not isinstance(datos, list):
            raise ValueError("La API devolvió un formato inesperado.")

        cotizaciones = []

        for dolar in datos:
            if not isinstance(dolar, dict):
                continue

            nombre = dolar.get("nombre")
            if not isinstance(nombre, str):
                continue

            nombre_normalizado = nombre.strip().lower()

            if nombre_normalizado not in TIPOS_DOLAR:
                continue

            compra = dolar.get("compra")
            venta = dolar.get("venta")

            if compra is None or venta is None:
                raise ValueError(
                    f"Faltan datos de compra o venta para {nombre}."
                )

            try:
                compra = float(compra)
                venta = float(venta)
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Los precios de {nombre} no son numéricos."
                ) from error

            if compra < 0 or venta <= 0:
                raise ValueError(
                    f"Los precios de {nombre} son inválidos."
                )

            cotizaciones.append(
                {
                    "nombre": nombre,
                    "compra": compra,
                    "venta": venta,
                }
            )

        nombres_encontrados = {
            dolar["nombre"].strip().lower()
            for dolar in cotizaciones
        }

        if set(TIPOS_DOLAR) != nombres_encontrados:
            raise ValueError(
                "La API no devolvió las cotizaciones oficial y blue."
            )

        return cotizaciones

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "La API tardó demasiado en responder."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "No se pudo conectar con la API. Revisá Internet."
        ) from error

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"La API respondió con un error HTTP: {error}"
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Ocurrió un error durante la petición: {error}"
        ) from error

    except (ValueError, TypeError) as error:
        raise RuntimeError(
            f"Los datos recibidos no son válidos: {error}"
        ) from error


def mostrar_resultados(
    monto: float,
    cotizaciones: list[dict[str, Any]],
) -> None:
    """Calcula y muestra la conversión en una tabla de consola.

    Args:
        monto: Cantidad de pesos argentinos ingresada.
        cotizaciones: Lista de cotizaciones obtenidas desde la API.
    """
    filas = []

    for dolar in cotizaciones:
        total_convertido = monto / dolar["venta"]

        filas.append(
            [
                dolar["nombre"].capitalize(),
                f"$ {dolar['compra']:,.2f}",
                f"$ {dolar['venta']:,.2f}",
                f"USD {total_convertido:,.2f}",
            ]
        )

    print(f"\nMonto ingresado: ARS {monto:,.2f}\n")
    print(
        tabulate(
            filas,
            headers=[
                "Tipo de dólar",
                "Compra (ARS)",
                "Venta (ARS)",
                "Total convertido",
            ],
            tablefmt="grid",
            stralign="right",
        )
    )


def main() -> None:
    """Coordina el ingreso del monto, la consulta y la presentación."""
    try:
        monto = ingresar_monto()
        cotizaciones = obtener_cotizaciones()
        mostrar_resultados(monto, cotizaciones)

    except KeyboardInterrupt:
        print("\nPrograma cancelado por el usuario.")

    except RuntimeError as error:
        print(f"\nNo se pudo completar la conversión: {error}")

    except Exception as error:
        print(f"\nOcurrió un error inesperado: {error}")


if __name__ == "__main__":
    main()