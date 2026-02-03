"""
Script de inicio para Render.
Inicializa la base de datos y arranca el servidor uvicorn.
"""
import os
import uvicorn
from database import engine, Base, get_db
import models

# Crear todas las tablas
print("Inicializando base de datos...")
Base.metadata.create_all(bind=engine)
print("Base de datos inicializada correctamente")

# Obtener puerto de la variable de entorno (Render usa PORT)
port = int(os.getenv("PORT", 8080))

print(f"Servidor iniciando en puerto {port}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
