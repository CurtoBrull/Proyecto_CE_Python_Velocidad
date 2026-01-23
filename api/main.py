from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List, Optional

from database import engine, get_db, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Radar de Velocidad API",
    description="API para el sistema de radar de velocidad con sensores Arduino",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_configuracion(db: Session):
    config = db.query(models.Configuracion).filter(
        models.Configuracion.clave == "distancia_sensores"
    ).first()
    if not config:
        config = models.Configuracion(
            clave="distancia_sensores",
            valor="100",
            descripcion="Distancia en metros entre los dos sensores"
        )
        db.add(config)
        db.commit()


@app.on_event("startup")
def startup_event():
    db = next(get_db())
    init_configuracion(db)
    db.close()


def get_distancia_sensores(db: Session) -> float:
    config = db.query(models.Configuracion).filter(
        models.Configuracion.clave == "distancia_sensores"
    ).first()
    return float(config.valor) if config else 100.0


@app.post("/mediciones/", response_model=schemas.MedicionResponse)
def registrar_medicion(db: Session = Depends(get_db)):
    timestamp_actual = datetime.now()
    distancia = get_distancia_sensores(db)

    medicion_pendiente = db.query(models.Medicion).filter(
        models.Medicion.es_primera_medicion == True,
        models.Medicion.medicion_completa == False
    ).first()

    if medicion_pendiente:
        tiempo_recorrido = (timestamp_actual - medicion_pendiente.timestamp).total_seconds()
        velocidad_ms = distancia / tiempo_recorrido
        velocidad_kmh = velocidad_ms * 3.6

        medicion_pendiente.velocidad_ms = velocidad_ms
        medicion_pendiente.velocidad_kmh = velocidad_kmh
        medicion_pendiente.tiempo_recorrido = tiempo_recorrido
        medicion_pendiente.medicion_completa = True
        medicion_pendiente.es_primera_medicion = False

        db.commit()
        db.refresh(medicion_pendiente)
        return medicion_pendiente
    else:
        nueva_medicion = models.Medicion(
            timestamp=timestamp_actual,
            distancia=distancia,
            es_primera_medicion=True,
            medicion_completa=False
        )
        db.add(nueva_medicion)
        db.commit()
        db.refresh(nueva_medicion)
        return nueva_medicion


@app.get("/mediciones/", response_model=List[schemas.MedicionResponse])
def listar_mediciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    solo_completas: bool = Query(True),
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Medicion)

    if solo_completas:
        query = query.filter(models.Medicion.medicion_completa == True)

    if fecha_inicio:
        query = query.filter(func.date(models.Medicion.timestamp) >= fecha_inicio)
    if fecha_fin:
        query = query.filter(func.date(models.Medicion.timestamp) <= fecha_fin)

    return query.order_by(models.Medicion.timestamp.desc()).offset(skip).limit(limit).all()


@app.get("/mediciones/{medicion_id}", response_model=schemas.MedicionResponse)
def obtener_medicion(medicion_id: int, db: Session = Depends(get_db)):
    medicion = db.query(models.Medicion).filter(models.Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medicion no encontrada")
    return medicion


@app.get("/estadisticas/", response_model=schemas.EstadisticasResponse)
def obtener_estadisticas(db: Session = Depends(get_db)):
    mediciones_completas = db.query(models.Medicion).filter(
        models.Medicion.medicion_completa == True
    )

    total = mediciones_completas.count()

    stats = db.query(
        func.avg(models.Medicion.velocidad_kmh).label("promedio"),
        func.max(models.Medicion.velocidad_kmh).label("maxima"),
        func.min(models.Medicion.velocidad_kmh).label("minima")
    ).filter(models.Medicion.medicion_completa == True).first()

    hoy = date.today()
    mediciones_hoy = mediciones_completas.filter(
        func.date(models.Medicion.timestamp) == hoy
    ).count()

    excesos = mediciones_completas.filter(
        models.Medicion.velocidad_kmh > 50
    ).count()

    return schemas.EstadisticasResponse(
        total_mediciones=total,
        velocidad_promedio_kmh=round(stats.promedio, 2) if stats.promedio else None,
        velocidad_maxima_kmh=round(stats.maxima, 2) if stats.maxima else None,
        velocidad_minima_kmh=round(stats.minima, 2) if stats.minima else None,
        mediciones_hoy=mediciones_hoy,
        excesos_velocidad=excesos
    )


@app.get("/configuracion/", response_model=List[schemas.ConfiguracionResponse])
def listar_configuracion(db: Session = Depends(get_db)):
    return db.query(models.Configuracion).all()


@app.get("/configuracion/{clave}", response_model=schemas.ConfiguracionResponse)
def obtener_configuracion(clave: str, db: Session = Depends(get_db)):
    config = db.query(models.Configuracion).filter(
        models.Configuracion.clave == clave
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return config


@app.put("/configuracion/{clave}", response_model=schemas.ConfiguracionResponse)
def actualizar_configuracion(
    clave: str,
    config_update: schemas.ConfiguracionUpdate,
    db: Session = Depends(get_db)
):
    config = db.query(models.Configuracion).filter(
        models.Configuracion.clave == clave
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")

    config.valor = config_update.valor
    db.commit()
    db.refresh(config)
    return config


@app.post("/", response_model=schemas.MedicionResponse)
def endpoint_legacy(db: Session = Depends(get_db)):
    return registrar_medicion(db)
