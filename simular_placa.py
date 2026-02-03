"""
Simulador de placa ESP32 para pruebas locales.
Envia mediciones automaticas a la API simulando el paso de objetos por los sensores.

Uso:
    python simular_placa.py [--url URL] [--intervalo SEGUNDOS] [--cantidad N]

Ejemplos:
    python simular_placa.py                          # Simula 5 mediciones con intervalos aleatorios
    python simular_placa.py --cantidad 10            # Simula 10 mediciones
    python simular_placa.py --intervalo 3            # Intervalo fijo de 3 segundos entre sensores
    python simular_placa.py --url http://localhost:8081/mediciones/  # URL personalizada
"""

import requests
import time
import random
import argparse


def simular_medicion(api_url: str, intervalo: float = None):
    """Simula una medicion completa (sensor 1 + sensor 2)."""

    print("\n" + "=" * 50)

    # Sensor 1
    print("Sensor 1 activado...")
    try:
        response = requests.post(api_url, timeout=10)
        data = response.json()
        print(f"  -> {data.get('mensaje', 'OK')}")
    except Exception as e:
        print(f"  -> Error: {e}")
        return False

    # Esperar (simula tiempo de recorrido)
    if intervalo is None:
        intervalo = random.uniform(1.5, 8.0)  # Entre 1.5 y 8 segundos

    print(f"Esperando {intervalo:.2f} segundos...")
    time.sleep(intervalo)

    # Sensor 2
    print("Sensor 2 activado...")
    try:
        response = requests.post(api_url, timeout=10)
        data = response.json()

        if 'velocidad_kmh' in data and data['velocidad_kmh']:
            velocidad = data['velocidad_kmh']
            tiempo = data.get('tiempo_segundos', intervalo)

            # Determinar si es exceso (asumiendo limite de 50 km/h por defecto)
            exceso = " ** EXCESO **" if velocidad > 50 else ""

            print(f"  -> Velocidad: {velocidad:.2f} km/h en {tiempo:.2f}s{exceso}")
        else:
            print(f"  -> {data.get('mensaje', 'OK')}")

        return True

    except Exception as e:
        print(f"  -> Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Simulador de placa ESP32 para pruebas"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8080/mediciones/",
        help="URL de la API (default: http://localhost:8080/mediciones/)"
    )
    parser.add_argument(
        "--intervalo",
        type=float,
        default=None,
        help="Intervalo fijo entre sensores en segundos (default: aleatorio 1.5-8s)"
    )
    parser.add_argument(
        "--cantidad",
        type=int,
        default=5,
        help="Numero de mediciones a simular (default: 5)"
    )
    parser.add_argument(
        "--pausa",
        type=float,
        default=2.0,
        help="Pausa entre mediciones completas en segundos (default: 2)"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("SIMULADOR DE PLACA ESP32")
    print("=" * 50)
    print(f"URL API: {args.url}")
    print(f"Mediciones a simular: {args.cantidad}")
    print(f"Intervalo entre sensores: {'aleatorio' if args.intervalo is None else f'{args.intervalo}s'}")
    print(f"Pausa entre mediciones: {args.pausa}s")
    print("\nPresiona Ctrl+C para detener\n")

    try:
        exitosas = 0
        for i in range(args.cantidad):
            print(f"\n--- Medicion {i + 1}/{args.cantidad} ---")

            if simular_medicion(args.url, args.intervalo):
                exitosas += 1

            if i < args.cantidad - 1:
                print(f"\nEsperando {args.pausa}s antes de siguiente medicion...")
                time.sleep(args.pausa)

        print("\n" + "=" * 50)
        print(f"RESUMEN: {exitosas}/{args.cantidad} mediciones exitosas")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nSimulacion detenida por el usuario")


if __name__ == "__main__":
    main()
