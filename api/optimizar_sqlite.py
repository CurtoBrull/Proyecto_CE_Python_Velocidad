#!/usr/bin/env python3
"""
Script para optimizar SQLite con WAL mode y pragmas de rendimiento.
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, 'db', 'radar_velocidad.db')

def optimizar_sqlite():
    """Aplica optimizaciones de rendimiento a SQLite."""
    print(f"Optimizando base de datos: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cambiar a modo WAL (Write-Ahead Logging) - mejora concurrencia
    cursor.execute("PRAGMA journal_mode=WAL;")
    print("✓ Modo WAL activado")
    
    # Optimizaciones de rendimiento
    cursor.execute("PRAGMA synchronous=NORMAL;")  # Menos seguro pero más rápido
    cursor.execute("PRAGMA cache_size=10000;")  # 10MB de caché
    cursor.execute("PRAGMA temp_store=MEMORY;")  # Temporales en memoria
    cursor.execute("PRAGMA mmap_size=30000000000;")  # Memory-mapped I/O
    cursor.execute("PRAGMA page_size=4096;")  # Tamaño de página óptimo
    
    print("✓ Pragmas de optimización aplicados")
    
    # Verificar configuración
    result = cursor.execute("PRAGMA journal_mode;").fetchone()
    print(f"✓ Journal mode: {result[0]}")
    
    result = cursor.execute("PRAGMA synchronous;").fetchone()
    print(f"✓ Synchronous: {result[0]}")
    
    conn.commit()
    conn.close()
    print("\n✅ Base de datos optimizada correctamente")

if __name__ == "__main__":
    optimizar_sqlite()
