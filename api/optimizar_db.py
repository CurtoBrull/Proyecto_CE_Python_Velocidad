#!/usr/bin/env python3
"""
Script para optimizar la base de datos creando índices.
Ejecutar después de tener datos en la base de datos.
"""

from database import engine, Base
import models  # Importar modelos para que Base los conozca
from sqlalchemy import text

def crear_indices():
    # Asegurar que las tablas existan
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        # Índice para filtrar mediciones completas
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_mediciones_completa ON mediciones (medicion_completa);"))
        # Índice para consultas por fecha
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_mediciones_timestamp ON mediciones (timestamp);"))
        # Índice compuesto para consultas de estadísticas
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_mediciones_completa_timestamp ON mediciones (medicion_completa, timestamp);"))
        conn.commit()
        print("Índices de base de datos creados exitosamente")

if __name__ == "__main__":
    crear_indices()
