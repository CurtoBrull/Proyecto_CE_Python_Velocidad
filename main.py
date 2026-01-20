from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.post("/")
def iniciar_medicion():
    medicion=datetime.now().timestamp()
    try:
        with open("mediciones.txt", "r+") as f:
            medicion1=f.readline()
            if medicion1 == "":
                f.write(str(medicion)+"\n")
            else:
                calcular_velocidad(medicion1, medicion)
    except FileNotFoundError:
        with open("mediciones.txt", "w") as f:
            f.write(str(medicion)+"\n")

def calcular_velocidad(medicion1, medicion2):
    distancia=100
    segundos=medicion2-float(medicion1)
    velocidad=distancia/segundos
    print(f"Velocidad: {velocidad:.2f} m/s")
    try:
        with open("mediciones.txt", "w") as f:
            pass
    except FileNotFoundError:
        pass