"""
Conversor de divisas de pesos argentinos a dólares.
Consulta las cotizaciones del dólar oficial y blue mediante una API.
"""

import requests
from tabulate import tabulate


URL_API = "https://dolarapi.com/v1/dolares"


def ingresar_monto() -> float:
    """Solicita un monto positivo en pesos argentinos.

    Returns:
        El monto ingresado por el usuario.
    """
    while True:
        try:
            entrada = input(
                "Ingresá el monto en pesos argentinos (ej. 100000): "
            )
            monto = float(entrada.replace(",", "."))

            if monto > 0:
                return monto

            print("Error: el monto debe ser mayor que cero.")

        except ValueError:
            print("Error: ingresá un número válido.")


def obtener_cotizaciones() -> list:
    """Consulta la API y obtiene las cotizaciones oficial y blue.

    Returns:
        Una lista con los datos de compra y venta de ambos dólares.

    Raises:
        Exception: Si ocurre un error al consultar o procesar la API.
    """
    try:
        respuesta = requests.get(URL_API, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        cotizaciones = []

        for dolar in datos:
            nombre = dolar.get("nombre", "").lower()

            if nombre == "oficial" or nombre == "blue":
                compra = float(dolar["compra"])
                venta = float(dolar["venta"])

                if venta <= 0:
                    raise ValueError("La cotización de venta no es válida.")

                cotizaciones.append(
                    {
                        "nombre": nombre,
                        "compra": compra,
                        "venta": venta,
                    }
                )

        if len(cotizaciones) != 2:
            raise ValueError(
                "No se encontraron las cotizaciones oficial y blue."
            )

        return cotizaciones

    except requests.exceptions.RequestException as error:
        raise Exception(
            "No se pudo consultar la API. Revisá tu conexión."
        ) from error

    except (ValueError, KeyError, TypeError) as error:
        raise Exception(
            "La API devolvió datos inválidos o incompletos."
        ) from error


def mostrar_resultados(monto: float, cotizaciones: list) -> None:
    """Muestra las cotizaciones y el resultado de la conversión.

    Args:
        monto: Monto ingresado en pesos argentinos.
        cotizaciones: Lista con las cotizaciones obtenidas.
    """
    filas = []

    for dolar in cotizaciones:
        resultado = monto / dolar["venta"]

        filas.append(
            [
                dolar["nombre"].capitalize(),
                f"$ {dolar['compra']:.2f}",
                f"$ {dolar['venta']:.2f}",
                f"USD {resultado:.2f}",
            ]
        )

    print(f"\nMonto ingresado: ARS {monto:.2f}\n")

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
        )
    )


def main() -> None:
    """Ejecuta el conversor de divisas."""
    try:
        monto = ingresar_monto()
        cotizaciones = obtener_cotizaciones()
        mostrar_resultados(monto, cotizaciones)

    except KeyboardInterrupt:
        print("\nPrograma cancelado por el usuario.")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()