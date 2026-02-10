from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer, case
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from typing import List, Optional
import os

from database import engine, get_db, Base
import models
import schemas

MEDICION_INICIADA = False

# Cache en memoria para configuración
_config_cache = {"distancia_sensores": None, "limite_velocidad": None}

# Almacenamiento del último POST recibido para mostrar en tiempo real
_ultimo_post = {"timestamp": None, "data": None}

app = FastAPI(
    title="Radar de Velocidad API",
    description="API para el sistema de radar de velocidad con sensores Arduino",
    version="1.0.0"
)

# CORS Configuration
# Allow origins from environment variable or default to local development + Render URLs
allowed_origins = [
    "http://localhost:8000",           # Local development
    "http://127.0.0.1:8000",          # Local development alternative
    "http://frontend:8000",             # Docker Compose
    "https://radarpython.onrender.com", # Render frontend
    os.getenv("FRONTEND_URL", ""),      # Environment variable for flexibility
]

# Remove empty strings from allowed_origins
allowed_origins = [origin for origin in allowed_origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_configuracion(db: Session):
    """
    Inicializa la configuración por defecto en la base de datos.

    Esta función verifica si existe una configuración con la clave 'distancia_sensores'.
    Si no existe, crea una nueva entrada en la tabla Configuracion con valores por defecto:
    - Clave: 'distancia_sensores'
    - Valor: '100' (distancia en metros)
    - Descripción: 'Distancia en metros entre los dos sensores'

    Parámetros:
    - db (Session): Sesión de base de datos de SQLAlchemy para realizar operaciones.

    Retorno:
    - None: No retorna ningún valor, solo modifica la base de datos.

    Esta función se ejecuta automáticamente al iniciar la aplicación para asegurar
    que la configuración básica esté presente.
    """
    # Inicializar distancia_sensores
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
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

    # Inicializar limite_velocidad
    limite = db.query(models.Configuracion).filter(
        models.Configuracion.clave == "limite_velocidad"
    ).first()
    if not limite:
        limite = models.Configuracion(
            clave="limite_velocidad",
            valor="50",
            descripcion="Limite de velocidad en km/h"
        )
        db.add(limite)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        # Inicializar configuración en DB (ya verifica duplicados)
        init_configuracion(db)

        # Cargar configuración en cache
        config = db.query(models.Configuracion).filter(
            models.Configuracion.clave == "distancia_sensores"
        ).first()
        _config_cache["distancia_sensores"] = float(config.valor) if config else 100.0

        limite = db.query(models.Configuracion).filter(
            models.Configuracion.clave == "limite_velocidad"
        ).first()
        _config_cache["limite_velocidad"] = float(limite.valor) if limite else 50.0



def get_distancia_sensores() -> float:
    """
    Obtiene la distancia configurada entre los dos sensores desde la cache en memoria.

    Esta función retorna el valor cacheado de 'distancia_sensores'. Si no está en cache,
    retorna un valor por defecto de 100.0 metros.

    Retorno:
    - float: La distancia en metros entre los sensores.
    """
    return _config_cache.get("distancia_sensores", 100.0)


@app.post("/mediciones/", response_model=schemas.MedicionResponse)
def registrar_medicion(
    medicion: schemas.MedicionCreate = None,
    db: Session = Depends(get_db)
):
    """
    Registra una nueva medición de velocidad o completa una medición pendiente.

    Esta función maneja la lógica principal del sistema de radar de velocidad.
    Cuando se llama, verifica si hay una medición pendiente (primera medición sin completar).
    Si existe una medición pendiente, calcula la velocidad basándose en el tiempo
    transcurrido entre la primera y segunda detección, y completa la medición.
    Si no hay medición pendiente, crea una nueva medición como primera detección.

    Parámetros:
    - medicion (MedicionCreate): Datos opcionales de la medición (timestamp desde la placa).
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - MedicionResponse: Un objeto de respuesta que contiene los detalles de la medición
      registrada o completada, incluyendo timestamp, distancia, velocidades calculadas, etc.

    Lógica de funcionamiento:
    1. Obtiene el timestamp actual y la distancia entre sensores.
    2. Busca una medición pendiente (es_primera_medicion=True, medicion_completa=False).
    3. Si encuentra una pendiente:
       - Calcula el tiempo recorrido en segundos.
       - Calcula velocidad en m/s: distancia / tiempo.
       - Calcula velocidad en km/h: velocidad_ms * 3.6.
       - Actualiza la medición con los valores calculados y marca como completa.
    4. Si no hay pendiente:
       - Crea una nueva medición con el timestamp actual, distancia, y marca como primera medición incompleta.

    Esta función asume que las llamadas alternan entre detecciones de los dos sensores.
    """
    # Obtener timestamp y distancia
    if medicion and medicion.detector1:
        timestamp_actual = medicion.detector1
    elif medicion and medicion.detector2:
        timestamp_actual = medicion.detector2
    else:
        timestamp_actual = datetime.now()
    
    distancia = get_distancia_sensores()

    # Buscar si hay una medición pendiente
    medicion_pendiente = db.query(models.Medicion).filter(
        models.Medicion.es_primera_medicion == True,
        models.Medicion.medicion_completa == False
    ).first()

    if medicion_pendiente:
        # Completar la medición pendiente
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
        
        # Guardar en memoria para mostrar en tiempo real
        _ultimo_post["timestamp"] = datetime.now().isoformat()
        _ultimo_post["data"] = {
            "id": medicion_pendiente.id,
            "timestamp": medicion_pendiente.timestamp.isoformat(),
            "distancia": medicion_pendiente.distancia,
            "velocidad_ms": medicion_pendiente.velocidad_ms,
            "velocidad_kmh": medicion_pendiente.velocidad_kmh,
            "tiempo_recorrido": medicion_pendiente.tiempo_recorrido,
            "medicion_completa": True,
            "es_primera_medicion": False
        }
        
        return medicion_pendiente
    else:
        # Crear nueva medición
        nueva_medicion = models.Medicion(
            timestamp=timestamp_actual,
            distancia=distancia,
            es_primera_medicion=True,
            medicion_completa=False
        )
        db.add(nueva_medicion)
        db.commit()
        db.refresh(nueva_medicion)
        
        # Guardar en memoria para mostrar en tiempo real
        _ultimo_post["timestamp"] = datetime.now().isoformat()
        _ultimo_post["data"] = {
            "id": nueva_medicion.id,
            "timestamp": nueva_medicion.timestamp.isoformat(),
            "distancia": nueva_medicion.distancia,
            "velocidad_ms": None,
            "velocidad_kmh": None,
            "tiempo_recorrido": None,
            "medicion_completa": False,
            "es_primera_medicion": True,
            "mensaje": "Sensor 1 activado. Esperando sensor 2..."
        }
        
        return nueva_medicion


@app.get("/ultimo-post/")
def obtener_ultimo_post():
    """
    Devuelve el último POST recibido en /mediciones/ para mostrar en tiempo real.
    
    Este endpoint es usado por auto.html para mostrar los datos que llegan
    de los sensores en tiempo real.
    """
    if _ultimo_post["data"] is None:
        return {"mensaje": "No hay datos aún", "data": None}
    return _ultimo_post


@app.get("/mediciones/", response_model=List[schemas.MedicionResponse])
def listar_mediciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    solo_completas: bool = Query(True),
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Lista las mediciones de velocidad con opciones de filtrado y paginación.

    Esta función permite obtener una lista de mediciones almacenadas en la base de datos,
    con la posibilidad de aplicar filtros por estado de completitud, rango de fechas,
    y controlar la paginación mediante skip y limit.

    Parámetros de consulta:
    - skip (int): Número de registros a saltar (para paginación). Por defecto 0. Debe ser >= 0.
    - limit (int): Número máximo de registros a retornar. Por defecto 20. Debe estar entre 1 y 100.
    - solo_completas (bool): Si True, solo retorna mediciones completas (con velocidad calculada).
      Por defecto True.
    - fecha_inicio (date, opcional): Fecha de inicio para filtrar mediciones (formato YYYY-MM-DD).
      Si se proporciona, solo incluye mediciones desde esta fecha inclusive.
    - fecha_fin (date, opcional): Fecha de fin para filtrar mediciones (formato YYYY-MM-DD).
      Si se proporciona, solo incluye mediciones hasta esta fecha inclusive.
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - List[MedicionResponse]: Lista de objetos MedicionResponse ordenados por timestamp descendente
      (más recientes primero), aplicando los filtros y límites especificados.

    La función construye una consulta SQLAlchemy dinámicamente aplicando los filtros
    solicitados y retorna los resultados paginados.
    """
    query = db.query(models.Medicion)

    if solo_completas:
        query = query.filter(models.Medicion.medicion_completa == True)

    if fecha_inicio:
        inicio = datetime.combine(fecha_inicio, datetime.min.time())
        query = query.filter(models.Medicion.timestamp >= inicio)
    if fecha_fin:
        fin = datetime.combine(fecha_fin, datetime.max.time())
        query = query.filter(models.Medicion.timestamp <= fin)

    return query.order_by(models.Medicion.timestamp.desc()).offset(skip).limit(limit).all()


@app.get("/mediciones/{medicion_id}", response_model=schemas.MedicionResponse)
def obtener_medicion(medicion_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una medición específica por su ID.

    Esta función busca en la base de datos una medición con el ID proporcionado.
    Si la medición existe, la retorna; si no, lanza una excepción HTTP 404.

    Parámetros:
    - medicion_id (int): El ID único de la medición a obtener. Se extrae de la URL.
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - MedicionResponse: Un objeto que contiene todos los detalles de la medición encontrada,
      incluyendo timestamp, distancia, velocidades calculadas, etc.

    Excepciones:
    - HTTPException (404): Se lanza si no se encuentra una medición con el ID especificado,
      con el mensaje "Medicion no encontrada".

    Esta función es útil para obtener detalles completos de una medición específica,
    por ejemplo, para mostrar en una interfaz de usuario o para análisis detallado.
    """
    medicion = db.query(models.Medicion).filter(models.Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medicion no encontrada")
    return medicion


@app.get("/estadisticas/", response_model=schemas.EstadisticasResponse)
def obtener_estadisticas(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas generales de todas las mediciones completas.

    Esta función calcula y retorna estadísticas agregadas de todas las mediciones
    de velocidad que han sido completadas (es decir, que tienen velocidad calculada).
    Incluye promedios, máximos, mínimos, conteos por día y excesos de velocidad.

    Parámetros:
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - EstadisticasResponse: Un objeto que contiene las siguientes estadísticas:
      - total_mediciones: Número total de mediciones completas.
      - velocidad_promedio_kmh: Velocidad promedio en km/h (redondeada a 2 decimales).
      - velocidad_maxima_kmh: Velocidad máxima registrada en km/h (redondeada a 2 decimales).
      - velocidad_minima_kmh: Velocidad mínima registrada en km/h (redondeada a 2 decimales).
      - mediciones_hoy: Número de mediciones completas realizadas hoy.
      - excesos_velocidad: Número de mediciones donde la velocidad supera los 50 km/h.

    Cálculos realizados:
    - Consulta todas las mediciones completas.
    - Calcula estadísticas agregadas usando funciones SQL (AVG, MAX, MIN).
    - Filtra mediciones del día actual usando la fecha de hoy.
    - Cuenta excesos de velocidad (mayor a 50 km/h).
    - Redondea los valores de velocidad a 2 decimales para presentación.

    Si no hay mediciones completas, los valores de velocidad serán None.
    """
    hoy = date.today()
    inicio_hoy = datetime.combine(hoy, datetime.min.time())
    fin_hoy = datetime.combine(hoy, datetime.max.time())

    # Query única consolidada
    stats = db.query(
        func.count(models.Medicion.id).label("total"),
        func.avg(models.Medicion.velocidad_kmh).label("promedio"),
        func.max(models.Medicion.velocidad_kmh).label("maxima"),
        func.min(models.Medicion.velocidad_kmh).label("minima"),
        func.sum(
            case((
                (models.Medicion.timestamp >= inicio_hoy) &
                (models.Medicion.timestamp <= fin_hoy), 1
            ), else_=0)
        ).label("mediciones_hoy"),
        func.sum(
            case((models.Medicion.velocidad_kmh > 50, 1), else_=0)
        ).label("excesos")
    ).filter(models.Medicion.medicion_completa == True).first()

    return schemas.EstadisticasResponse(
        total_mediciones=stats.total or 0,
        velocidad_promedio_kmh=round(stats.promedio, 2) if stats.promedio else None,
        velocidad_maxima_kmh=round(stats.maxima, 2) if stats.maxima else None,
        velocidad_minima_kmh=round(stats.minima, 2) if stats.minima else None,
        mediciones_hoy=stats.mediciones_hoy or 0,
        excesos_velocidad=stats.excesos or 0
    )


@app.get("/configuracion/", response_model=List[schemas.ConfiguracionResponse])
def listar_configuracion(db: Session = Depends(get_db)):
    """
    Lista todas las configuraciones almacenadas en la base de datos.

    Esta función retorna una lista completa de todas las entradas en la tabla
    Configuracion, incluyendo claves, valores y descripciones.

    Parámetros:
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - List[ConfiguracionResponse]: Lista de objetos ConfiguracionResponse que contienen
      todas las configuraciones del sistema.

    Esta función es útil para obtener una vista general de todos los parámetros
    configurables del sistema, como la distancia entre sensores u otras opciones.
    """
    return db.query(models.Configuracion).all()


@app.get("/configuracion/{clave}", response_model=schemas.ConfiguracionResponse)
def obtener_configuracion(clave: str, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una configuración específica por su clave.

    Esta función busca en la base de datos una configuración con la clave proporcionada.
    Si la configuración existe, la retorna; si no, lanza una excepción HTTP 404.

    Parámetros:
    - clave (str): La clave única de la configuración a obtener. Se extrae de la URL.
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - ConfiguracionResponse: Un objeto que contiene los detalles de la configuración
      encontrada, incluyendo clave, valor y descripción.

    Excepciones:
    - HTTPException (404): Se lanza si no se encuentra una configuración con la clave
      especificada, con el mensaje "Configuracion no encontrada".

    Esta función permite acceder a configuraciones individuales, útil para obtener
    valores específicos como la distancia entre sensores.
    """
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
    """
    Actualiza el valor de una configuración específica por su clave.

    Esta función busca una configuración existente por su clave y actualiza su valor
    con el nuevo valor proporcionado en el cuerpo de la solicitud. Si la configuración
    no existe, lanza una excepción HTTP 404.

    Parámetros:
    - clave (str): La clave única de la configuración a actualizar. Se extrae de la URL.
    - config_update (ConfiguracionUpdate): Objeto que contiene el nuevo valor para la configuración.
      Solo incluye el campo 'valor' que se va a actualizar.
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - ConfiguracionResponse: Un objeto que contiene los detalles actualizados de la configuración,
      incluyendo clave, nuevo valor y descripción.

    Excepciones:
    - HTTPException (404): Se lanza si no se encuentra una configuración con la clave
      especificada, con el mensaje "Configuracion no encontrada".

    La función actualiza solo el campo 'valor' de la configuración, manteniendo la clave
    y descripción originales. Después de la actualización, confirma los cambios en la
    base de datos y refresca el objeto para retornar los datos actualizados.
    """
    config = db.query(models.Configuracion).filter(
        models.Configuracion.clave == clave
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")

    config.valor = config_update.valor
    db.commit()
    db.refresh(config)
    # Actualizar cache
    if clave == "distancia_sensores":
        _config_cache["distancia_sensores"] = float(config.valor)
    elif clave == "limite_velocidad":
        _config_cache["limite_velocidad"] = float(config.valor)
    return config


@app.post("/", response_model=schemas.MedicionResponse)
def endpoint_legacy(db: Session = Depends(get_db)):
    """
    Endpoint legacy para compatibilidad con versiones anteriores.

    Esta función proporciona un endpoint alternativo en la raíz ("/") que realiza
    la misma funcionalidad que el endpoint "/mediciones/" para registrar mediciones.
    Está diseñado para mantener compatibilidad con sistemas o clientes que esperan
    el endpoint en la ruta raíz.

    Parámetros:
    - db (Session): Sesión de base de datos inyectada automáticamente por FastAPI.

    Retorno:
    - MedicionResponse: El mismo objeto retornado por registrar_medicion(),
      que contiene los detalles de la medición registrada o completada.

    Esta función simplemente delega la lógica a registrar_medicion(), proporcionando
    una interfaz alternativa para el mismo servicio. Se recomienda usar "/mediciones/"
    para nuevas implementaciones.
    """
    return registrar_medicion(db)
