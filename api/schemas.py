from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MedicionBase(BaseModel):
    distancia: Optional[float] = None


class MedicionCreate(MedicionBase):
    timestamp: Optional[float] = None  # Unix timestamp desde la placa


class MedicionResponse(BaseModel):
    id: int
    timestamp: datetime
    velocidad_ms: Optional[float] = None
    velocidad_kmh: Optional[float] = None
    distancia: float
    tiempo_recorrido: Optional[float] = None
    es_primera_medicion: bool
    medicion_completa: bool

    class Config:
        from_attributes = True


class ConfiguracionBase(BaseModel):
    clave: str
    valor: str
    descripcion: Optional[str] = None


class ConfiguracionResponse(ConfiguracionBase):
    id: int

    class Config:
        from_attributes = True


class ConfiguracionUpdate(BaseModel):
    valor: str


class EstadisticasResponse(BaseModel):
    total_mediciones: int
    velocidad_promedio_kmh: Optional[float] = None
    velocidad_maxima_kmh: Optional[float] = None
    velocidad_minima_kmh: Optional[float] = None
    mediciones_hoy: int
    excesos_velocidad: int
