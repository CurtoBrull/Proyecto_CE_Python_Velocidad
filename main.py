from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

app = FastAPI(title="Radar de Velocidad API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ARCHIVO_MEDICIONES = "mediciones.json"
ARCHIVO_CONFIG = "config.json"
DISTANCIA_SENSORES = 100  # metros
LIMITE_VELOCIDAD = 50  # km/h


def cargar_config():
    """Carga la configuración desde el archivo JSON."""
    try:
        with open(ARCHIVO_CONFIG, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def guardar_config(config: dict):
    """Guarda la configuración en el archivo JSON."""
    with open(ARCHIVO_CONFIG, "w") as f:
        json.dump(config, f, indent=2)


def obtener_distancia() -> float:
    config = cargar_config()
    return config.get("distancia_sensores", DISTANCIA_SENSORES)


def obtener_limite() -> float:
    config = cargar_config()
    return config.get("limite_velocidad", LIMITE_VELOCIDAD)


class MedicionRequest(BaseModel):
    timestamp: Optional[float] = None  # Unix timestamp desde la placa
    sensor_id: Optional[int] = None    # 1 o 2


class MedicionResponse(BaseModel):
    mensaje: str
    velocidad_ms: Optional[float] = None
    velocidad_kmh: Optional[float] = None
    tiempo_segundos: Optional[float] = None


@app.post("/", response_model=MedicionResponse)
@app.post("/mediciones/", response_model=MedicionResponse)
def registrar_medicion(data: Optional[MedicionRequest] = None):
    # Usar timestamp de la placa si viene, sino usar el del servidor
    if data and data.timestamp:
        medicion = data.timestamp
    else:
        medicion = datetime.now().timestamp()

    try:
        with open(ARCHIVO_MEDICIONES, "r") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = {}

    medicion1 = datos.get("medicion1")

    if medicion1 is None:
        # Primera medición - guardar timestamp
        datos["medicion1"] = medicion
        with open(ARCHIVO_MEDICIONES, "w") as f:
            json.dump(datos, f, indent=2)
        return MedicionResponse(mensaje="Sensor 1 activado. Esperando sensor 2...")
    else:
        # Segunda medición - calcular velocidad
        resultado = calcular_velocidad(medicion1, medicion)
        # Limpiar para siguiente medición
        with open(ARCHIVO_MEDICIONES, "w") as f:
            json.dump({}, f, indent=2)
        return resultado


def calcular_velocidad(medicion1: float, medicion2: float) -> MedicionResponse:
    segundos = medicion2 - float(medicion1)

    if segundos <= 0:
        return MedicionResponse(mensaje="Error: tiempo negativo o cero")

    distancia = obtener_distancia()
    velocidad_ms = distancia / segundos
    velocidad_kmh = velocidad_ms * 3.6

    limite = obtener_limite()
    exceso = " - EXCESO" if velocidad_kmh > limite else ""
    print(f"Velocidad: {velocidad_kmh:.2f} km/h ({velocidad_ms:.2f} m/s) en {segundos:.2f}s{exceso}")

    return MedicionResponse(
        mensaje=f"Velocidad: {velocidad_kmh:.2f} km/h",
        velocidad_ms=round(velocidad_ms, 2),
        velocidad_kmh=round(velocidad_kmh, 2),
        tiempo_segundos=round(segundos, 2)
    )


@app.get("/estado/")
def obtener_estado():
    try:
        with open(ARCHIVO_MEDICIONES, "r") as f:
            datos = json.load(f)
            hay_pendiente = datos.get("medicion1") is not None
    except (FileNotFoundError, json.JSONDecodeError):
        hay_pendiente = False

    return {
        "esperando_sensor2": hay_pendiente,
        "distancia_sensores": obtener_distancia(),
        "limite_velocidad": obtener_limite()
    }


@app.delete("/reset/")
def reset_medicion():
    with open(ARCHIVO_MEDICIONES, "w") as f:
        json.dump({}, f, indent=2)
    return {"mensaje": "Medición reiniciada"}


class ConfigUpdate(BaseModel):
    valor: str


@app.get("/configuracion/distancia_sensores")
def get_distancia():
    return {"clave": "distancia_sensores", "valor": str(obtener_distancia())}


@app.put("/configuracion/distancia_sensores")
def set_distancia(data: ConfigUpdate):
    try:
        nueva_distancia = float(data.valor)
        if nueva_distancia <= 0:
            return {"error": "La distancia debe ser mayor a 0"}
        config = cargar_config()
        config["distancia_sensores"] = nueva_distancia
        guardar_config(config)
        return {"clave": "distancia_sensores", "valor": str(nueva_distancia)}
    except ValueError:
        return {"error": "Valor de distancia inválido"}


@app.get("/configuracion/limite_velocidad")
def get_limite():
    return {"clave": "limite_velocidad", "valor": str(obtener_limite())}


@app.put("/configuracion/limite_velocidad")
def set_limite(data: ConfigUpdate):
    try:
        nuevo_limite = float(data.valor)
        if nuevo_limite <= 0:
            return {"error": "El límite debe ser mayor a 0"}
        config = cargar_config()
        config["limite_velocidad"] = nuevo_limite
        guardar_config(config)
        return {"clave": "limite_velocidad", "valor": str(nuevo_limite)}
    except ValueError:
        return {"error": "Valor de límite inválido"}