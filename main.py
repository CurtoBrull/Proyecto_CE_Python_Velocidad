from fastapi import FastAPI
from datetime import datetime
import json

app = FastAPI()

ARCHIVO_MEDICIONES = "mediciones.json"

@app.post("/")
def iniciar_medicion():
    medicion = datetime.now().timestamp()
    try:
        with open(ARCHIVO_MEDICIONES, "r") as f:
            datos = json.load(f)
            medicion1 = datos.get("medicion1")
            if medicion1 is None:
                datos["medicion1"] = medicion
                with open(ARCHIVO_MEDICIONES, "w") as fw:
                    json.dump(datos, fw, indent=2)
            else:
                calcular_velocidad(medicion1, medicion)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(ARCHIVO_MEDICIONES, "w") as f:
            json.dump({"medicion1": medicion}, f, indent=2)

def calcular_velocidad(medicion1, medicion2):
    distancia = 100
    segundos = medicion2 - float(medicion1)
    velocidad = distancia / segundos
    print(f"Velocidad: {velocidad:.2f} m/s")
    # Limpiar el archivo JSON para la siguiente medición
    with open(ARCHIVO_MEDICIONES, "w") as f:
        json.dump({}, f, indent=2)