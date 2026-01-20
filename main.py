from fastapi import FastAPI
import time
import os
import csv
from datetime import datetime

app = FastAPI()

DISTANCIA_METROS = 100  # Distancia entre los dos sensores en metros
ARCHIVO_MEDICION = "medicion.txt"
ARCHIVO_CSV = "mediciones.csv"


def guardar_medicion_csv(tiempo_segundos: float, velocidad_ms: float, velocidad_kmh: float):
    """Guarda los datos de la medición en un archivo CSV."""
    archivo_existe = os.path.exists(ARCHIVO_CSV)

    with open(ARCHIVO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Escribir encabezados si el archivo es nuevo
        if not archivo_existe:
            writer.writerow(["fecha_hora", "tiempo_segundos", "velocidad_ms", "velocidad_kmh", "distancia_metros"])

        # Escribir los datos de la medición
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            round(tiempo_segundos, 3),
            round(velocidad_ms, 2),
            round(velocidad_kmh, 2),
            DISTANCIA_METROS
        ])


@app.post("/detectar")
async def detectar_movimiento():
    """
    Simula la detección de movimiento.
    - Primera llamada: guarda el timestamp en el archivo TXT
    - Segunda llamada: calcula la velocidad y limpia el archivo
    """
    timestamp_actual = time.time()

    # Verificar si existe una medición previa
    if os.path.exists(ARCHIVO_MEDICION):
        # Leer el timestamp de la primera medición
        with open(ARCHIVO_MEDICION, "r") as f:
            timestamp_inicial = float(f.read().strip())

        # Calcular tiempo transcurrido y velocidad
        tiempo_segundos = timestamp_actual - timestamp_inicial
        velocidad_ms = DISTANCIA_METROS / tiempo_segundos  # m/s
        velocidad_kmh = velocidad_ms * 3.6  # km/h

        # Guardar en CSV
        guardar_medicion_csv(tiempo_segundos, velocidad_ms, velocidad_kmh)

        # Limpiar el archivo para nueva medición
        os.remove(ARCHIVO_MEDICION)

        return {
            "estado": "velocidad_calculada",
            "tiempo_segundos": round(tiempo_segundos, 3),
            "velocidad_ms": round(velocidad_ms, 2),
            "velocidad_kmh": round(velocidad_kmh, 2),
            "distancia_metros": DISTANCIA_METROS
        }
    else:
        # Primera detección: guardar timestamp
        with open(ARCHIVO_MEDICION, "w") as f:
            f.write(str(timestamp_actual))

        return {
            "estado": "primera_deteccion",
            "mensaje": "Timestamp guardado. Esperando segunda detección...",
            "timestamp": timestamp_actual
        }


@app.get("/estado")
async def obtener_estado():
    """Verifica si hay una medición en progreso."""
    if os.path.exists(ARCHIVO_MEDICION):
        with open(ARCHIVO_MEDICION, "r") as f:
            timestamp = float(f.read().strip())
        return {
            "medicion_en_progreso": True,
            "timestamp_inicial": timestamp
        }
    return {"medicion_en_progreso": False}


@app.delete("/reset")
async def resetear_medicion():
    """Elimina la medición en progreso."""
    if os.path.exists(ARCHIVO_MEDICION):
        os.remove(ARCHIVO_MEDICION)
        return {"mensaje": "Medición reseteada"}
    return {"mensaje": "No había medición en progreso"}


@app.get("/mediciones")
async def obtener_mediciones():
    """Devuelve todas las mediciones guardadas en el CSV."""
    if not os.path.exists(ARCHIVO_CSV):
        return {"mediciones": [], "total": 0}

    mediciones = []
    with open(ARCHIVO_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mediciones.append({
                "fecha_hora": row["fecha_hora"],
                "tiempo_segundos": float(row["tiempo_segundos"]),
                "velocidad_ms": float(row["velocidad_ms"]),
                "velocidad_kmh": float(row["velocidad_kmh"]),
                "distancia_metros": int(row["distancia_metros"])
            })

    return {"mediciones": mediciones, "total": len(mediciones)}
