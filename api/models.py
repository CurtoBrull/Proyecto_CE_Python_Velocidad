from sqlalchemy import Column, Integer, Float, DateTime, Boolean, String
from datetime import datetime
from database import Base


class Medicion(Base):
    __tablename__ = "mediciones"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    velocidad_ms = Column(Float, nullable=True)
    velocidad_kmh = Column(Float, nullable=True)
    distancia = Column(Float, default=100.0)
    tiempo_recorrido = Column(Float, nullable=True)
    es_primera_medicion = Column(Boolean, default=False)
    medicion_completa = Column(Boolean, default=False)


class Configuracion(Base):
    __tablename__ = "configuracion"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(50), unique=True, index=True)
    valor = Column(String(100))
    descripcion = Column(String(200), nullable=True)
