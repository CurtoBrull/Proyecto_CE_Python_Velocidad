#!/usr/bin/env python3
"""
Script de inicio para la API de Radar de Velocidad en producción.
Maneja la inicialización de la base de datos y el arranque del servidor.
"""

import os
import sys
from pathlib import Path

# Añadir el directorio actual al path para imports
sys.path.insert(0, str(Path(__file__).parent))

from database import engine, Base
import models

def init_database():
    """Inicializa la base de datos creando todas las tablas."""
    print("🔧 Inicializando base de datos...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        sys.exit(1)

def main():
    """Función principal de inicio."""
    print("🚀 Iniciando API de Radar de Velocidad...")
    
    # Inicializar base de datos
    init_database()
    
    # Obtener puerto del entorno o usar 8000 por defecto
    port = os.getenv("PORT", "8000")
    
    print(f"🌐 Servidor iniciando en puerto {port}")
    
    # Importar y ejecutar uvicorn
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(port),
        log_level="info"
    )

if __name__ == "__main__":
    main()