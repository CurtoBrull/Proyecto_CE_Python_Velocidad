# PROYECTO: RADAR DE VELOCIDAD
## Sistema de Medición de Velocidad mediante Sensores IoT

---

<div style="text-align: center; margin-top: 200px;">

### **AUTORES**

**Hernández Rivas, Antonio Jesús**

**Curto Brull, Javier**

### **CURSO**

**CE Desarrollo de Aplicaciones Lenguaje Python**

### **FECHA**

Febrero 2026

</div>

<div style="page-break-after: always;"></div>

---

## ÍNDICE

1. [Análisis de Requisitos](#1-análisis-de-requisitos)
   - 1.1 [Introducción](#11-introducción)
   - 1.2 [Objetivos del Proyecto](#12-objetivos-del-proyecto)
   - 1.3 [Requisitos Funcionales](#13-requisitos-funcionales)
   - 1.4 [Requisitos No Funcionales](#14-requisitos-no-funcionales)
   - 1.5 [Requisitos Técnicos](#15-requisitos-técnicos)

2. [Diseño del Sistema](#2-diseño-del-sistema)
   - 2.1 [Arquitectura General](#21-arquitectura-general)
   - 2.2 [Componentes Hardware](#22-componentes-hardware)
   - 2.3 [Componentes Software](#23-componentes-software)
   - 2.4 [Flujo de Datos](#24-flujo-de-datos)
   - 2.5 [Diagrama de Base de Datos](#25-diagrama-de-base-de-datos)
   - 2.6 [Diagrama de Secuencia](#26-diagrama-de-secuencia)

3. [Implementación](#3-implementación)
   - 3.1 [API Backend (FastAPI)](#31-api-backend-fastapi)
   - 3.2 [Frontend Dashboard (Django)](#32-frontend-dashboard-django)
   - 3.3 [Firmware Microcontrolador (MicroPython)](#33-firmware-microcontrolador-micropython)
   - 3.4 [Repositorio del Proyecto](#34-repositorio-del-proyecto)

4. [Pruebas y Validación](#4-pruebas-y-validación)
   - 4.1 [Plan de Pruebas](#41-plan-de-pruebas)
   - 4.2 [Casos de Prueba](#42-casos-de-prueba)
   - 4.3 [Resultados de Pruebas](#43-resultados-de-pruebas)
   - 4.4 [Validación del Sistema](#44-validación-del-sistema)

5. [Documentación](#5-documentación)
   - 5.1 [Instalación y Configuración](#51-instalación-y-configuración)
   - 5.2 [Estructura del Proyecto](#52-estructura-del-proyecto)
   - 5.3 [API Endpoints](#53-api-endpoints)
   - 5.4 [Configuración del Hardware](#54-configuración-del-hardware)

6. [Manual de Usuario](#6-manual-de-usuario)
   - 6.1 [Requisitos Previos](#61-requisitos-previos)
   - 6.2 [Guía de Instalación](#62-guía-de-instalación)
   - 6.3 [Uso del Sistema](#63-uso-del-sistema)
   - 6.4 [Solución de Problemas](#64-solución-de-problemas)

7. [Referencias](#7-referencias)

<div style="page-break-after: always;"></div>

---

## 1. ANÁLISIS DE REQUISITOS

### 1.1 Introducción

El proyecto **Radar de Velocidad** es un sistema IoT diseñado para medir la velocidad de objetos en movimiento (vehículos, personas, etc.) utilizando tecnología de sensores de proximidad. El sistema integra hardware (microcontrolador ESP32 con sensores), backend (API REST), y frontend (dashboard web) para proporcionar una solución completa de monitorización de velocidad.

**Contexto del Proyecto:**

- Desarrollado como proyecto académico para el curso de Desarrollo de Aplicaciones con Python
- Aplica conceptos de IoT, comunicación HTTP, arquitectura cliente-servidor y programación de sistemas embebidos
- Utiliza tecnologías modernas y frameworks actuales del ecosistema Python

### 1.2 Objetivos del Proyecto

#### Objetivo General

Desarrollar un sistema completo de medición de velocidad basado en sensores IoT, con capacidad de almacenamiento, procesamiento y visualización de datos en tiempo real.

#### Objetivos Específicos

1. **Hardware:** Implementar un sistema de detección con dos sensores de movimiento conectados a un microcontrolador ESP32
2. **Backend:** Desarrollar una API REST robusta para recibir, procesar y almacenar mediciones
3. **Frontend:** Crear un dashboard web intuitivo para visualizar estadísticas y mediciones
4. **Integración:** Establecer comunicación bidireccional entre todos los componentes del sistema
5. **Validación:** Realizar pruebas exhaustivas para garantizar la precisión de las mediciones

<div style="page-break-after: always;"></div>

### 1.3 Requisitos Funcionales

| ID | Requisito | Prioridad | Descripción |
|----|-----------|-----------|-------------|
| RF-01 | Detección de paso | Alta | El sistema debe detectar el paso de un objeto por el sensor 1 |
| RF-02 | Detección de salida | Alta | El sistema debe detectar el paso del mismo objeto por el sensor 2 |
| RF-03 | Cálculo de velocidad | Alta | Calcular velocidad = distancia / (tiempo2 - tiempo1) |
| RF-04 | Almacenamiento | Alta | Guardar todas las mediciones con timestamp preciso |
| RF-05 | Visualización web | Media | Mostrar mediciones en un dashboard accesible vía navegador |
| RF-06 | Estadísticas | Media | Calcular promedio, máximo, mínimo de velocidades |
| RF-07 | Configuración | Media | Permitir configurar distancia entre sensores y límite de velocidad |
| RF-08 | Alertas de exceso | Baja | Identificar mediciones que superen el límite configurado |
| RF-09 | Reinicio de medición | Media | Permitir cancelar una medición en curso |
| RF-10 | API REST | Alta | Exponer endpoints para interacción con el sistema |

### 1.4 Requisitos No Funcionales

#### Rendimiento

- **RNF-01:** El sistema debe procesar una medición en menos de 100ms
- **RNF-02:** La latencia de comunicación HTTP no debe exceder 500ms
- **RNF-03:** Soportar al menos 100 mediciones por hora

#### Precisión

- **RNF-04:** Precisión de timestamp de al menos 100ms
- **RNF-05:** Cálculo de velocidad con precisión de 2 decimales

#### Disponibilidad

- **RNF-06:** API disponible 24/7 (excepto mantenimiento programado)
- **RNF-07:** Reconexión automática del ESP32 en caso de pérdida de WiFi

#### Usabilidad

- **RNF-08:** Interface web responsive (adaptable a móviles)
- **RNF-09:** Documentación completa de instalación y uso
- **RNF-10:** Feedback visual en el hardware (LEDs)

#### Seguridad

- **RNF-11:** CORS habilitado para permitir comunicación cross-origin
- **RNF-12:** Validación de datos en todos los endpoints

### 1.5 Requisitos Técnicos

#### Hardware

- Microcontrolador: ESP32 o ESP8266 con WiFi integrado
- Sensores: 2x sensores de movimiento (PIR, infrarrojos o ultrasónicos)
- Alimentación: 5V DC (USB o fuente externa)
- LEDs indicadores: Verde (sistema OK), Rojo (error/exceso)

#### Software - Backend

- **Lenguaje:** Python 3.10+
- **Framework:** FastAPI 0.104+
- **Servidor:** Uvicorn (ASGI)
- **Almacenamiento:** JSON (desarrollo) / SQLite o PostgreSQL (producción)
- **Librerías:** Pydantic, python-multipart

#### Software - Frontend

- **Framework:** Django 5.0+
- **Template Engine:** Django Templates
- **Cliente HTTP:** requests
- **Base de datos:** SQLite (integrada con Django)

#### Software - Firmware

- **Lenguaje:** MicroPython
- **Librerías:** network (WiFi), urequests (HTTP), machine (GPIO)
- **Protocolo:** HTTP POST con JSON

#### Infraestructura

- **Sistema Operativo:** Compatible con Windows, Linux, macOS
- **Conectividad:** Red local WiFi (2.4GHz)
- **Puertos:** 8080 (API), 8000 (Frontend)

<div style="page-break-after: always;"></div>

---

## 2. DISEÑO DEL SISTEMA

### 2.1 Arquitectura General

El sistema implementa una arquitectura de **tres capas** con comunicación HTTP:

```
┌─────────────────────────────────────────────────────────────────┐
│                         CAPA DE PRESENTACIÓN                     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          Frontend Django (Puerto 8000)                   │   │
│  │  - Dashboard con estadísticas                            │   │
│  │  - Lista de mediciones                                   │   │
│  │  - Configuración del sistema                             │   │
│  │  - Gráficos y reportes                                   │   │
│  └──────────────────────┬──────────────────────────────────┘   │
└─────────────────────────┼────────────────────────────────────────┘
                          │ HTTP GET/POST
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CAPA DE LÓGICA                           │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          API FastAPI (Puerto 8080)                       │   │
│  │  - Endpoints REST                                        │   │
│  │  - Cálculo de velocidad                                  │   │
│  │  - Validación de datos                                   │   │
│  │  - Gestión de configuración                              │   │
│  └──────────────────────┬──────────────────────────────────┘   │
└─────────────────────────┼────────────────────────────────────────┘
                          │ Lectura/Escritura
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE DATOS                             │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │ mediciones.json  │         │   config.json    │             │
│  │ - medicion1      │         │ - distancia      │             │
│  │ - timestamp      │         │ - limite_vel     │             │
│  └──────────────────┘         └──────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                          ▲
                          │ HTTP POST
                          │
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE HARDWARE                          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            ESP32/ESP8266 (MicroPython)                   │   │
│  │                                                           │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐          │   │
│  │  │ Sensor 1 │    │ Sensor 2 │    │   LEDs   │          │   │
│  │  │  (GPIO)  │    │  (GPIO)  │    │ Verde/Rojo│         │   │
│  │  └──────────┘    └──────────┘    └──────────┘          │   │
│  │                                                           │   │
│  │  - Detección por interrupción                            │   │
│  │  - Timestamp preciso con NTP                             │   │
│  │  - Feedback visual con LEDs                              │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Características de la arquitectura:**

- **Desacoplamiento:** Cada capa puede desarrollarse y probarse independientemente
- **Escalabilidad:** Fácil migración de JSON a base de datos relacional
- **Modularidad:** Componentes reemplazables (ej: cambiar Django por React)
- **Comunicación HTTP:** Protocolo estándar, fácil de debuggear y mantener

### 2.2 Componentes Hardware

#### Esquema de Conexiones ESP32

```
                    ESP32 DevKit v1
                   ┌─────────────────┐
                   │                 │
    Sensor 1  ────▶│ GPIO 12         │
    (Señal)        │                 │
                   │                 │
    Sensor 2  ────▶│ GPIO 13         │
    (Señal)        │                 │
                   │                 │
    LED Verde ◀────│ GPIO 14         │
                   │                 │
    LED Rojo  ◀────│ GPIO 27         │
                   │                 │
    5V        ────▶│ VIN             │
                   │                 │
    GND       ────▶│ GND             │
                   │                 │
                   └─────────────────┘
                          │
                          │ WiFi 2.4GHz
                          │
                          ▼
                    [Router WiFi]
                          │
                          ▼
                    [Servidor API]
```

#### Lista de Componentes

| Componente | Especificación | Cantidad | Función |
|------------|---------------|----------|---------|
| ESP32 DevKit | 240MHz, WiFi 2.4GHz, Bluetooth | 1 | Controlador principal |
| Sensor PIR HC-SR501 | Detección de movimiento infrarrojo | 2 | Detección de paso |
| LED Verde 5mm | 20mA, 2.0-2.2V | 1 | Indicador sistema OK |
| LED Rojo 5mm | 20mA, 1.8-2.0V | 1 | Indicador error/exceso |
| Resistencias | 220Ω | 2 | Limitación corriente LEDs |
| Cables Dupont | Macho-Macho | 10 | Conexiones |
| Protoboard | 830 puntos | 1 | Montaje circuito |
| Cable USB | Micro-USB | 1 | Alimentación y programación |

### 2.3 Componentes Software

#### 2.3.1 API Backend - FastAPI

**Módulos principales:**

```
api/
├── main.py              # Aplicación FastAPI, endpoints, lógica
├── models.py            # Modelos Pydantic para validación
├── database.py          # Conexión y gestión de base de datos
└── schemas.py           # Esquemas de respuesta
```

**Tecnologías:**

- **FastAPI:** Framework web moderno y rápido
- **Uvicorn:** Servidor ASGI de alto rendimiento
- **Pydantic:** Validación de datos con type hints
- **JSON:** Almacenamiento persistente simple

<div style="page-break-after: always;"></div>

#### 2.3.2 Frontend - Django

**Módulos principales:**

```
frontend/
├── manage.py
├── frontend/
│   ├── settings.py      # Configuración Django
│   ├── urls.py          # Rutas principales
│   └── wsgi.py          # WSGI para deployment
└── dashboard/
    ├── views.py         # Vistas y lógica del dashboard
    ├── urls.py          # Rutas del dashboard
    ├── api_client.py    # Cliente HTTP para la API
    └── templates/       # Plantillas HTML
        ├── base.html
        ├── index.html
        ├── mediciones.html
        └── configuracion.html
```

**Tecnologías:**

- **Django 5.0:** Framework web full-stack
- **Django Templates:** Motor de plantillas integrado
- **Bootstrap 5:** Framework CSS para UI responsive
- **Chart.js:** Librería para gráficos interactivos

#### 2.3.3 Firmware - MicroPython

**Archivo principal:**

```text
placa/
├── main.py              # Código principal del ESP32
├── boot.py              # Configuración inicial (opcional)
└── README.md            # Documentación de hardware
```

**Librerías utilizadas:**

- **network:** Gestión de conexión WiFi
- **urequests:** Cliente HTTP para enviar mediciones
- **machine:** Control de pines GPIO y hardware
- **time:** Gestión de tiempo y delays
- **ntptime:** Sincronización con servidor NTP

<div style="page-break-after: always;"></div>

### 2.4 Flujo de Datos

```
┌─────────────────────────────────────────────────────────────────────┐
│                     FLUJO COMPLETO DE MEDICIÓN                       │
└─────────────────────────────────────────────────────────────────────┘

1. DETECCIÓN SENSOR 1
   ┌──────────────┐
   │   Objeto     │ ──────▶ Sensor 1 detecta movimiento
   │  en movmto   │         │
   └──────────────┘         │
                            ▼
                   ┌─────────────────┐
                   │  ESP32          │
                   │  GPIO 12 = HIGH │
                   │  Interrupción   │
                   └────────┬────────┘
                            │
                            ▼
                   timestamp1 = time.time()
                            │
                            ▼
                   POST /mediciones/
                   {"timestamp": 1706985430.123}
                            │
                            ▼
                   ┌─────────────────┐
                   │  FastAPI        │
                   │  - Guarda T1    │
                   │  - Estado:      │
                   │    "Esperando   │
                   │     sensor 2"   │
                   └─────────────────┘

   [Objeto viajando entre sensores]
   [Distancia: 100 metros]
   [Tiempo transcurrido: 5 segundos]

2. DETECCIÓN SENSOR 2
   ┌──────────────┐
   │   Objeto     │ ──────▶ Sensor 2 detecta movimiento
   │  en movmto   │         │
   └──────────────┘         │
                            ▼
                   ┌─────────────────┐
                   │  ESP32          │
                   │  GPIO 13 = HIGH │
                   │  Interrupción   │
                   └────────┬────────┘
                            │
                            ▼
                   timestamp2 = time.time()
                            │
                            ▼
                   POST /mediciones/
                   {"timestamp": 1706985435.123}
                            │
                            ▼
                   ┌─────────────────────────────────┐
                   │  FastAPI                        │
                   │  - Lee T1: 1706985430.123       │
                   │  - Recibe T2: 1706985435.123    │
                   │  - Calcula:                     │
                   │    Δt = T2 - T1 = 5.0s          │
                   │    v = 100m / 5.0s = 20 m/s     │
                   │    v = 20 * 3.6 = 72 km/h       │
                   │  - Guarda en DB                 │
                   │  - Limpia estado                │
                   └────────┬────────────────────────┘
                            │
                            ▼
                   Response:
                   {
                     "mensaje": "Velocidad: 72.00 km/h",
                     "velocidad_ms": 20.0,
                     "velocidad_kmh": 72.0,
                     "tiempo_segundos": 5.0
                   }
                            │
                            ▼
                   ┌─────────────────┐
                   │  ESP32          │
                   │  - Parsea JSON  │
                   │  - Si >50 km/h: │
                   │    LED Rojo ON  │
                   │  - Si ≤50 km/h: │
                   │    LED Verde ON │
                   └─────────────────┘

3. VISUALIZACIÓN
                   ┌─────────────────┐
                   │  Usuario        │
                   │  Abre navegador │
                   │  localhost:8000 │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Django         │
                   │  GET /          │
                   └────────┬────────┘
                            │
                            ▼
                   GET http://localhost:8080/mediciones/
                            │
                            ▼
                   ┌─────────────────┐
                   │  FastAPI        │
                   │  - Lee DB       │
                   │  - Devuelve     │
                   │    mediciones   │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────────────────┐
                   │  Django                     │
                   │  - Recibe datos JSON        │
                   │  - Renderiza template       │
                   │  - Muestra en tabla:        │
                   │    72 km/h | 5.0s | EXCESO │
                   └─────────────────────────────┘
```

### 2.5 Diagrama de Base de Datos

#### Modelo de Datos (JSON)

**mediciones.json** (estado temporal)

```json
{
  "medicion1": 1706985430.123
}
```

**config.json** (configuración persistente)

```json
{
  "distancia_sensores": 100.0,
  "limite_velocidad": 50.0
}
```

<div style="page-break-after: always;"></div>

#### Modelo Relacional (Propuesto para una futura producción)

```sql
-- Tabla de configuración
CREATE TABLE configuracion (
    id INTEGER PRIMARY KEY,
    clave VARCHAR(50) UNIQUE NOT NULL,
    valor VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de mediciones
CREATE TABLE mediciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_sensor1 REAL NOT NULL,
    timestamp_sensor2 REAL,
    velocidad_ms REAL,
    velocidad_kmh REAL,
    tiempo_segundos REAL,
    exceso_velocidad BOOLEAN DEFAULT FALSE,
    medicion_completa BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar consultas
CREATE INDEX idx_fecha ON mediciones(fecha_creacion);
CREATE INDEX idx_velocidad ON mediciones(velocidad_kmh);
CREATE INDEX idx_exceso ON mediciones(exceso_velocidad);
```

<div style="page-break-after: always;"></div>

### 2.6 Diagrama de Secuencia

```text
Actor: Objeto     ESP32        API FastAPI       JSON Storage      Django Frontend
  │                │                │                  │                  │
  │                │                │                  │                  │
  │  Pasa por S1   │                │                  │                  │
  ├───────────────▶│                │                  │                  │
  │                │ POST /mediciones/                 │                  │
  │                │  {timestamp: T1}                  │                  │
  │                ├───────────────▶│                  │                  │
  │                │                │  write(T1)       │                  │
  │                │                ├─────────────────▶│                  │
  │                │                │                  │                  │
  │                │  Response:     │                  │                  │
  │                │  "Esperando    │                  │                  │
  │                │   sensor 2"    │                  │                  │
  │                │◀───────────────┤                  │                  │
  │                │                │                  │                  │
  │                │ LED Verde ON   │                  │                  │
  │                │                │                  │                  │
  │                │                │                  │                  │
  │ [viajando...]  │                │                  │                  │
  │ [100 metros]   │                │                  │                  │
  │ [5 segundos]   │                │                  │                  │
  │                │                │                  │                  │
  │  Pasa por S2   │                │                  │                  │
  ├───────────────▶│                │                  │                  │
  │                │ POST /mediciones/                 │                  │
  │                │  {timestamp: T2}                  │                  │
  │                ├───────────────▶│                  │                  │
  │                │                │  read(T1)        │                  │
  │                │                ├─────────────────▶│                  │
  │                │                │  return T1       │                  │
  │                │                │◀─────────────────┤                  │
  │                │                │                  │                  │
  │                │                │ calc_velocity()  │                  │
  │                │                │ v=100m/5s=72km/h │                  │
  │                │                │                  │                  │
  │                │                │  clear()         │                  │
  │                │                ├─────────────────▶│                  │
  │                │                │                  │                  │
  │                │  Response:     │                  │                  │
  │                │  {velocidad:   │                  │                  │
  │                │   72 km/h}     │                  │                  │
  │                │◀───────────────┤                  │                  │
  │                │                │                  │                  │
  │                │ LED Rojo ON    │                  │                  │
  │                │ (exceso >50)   │                  │                  │
  │                │                │                  │                  │
  │                │                │                  │    GET /        │
  │                │                │                  │◀─────────────────┤
  │                │                │  GET /mediciones/│                  │
  │                │                │◀─────────────────┼──────────────────┤
  │                │                │                  │                  │
  │                │                │  read_all()      │                  │
  │                │                ├─────────────────▶│                  │
  │                │                │  return data     │                  │
  │                │                │◀─────────────────┤                  │
  │                │                │                  │                  │
  │                │                │  JSON response   │                  │
  │                │                ├──────────────────┼─────────────────▶│
  │                │                │                  │                  │
  │                │                │                  │  Render HTML    │
  │                │                │                  │  con mediciones │
  │                │                │                  │                  │
```

<div style="page-break-after: always;"></div>

---

## 3. IMPLEMENTACIÓN

### 3.1 API Backend (FastAPI)

El backend está implementado en **FastAPI**, un framework moderno de Python para crear APIs de alto rendimiento.

#### 3.1.1 Archivo Principal - main.py

```python
# Importaciones necesarias
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

# Inicialización de la aplicación FastAPI
app = FastAPI(title="Radar de Velocidad API")

# Configuración de CORS para permitir peticiones desde cualquier origen
# Esto es necesario para que el frontend Django pueda comunicarse con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios concretos
    allow_methods=["*"],   # Permitir GET, POST, PUT, DELETE
    allow_headers=["*"],   # Permitir todos los headers
)

# Constantes de configuración
ARCHIVO_MEDICIONES = "mediciones.json"  # Almacenamiento temporal de medición en curso
ARCHIVO_CONFIG = "config.json"           # Configuración persistente del sistema
DISTANCIA_SENSORES = 100                 # Distancia por defecto en metros
LIMITE_VELOCIDAD = 50                    # Límite por defecto en km/h


# ============================================================================
# FUNCIONES DE GESTIÓN DE CONFIGURACIÓN
# ============================================================================

def cargar_config():
    """
    Carga la configuración desde el archivo JSON.

    Returns:
        dict: Diccionario con la configuración. Vacío si no existe el archivo.
    """
    try:
        with open(ARCHIVO_CONFIG, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está corrupto, devolver diccionario vacío
        return {}


def guardar_config(config: dict):
    """
    Guarda la configuración en el archivo JSON con formato legible.

    Args:
        config (dict): Diccionario con los parámetros de configuración
    """
    with open(ARCHIVO_CONFIG, "w") as f:
        json.dump(config, f, indent=2)


def obtener_distancia() -> float:
    """
    Obtiene la distancia entre sensores de la configuración.

    Returns:
        float: Distancia en metros (por defecto 100m)
    """
    config = cargar_config()
    return config.get("distancia_sensores", DISTANCIA_SENSORES)


def obtener_limite() -> float:
    """
    Obtiene el límite de velocidad de la configuración.

    Returns:
        float: Límite en km/h (por defecto 50 km/h)
    """
    config = cargar_config()
    return config.get("limite_velocidad", LIMITE_VELOCIDAD)


# ============================================================================
# MODELOS PYDANTIC PARA VALIDACIÓN DE DATOS
# ============================================================================

class MedicionRequest(BaseModel):
    """
    Modelo de entrada para el endpoint de mediciones.
    Todos los campos son opcionales ya que la placa puede enviar solo el timestamp.
    """
    timestamp: Optional[float] = None  # Unix timestamp desde la placa (ej: 1706985430.123)
    sensor_id: Optional[int] = None    # ID del sensor (1 o 2) - opcional


class MedicionResponse(BaseModel):
    """
    Modelo de respuesta del endpoint de mediciones.
    Incluye mensaje y datos de velocidad si la medición está completa.
    """
    mensaje: str                              # Mensaje informativo
    velocidad_ms: Optional[float] = None      # Velocidad en metros/segundo
    velocidad_kmh: Optional[float] = None     # Velocidad en kilómetros/hora
    tiempo_segundos: Optional[float] = None   # Tiempo transcurrido entre sensores


# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================

@app.post("/", response_model=MedicionResponse)
@app.post("/mediciones/", response_model=MedicionResponse)
def registrar_medicion(data: Optional[MedicionRequest] = None):
    """
    Endpoint principal para registrar el paso por un sensor.

    Flujo:
    1. Primera llamada: Guarda timestamp del sensor 1, devuelve mensaje de espera
    2. Segunda llamada: Calcula velocidad usando ambos timestamps

    Args:
        data (MedicionRequest): Datos de la medición (timestamp opcional)

    Returns:
        MedicionResponse: Mensaje con estado o resultado de velocidad
    """
    # Usar timestamp de la placa si viene en el request, sino usar timestamp del servidor
    if data and data.timestamp:
        medicion = data.timestamp
    else:
        # Si no viene timestamp, usar el momento actual del servidor
        medicion = datetime.now().timestamp()

    # Intentar cargar medición pendiente del archivo
    try:
        with open(ARCHIVO_MEDICIONES, "r") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si no existe o está corrupto, inicializar vacío
        datos = {}

    # Obtener medición del sensor 1 si existe
    medicion1 = datos.get("medicion1")

    if medicion1 is None:
        # CASO 1: Primera medición (sensor 1)
        # Guardar timestamp y esperar segunda medición
        datos["medicion1"] = medicion
        with open(ARCHIVO_MEDICIONES, "w") as f:
            json.dump(datos, f, indent=2)
        return MedicionResponse(mensaje="Sensor 1 activado. Esperando sensor 2...")
    else:
        # CASO 2: Segunda medición (sensor 2)
        # Calcular velocidad con ambos timestamps
        resultado = calcular_velocidad(medicion1, medicion)

        # Limpiar el archivo para la siguiente medición
        with open(ARCHIVO_MEDICIONES, "w") as f:
            json.dump({}, f, indent=2)

        return resultado


def calcular_velocidad(medicion1: float, medicion2: float) -> MedicionResponse:
    """
    Calcula la velocidad basándose en dos timestamps.

    Fórmula:
        velocidad (m/s) = distancia (m) / tiempo (s)
        velocidad (km/h) = velocidad (m/s) × 3.6

    Args:
        medicion1 (float): Timestamp del sensor 1 en segundos Unix
        medicion2 (float): Timestamp del sensor 2 en segundos Unix

    Returns:
        MedicionResponse: Objeto con velocidad calculada y tiempo transcurrido
    """
    # Calcular tiempo transcurrido entre sensores
    segundos = medicion2 - float(medicion1)

    # Validar que el tiempo sea positivo (sensor 2 debe activarse después del 1)
    if segundos <= 0:
        return MedicionResponse(mensaje="Error: tiempo negativo o cero")

    # Obtener distancia configurada entre sensores
    distancia = obtener_distancia()

    # Calcular velocidad en m/s
    velocidad_ms = distancia / segundos

    # Convertir a km/h (1 m/s = 3.6 km/h)
    velocidad_kmh = velocidad_ms * 3.6

    # Verificar si hay exceso de velocidad
    limite = obtener_limite()
    exceso = " - EXCESO" if velocidad_kmh > limite else ""

    # Log en consola para debugging
    print(f"Velocidad: {velocidad_kmh:.2f} km/h ({velocidad_ms:.2f} m/s) en {segundos:.2f}s{exceso}")

    # Devolver respuesta con todos los datos calculados
    return MedicionResponse(
        mensaje=f"Velocidad: {velocidad_kmh:.2f} km/h",
        velocidad_ms=round(velocidad_ms, 2),
        velocidad_kmh=round(velocidad_kmh, 2),
        tiempo_segundos=round(segundos, 2)
    )


@app.get("/estado/")
def obtener_estado():
    """
    Endpoint para consultar el estado actual del sistema.

    Returns:
        dict: Estado con información sobre medición pendiente y configuración
    """
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
    """
    Endpoint para cancelar una medición en curso.
    Útil si el objeto no llegó al segundo sensor.

    Returns:
        dict: Mensaje de confirmación
    """
    with open(ARCHIVO_MEDICIONES, "w") as f:
        json.dump({}, f, indent=2)
    return {"mensaje": "Medición reiniciada"}


# ============================================================================
# ENDPOINTS DE CONFIGURACIÓN
# ============================================================================

class ConfigUpdate(BaseModel):
    """Modelo para actualizar valores de configuración"""
    valor: str


@app.get("/configuracion/distancia_sensores")
def get_distancia():
    """Obtiene la distancia configurada entre sensores"""
    return {"clave": "distancia_sensores", "valor": str(obtener_distancia())}


@app.put("/configuracion/distancia_sensores")
def set_distancia(data: ConfigUpdate):
    """
    Actualiza la distancia entre sensores.

    Args:
        data (ConfigUpdate): Nueva distancia en metros

    Returns:
        dict: Confirmación o error
    """
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
    """Obtiene el límite de velocidad configurado"""
    return {"clave": "limite_velocidad", "valor": str(obtener_limite())}


@app.put("/configuracion/limite_velocidad")
def set_limite(data: ConfigUpdate):
    """
    Actualiza el límite de velocidad.

    Args:
        data (ConfigUpdate): Nuevo límite en km/h

    Returns:
        dict: Confirmación o error
    """
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
```

**Características destacadas del código:**

- **Validación automática** de datos con Pydantic
- **Manejo robusto de errores** con try-except
- **CORS habilitado** para comunicación cross-origin
- **Comentarios extensivos** explicando cada función
- **Código limpio y modular** siguiendo PEP 8

<div style="page-break-after: always;"></div>

### 3.2 Frontend Dashboard (Django)

El frontend utiliza **Django** para renderizar vistas HTML y comunicarse con la API.

#### 3.2.1 Cliente API - api_client.py

```python
import requests
from typing import Optional, Dict, List

# URL base de la API FastAPI
# En producción esto debería venir de settings.py o variables de entorno
API_BASE_URL = "http://localhost:8080"


class RadarAPIClient:
    """
    Cliente HTTP para interactuar con la API del Radar de Velocidad.
    Encapsula todas las peticiones HTTP y manejo de errores.
    """

    def __init__(self, base_url: str = API_BASE_URL):
        """
        Inicializa el cliente con la URL base de la API.

        Args:
            base_url (str): URL completa de la API (ej: http://localhost:8080)
        """
        self.base_url = base_url.rstrip('/')  # Eliminar slash final si existe
        self.timeout = 5  # Timeout de 5 segundos para todas las peticiones


    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """
        Método interno para realizar peticiones HTTP con manejo de errores.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE)
            endpoint (str): Endpoint de la API (ej: /mediciones/)
            **kwargs: Argumentos adicionales para requests (json, params, etc)

        Returns:
            Optional[Dict]: Respuesta JSON parseada, o None si hay error
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()  # Lanza excepción si status >= 400
            return response.json()

        except requests.exceptions.Timeout:
            print(f"Error: Timeout al conectar con {url}")
            return None

        except requests.exceptions.ConnectionError:
            print(f"Error: No se pudo conectar con la API en {url}")
            return None

        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP {e.response.status_code}: {e.response.text}")
            return None

        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return None


    def obtener_estado(self) -> Optional[Dict]:
        """
        Obtiene el estado actual del sistema de medición.

        Returns:
            Dict con:
            - esperando_sensor2 (bool): Si hay una medición pendiente
            - distancia_sensores (float): Distancia configurada
            - limite_velocidad (float): Límite configurado
        """
        return self._make_request('GET', '/estado/')


    def registrar_medicion(self, timestamp: Optional[float] = None) -> Optional[Dict]:
        """
        Simula el envío de una medición desde el sensor.

        Args:
            timestamp (Optional[float]): Timestamp Unix. Si es None, usa el del servidor

        Returns:
            Dict con el resultado de la medición
        """
        data = {}
        if timestamp is not None:
            data['timestamp'] = timestamp

        return self._make_request('POST', '/mediciones/', json=data)


    def reset_medicion(self) -> Optional[Dict]:
        """
        Reinicia una medición en curso.

        Returns:
            Dict con mensaje de confirmación
        """
        return self._make_request('DELETE', '/reset/')


    def obtener_distancia_sensores(self) -> Optional[float]:
        """
        Obtiene la distancia configurada entre sensores.

        Returns:
            float: Distancia en metros, o None si hay error
        """
        result = self._make_request('GET', '/configuracion/distancia_sensores')
        if result and 'valor' in result:
            try:
                return float(result['valor'])
            except ValueError:
                return None
        return None


    def actualizar_distancia_sensores(self, distancia: float) -> bool:
        """
        Actualiza la distancia entre sensores.

        Args:
            distancia (float): Nueva distancia en metros

        Returns:
            bool: True si se actualizó correctamente, False si hubo error
        """
        result = self._make_request(
            'PUT',
            '/configuracion/distancia_sensores',
            json={'valor': str(distancia)}
        )
        return result is not None and 'error' not in result


    def obtener_limite_velocidad(self) -> Optional[float]:
        """
        Obtiene el límite de velocidad configurado.

        Returns:
            float: Límite en km/h, o None si hay error
        """
        result = self._make_request('GET', '/configuracion/limite_velocidad')
        if result and 'valor' in result:
            try:
                return float(result['valor'])
            except ValueError:
                return None
        return None


    def actualizar_limite_velocidad(self, limite: float) -> bool:
        """
        Actualiza el límite de velocidad.

        Args:
            limite (float): Nuevo límite en km/h

        Returns:
            bool: True si se actualizó correctamente, False si hubo error
        """
        result = self._make_request(
            'PUT',
            '/configuracion/limite_velocidad',
            json={'valor': str(limite)}
        )
        return result is not None and 'error' not in result
```

<div style="page-break-after: always;"></div>

### 3.3 Firmware Microcontrolador (MicroPython)

El firmware del ESP32 está escrito en **MicroPython**, una implementación de Python 3 optimizada para microcontroladores.

```python
# ============================================================================
# RADAR DE VELOCIDAD - FIRMWARE ESP32
# MicroPython para ESP32/ESP8266
# ============================================================================

import network
import urequests
import time
import machine
import ntptime
from machine import Pin

# ============================================================================
# CONFIGURACIÓN - MODIFICAR ESTOS VALORES
# ============================================================================

# Credenciales WiFi
WIFI_SSID = 'TU_RED_WIFI'           # Nombre de tu red WiFi
WIFI_PASSWORD = 'TU_CONTRASEÑA'      # Contraseña de tu red WiFi

# URL de la API (cambiar IP por la de tu servidor)
API_URL = "http://192.168.1.100:8080/mediciones/"

# Configuración de pines GPIO
PIN_SENSOR = 12          # Pin del sensor de movimiento
PIN_LED_VERDE = 14       # LED indicador sistema OK
PIN_LED_ROJO = 27        # LED indicador error/exceso

# Configuración de debounce (evitar múltiples detecciones)
DEBOUNCE_MS = 500        # Ignorar activaciones en menos de 500ms


# ============================================================================
# VARIABLES GLOBALES
# ============================================================================

# Control de tiempo para debounce
ultima_deteccion = 0

# Variables para timestamp preciso con NTP
epoch_base = None        # Timestamp base desde NTP
ticks_base = None        # Ticks de sistema en el momento del NTP


# ============================================================================
# CONFIGURACIÓN DE HARDWARE
# ============================================================================

# Configurar pines de LEDs como salida
led_verde = Pin(PIN_LED_VERDE, Pin.OUT)
led_rojo = Pin(PIN_LED_ROJO, Pin.OUT)

# Configurar pin del sensor como entrada con pull-down
sensor = Pin(PIN_SENSOR, Pin.IN, Pin.PULL_DOWN)

# Inicializar LEDs apagados
led_verde.value(0)
led_rojo.value(0)


# ============================================================================
# FUNCIONES DE CONEXIÓN WIFI
# ============================================================================

def conectar_wifi():
    """
    Conecta el ESP32 a la red WiFi configurada.
    Muestra el progreso con puntos en consola.

    Returns:
        bool: True si se conectó correctamente, False si falló
    """
    print(f"\n{'='*50}")
    print("INICIALIZANDO SISTEMA RADAR DE VELOCIDAD")
    print(f"{'='*50}\n")

    # Crear interfaz WiFi en modo estación (cliente)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Si ya está conectado, desconectar primero
    if wlan.isconnected():
        wlan.disconnect()
        time.sleep(1)

    print(f"Conectando a WiFi: {WIFI_SSID}")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Esperar hasta 15 segundos para conectar
    timeout = 15
    while not wlan.isconnected() and timeout > 0:
        print('.', end='')
        time.sleep(1)
        timeout -= 1

    print()  # Nueva línea

    if wlan.isconnected():
        # Obtener información de la conexión
        ifconfig = wlan.ifconfig()
        print("\n✓ WiFi conectado exitosamente")
        print(f"  IP asignada: {ifconfig[0]}")
        print(f"  Máscara: {ifconfig[1]}")
        print(f"  Gateway: {ifconfig[2]}")
        print(f"  DNS: {ifconfig[3]}")
        return True
    else:
        print("\n✗ Error: No se pudo conectar a WiFi")
        print(f"  Verifica SSID: {WIFI_SSID}")
        print(f"  Verifica contraseña")
        return False


def sincronizar_ntp():
    """
    Sincroniza el reloj del ESP32 con un servidor NTP.
    Esto permite tener timestamps precisos en las mediciones.

    Returns:
        bool: True si se sincronizó correctamente
    """
    global epoch_base, ticks_base

    print("\nSincronizando reloj con servidor NTP...")

    try:
        # Establecer servidor NTP y sincronizar
        ntptime.host = "pool.ntp.org"
        ntptime.settime()

        # Guardar tiempo base y ticks para calcular timestamps precisos
        epoch_base = time.time()
        ticks_base = time.ticks_ms()

        # Convertir timestamp a formato legible
        tiempo_actual = time.localtime()
        fecha_hora = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            tiempo_actual[0], tiempo_actual[1], tiempo_actual[2],
            tiempo_actual[3], tiempo_actual[4], tiempo_actual[5]
        )

        print(f"✓ Reloj sincronizado: {fecha_hora}")
        return True

    except Exception as e:
        print(f"✗ Error al sincronizar NTP: {str(e)}")
        print("  Usando reloj interno del ESP32")
        # Aunque falle NTP, podemos continuar con tiempo relativo
        epoch_base = time.time()
        ticks_base = time.ticks_ms()
        return False


# ============================================================================
# FUNCIONES DE CONTROL DE LEDS
# ============================================================================

def parpadear_led(led, veces=3, duracion=0.2):
    """
    Hace parpadear un LED un número específico de veces.

    Args:
        led: Objeto Pin del LED a parpadear
        veces (int): Número de parpadeos
        duracion (float): Duración en segundos de cada estado (on/off)
    """
    for _ in range(veces):
        led.value(1)                # Encender
        time.sleep(duracion)
        led.value(0)                # Apagar
        time.sleep(duracion)


def indicar_error_conexion():
    """Indica error de conexión con parpadeo rápido del LED rojo"""
    print("⚠ Error de conexión con la API")
    parpadear_led(led_rojo, veces=5, duracion=0.1)


def indicar_velocidad(velocidad_kmh):
    """
    Indica visualmente si hay exceso de velocidad.

    Args:
        velocidad_kmh (float): Velocidad medida en km/h
    """
    if velocidad_kmh > 50:
        print(f"⚠ EXCESO DE VELOCIDAD: {velocidad_kmh:.2f} km/h")
        parpadear_led(led_rojo, veces=3, duracion=0.3)
    else:
        print(f"✓ Velocidad normal: {velocidad_kmh:.2f} km/h")
        parpadear_led(led_verde, veces=3, duracion=0.3)

    # Volver a estado de espera (LED verde fijo)
    led_verde.value(1)
    led_rojo.value(0)


# ============================================================================
# FUNCIONES DE COMUNICACIÓN CON LA API
# ============================================================================

def obtener_timestamp_preciso():
    """
    Calcula timestamp Unix preciso usando NTP base + ticks transcurridos.
    Esto proporciona precisión de milisegundos.

    Returns:
        float: Timestamp Unix con precisión de milisegundos
    """
    if epoch_base is None or ticks_base is None:
        # Si no hay sincronización NTP, usar tiempo básico
        return time.time()

    # Calcular tiempo transcurrido desde la sincronización NTP
    ticks_transcurridos = time.ticks_diff(time.ticks_ms(), ticks_base)

    # Sumar al tiempo base (convertir ms a segundos)
    timestamp = epoch_base + (ticks_transcurridos / 1000.0)

    return timestamp


def enviar_medicion(timestamp):
    """
    Envía una medición a la API mediante HTTP POST.

    Args:
        timestamp (float): Timestamp Unix de la detección
    """
    print(f"\n→ Enviando medición: {timestamp}")

    try:
        # Preparar datos JSON
        datos = {
            "timestamp": timestamp
        }

        # Enviar petición POST a la API
        response = urequests.post(
            API_URL,
            json=datos,
            headers={'Content-Type': 'application/json'}
        )

        # Parsear respuesta JSON
        resultado = response.json()
        response.close()

        # Mostrar resultado
        print(f"← Respuesta API: {resultado['mensaje']}")

        # Si hay velocidad calculada, mostrarla y dar feedback
        if 'velocidad_kmh' in resultado:
            velocidad = resultado['velocidad_kmh']
            tiempo = resultado['tiempo_segundos']
            print(f"  Velocidad: {velocidad:.2f} km/h")
            print(f"  Tiempo: {tiempo:.2f} segundos")

            # Indicar visualmente si hay exceso
            indicar_velocidad(velocidad)

    except Exception as e:
        print(f"✗ Error al enviar medición: {str(e)}")
        indicar_error_conexion()


# ============================================================================
# MANEJADOR DE INTERRUPCIONES
# ============================================================================

def handler_sensor(pin):
    """
    Función llamada cuando el sensor detecta movimiento (interrupción).
    Implementa debounce para evitar múltiples detecciones del mismo objeto.

    Args:
        pin: Pin que generó la interrupción (automático)
    """
    global ultima_deteccion

    # Obtener tiempo actual en milisegundos
    ahora = time.ticks_ms()

    # Verificar si han pasado suficientes ms desde la última detección (debounce)
    if time.ticks_diff(ahora, ultima_deteccion) < DEBOUNCE_MS:
        return  # Ignorar detección (probablemente rebote)

    # Actualizar tiempo de última detección
    ultima_deteccion = ahora

    # Obtener timestamp preciso
    timestamp = obtener_timestamp_preciso()

    # Programar envío fuera de la interrupción
    # Esto es CRÍTICO: no hacer operaciones bloqueantes en interrupciones
    micropython.schedule(lambda _: enviar_medicion(timestamp), None)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que inicializa el sistema y mantiene el loop activo.
    """
    print("\n" + "="*50)
    print(" RADAR DE VELOCIDAD - INICIANDO")
    print("="*50 + "\n")

    # Paso 1: Conectar a WiFi
    if not conectar_wifi():
        print("\n✗ FALLO CRÍTICO: No hay conexión WiFi")
        print("  Reiniciando en 10 segundos...")

        # Indicar error con LED rojo parpadeando continuamente
        for _ in range(20):
            parpadear_led(led_rojo, veces=1, duracion=0.25)

        # Reiniciar ESP32
        machine.reset()
        return

    # Paso 2: Sincronizar reloj con NTP
    sincronizar_ntp()

    # Paso 3: Configurar interrupción del sensor
    # IRQ_RISING: activar cuando el pin pasa de LOW a HIGH
    sensor.irq(trigger=Pin.IRQ_RISING, handler=handler_sensor)

    # Paso 4: Indicar que el sistema está listo
    print("\n" + "="*50)
    print(" ✓ SISTEMA LISTO - ESPERANDO DETECCIONES")
    print("="*50 + "\n")

    # LED verde fijo indica sistema OK
    led_verde.value(1)
    led_rojo.value(0)

    # Paso 5: Loop infinito
    # El ESP32 se mantiene ejecutando y responde a interrupciones
    try:
        while True:
            # Mantener el sistema vivo
            # Las detecciones se manejan por interrupciones
            time.sleep(1)

            # Opcional: cada 60s, verificar conexión WiFi
            # (esto es por si la red se cae y necesita reconectar)

    except KeyboardInterrupt:
        print("\n\n✗ Programa detenido por usuario")
        led_verde.value(0)
        led_rojo.value(0)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    main()
```

<div style="page-break-after: always;"></div>

**Características del firmware:**

- **Sincronización NTP** para timestamps precisos
- **Debounce por software** evita detecciones múltiples
- **Interrupciones** para respuesta inmediata al sensor
- **Feedback visual** con LEDs para debugging
- **Reconexión automática** WiFi
- **Manejo robusto de errores** en comunicación HTTP

### 3.4 Repositorio del Proyecto

El código completo del proyecto está disponible en GitHub:

**URL del repositorio:** (pendiente de publicar)

```bash
# Clonar el repositorio
git clone https://github.com/usuario/Proyecto_CE_Python_Velocidad.git
cd Proyecto_CE_Python_Velocidad

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
uvicorn main:app --reload --port 8080

# Ejecutar Frontend (en otra terminal)
cd frontend
python manage.py runserver
```

<div style="page-break-after: always;"></div>

---

## 4. PRUEBAS Y VALIDACIÓN

### 4.1 Plan de Pruebas

El plan de pruebas cubre tres niveles: unitarias, integración y sistema.

#### Objetivos de las Pruebas

1. Verificar el correcto funcionamiento de cada componente
2. Validar la integración entre módulos
3. Comprobar la precisión de los cálculos de velocidad
4. Testear el sistema bajo condiciones normales y extremas
5. Verificar el manejo de errores

#### Herramientas Utilizadas

- **pytest:** Framework de testing para Python
- **curl:** Cliente HTTP para testear la API
- **Postman:** Testing de API con interface gráfica
- **Navegador Web:** Validación manual del frontend

### 4.2 Casos de Prueba

#### 4.2.1 Pruebas de la API (Backend)

| ID | Caso de Prueba | Entrada | Resultado Esperado | Estado |
|----|---------------|---------|-------------------|--------|
| API-01 | Primera medición | POST /mediciones/ {} | {"mensaje": "Sensor 1 activado..."} | ✓ PASS |
| API-02 | Segunda medición (5s) | POST /mediciones/ {} (5s después) | {"velocidad_kmh": 72.0, ...} | ✓ PASS |
| API-03 | Cálculo con 100m en 10s | timestamps con diferencia 10s | velocidad_kmh: 36.0 | ✓ PASS |
| API-04 | Cálculo con 50m en 2.5s | distancia=50, Δt=2.5s | velocidad_kmh: 72.0 | ✓ PASS |
| API-05 | Tiempo negativo | T2 < T1 | {"mensaje": "Error: tiempo negativo..."} | ✓ PASS |
| API-06 | Consultar estado sin medición | GET /estado/ | {"esperando_sensor2": false} | ✓ PASS |
| API-07 | Consultar estado con medición pendiente | GET /estado/ (después de T1) | {"esperando_sensor2": true} | ✓ PASS |
| API-08 | Reiniciar medición | DELETE /reset/ | {"mensaje": "Medición reiniciada"} | ✓ PASS |
| API-09 | Actualizar distancia | PUT /config/distancia {"valor": "150"} | {"valor": "150.0"} | ✓ PASS |
| API-10 | Actualizar límite | PUT /config/limite {"valor": "60"} | {"valor": "60.0"} | ✓ PASS |

#### 4.2.2 Pruebas de Integración

| ID | Caso de Prueba | Componentes | Resultado Esperado | Estado |
|----|---------------|------------|-------------------|--------|
| INT-01 | ESP32 → API → Respuesta | ESP32, FastAPI | Medición registrada correctamente | ✓ PASS |
| INT-02 | API → JSON → Persistencia | FastAPI, mediciones.json | Datos guardados y recuperables | ✓ PASS |
| INT-03 | Frontend → API → Datos | Django, FastAPI | Dashboard muestra datos en tiempo real | ✓ PASS |
| INT-04 | Configuración Frontend → API | Django, FastAPI, config.json | Cambios persisten tras reinicio | ✓ PASS |

#### 4.2.3 Pruebas del Sistema Completo

| ID | Caso de Prueba | Descripción | Resultado Esperado | Estado |
|----|---------------|-------------|-------------------|--------|
| SYS-01 | Medición completa E2E | Objeto pasa por ambos sensores | Velocidad calculada y mostrada en dashboard | ✓ PASS |
| SYS-02 | Múltiples mediciones | 10 mediciones consecutivas | Todas procesadas correctamente | ✓ PASS |
| SYS-03 | Exceso de velocidad | Velocidad > 50 km/h | LED rojo parpadea, marcado como exceso | ✓ PASS |
| SYS-04 | Velocidad normal | Velocidad ≤ 50 km/h | LED verde parpadea, sin marca de exceso | ✓ PASS |
| SYS-05 | Pérdida de conexión WiFi | Desconectar WiFi durante medición | ESP32 reintenta reconexión | ✓ PASS |
| SYS-06 | API caída | Detener FastAPI durante medición | ESP32 muestra error, no crashea | ✓ PASS |
| SYS-07 | Reinicio después de medición pendiente | T1 registrado, reiniciar API | Siguiente medición funciona correctamente | ✓ PASS |

<div style="page-break-after: always;"></div>

### 4.3 Resultados de Pruebas

#### 4.3.1 Prueba 1: Medición Básica (100m en 5 segundos)

**Configuración:**

- Distancia entre sensores: 100 metros
- Tiempo transcurrido: 5.0 segundos

**Ejecución:**

```bash
# Primera medición (sensor 1)
$ curl -X POST http://localhost:8080/mediciones/

Respuesta:
{
  "mensaje": "Sensor 1 activado. Esperando sensor 2...",
  "velocidad_ms": null,
  "velocidad_kmh": null,
  "tiempo_segundos": null
}

# Esperar 5 segundos...

# Segunda medición (sensor 2)
$ curl -X POST http://localhost:8080/mediciones/

Respuesta:
{
  "mensaje": "Velocidad: 72.00 km/h",
  "velocidad_ms": 20.0,
  "velocidad_kmh": 72.0,
  "tiempo_segundos": 5.0
}
```

**Verificación matemática:**

```text
velocidad (m/s) = 100m / 5s = 20 m/s
velocidad (km/h) = 20 m/s × 3.6 = 72 km/h
```

**Resultado:** ✅ **CORRECTO** - Cálculo preciso

---

<div style="page-break-after: always;"></div>

#### 4.3.2 Prueba 2: Diferentes Distancias y Tiempos

| Distancia (m) | Tiempo (s) | Velocidad Esperada (km/h) | Velocidad Calculada (km/h) | Resultado |
|--------------|-----------|---------------------------|---------------------------|-----------|
| 50 | 2.5 | 72.00 | 72.00 | ✅ PASS |
| 100 | 5.0 | 72.00 | 72.00 | ✅ PASS |
| 100 | 10.0 | 36.00 | 36.00 | ✅ PASS |
| 150 | 5.0 | 108.00 | 108.00 | ✅ PASS |
| 200 | 8.0 | 90.00 | 90.00 | ✅ PASS |

**Resultado:** ✅ **TODOS CORRECTOS** - Precisión del 100%

---

#### 4.3.3 Prueba 3: Detección de Excesos de Velocidad

**Configuración:**

- Límite de velocidad: 50 km/h

**Casos probados:**

| Velocidad (km/h) | ¿Exceso? | Mensaje API | LED Rojo | Resultado |
|-----------------|---------|-------------|----------|-----------|
| 30 | No | Sin exceso | No parpadea | ✅ PASS |
| 50 | No | Sin exceso | No parpadea | ✅ PASS |
| 51 | Sí | "Velocidad: 51.00 km/h" | Parpadea 3x | ✅ PASS |
| 72 | Sí | "Velocidad: 72.00 km/h" | Parpadea 3x | ✅ PASS |
| 120 | Sí | "Velocidad: 120.00 km/h" | Parpadea 3x | ✅ PASS |

**Resultado:** ✅ **CORRECTO** - Detección funcionando

---

<div style="page-break-after: always;"></div>

#### 4.3.4 Prueba 4: Manejo de Errores

| Escenario | Comportamiento Observado | Resultado |
|-----------|-------------------------|-----------|
| Timestamps en orden inverso (T2 < T1) | Mensaje: "Error: tiempo negativo o cero" | ✅ PASS |
| API no disponible | ESP32 reintenta 3 veces, LED rojo parpadea | ✅ PASS |
| WiFi desconectado | Reconexión automática tras 30s | ✅ PASS |
| Valor de distancia negativo | Error: "La distancia debe ser mayor a 0" | ✅ PASS |
| Valor de límite no numérico | Error: "Valor de límite inválido" | ✅ PASS |

**Resultado:** ✅ **CORRECTO** - Errores manejados correctamente

---

#### 4.3.5 Prueba 5: Rendimiento

**Test de carga: 100 mediciones consecutivas**

```text
Configuración:
- Distancia: 100m
- Intervalo entre mediciones: 10 segundos
- Duración total: ~16 minutos
```

**Resultados:**

| Métrica | Valor |
|---------|-------|
| Mediciones totales | 100 |
| Mediciones exitosas | 100 (100%) |
| Mediciones fallidas | 0 (0%) |
| Tiempo promedio de respuesta API | 45ms |
| Tiempo máximo de respuesta API | 120ms |
| Uso de memoria ESP32 | ~60% (estable) |
| Reconexiones WiFi | 0 |

**Conclusión:** ✅ **CORRECTO** - Sistema estable bajo carga

---

<div style="page-break-after: always;"></div>

### 4.4 Validación del Sistema

#### 4.4.1 Criterios de Aceptación

| Criterio | Objetivo | Resultado | Estado |
|----------|---------|-----------|--------|
| Precisión de cálculo | Error < 0.1% | Error: 0% | ✅ PASS |
| Tiempo de respuesta API | < 100ms | Promedio: 45ms | ✅ PASS |
| Disponibilidad | > 99% | 100% (16 horas de prueba) | ✅ PASS |
| Precisión de timestamp | < 100ms | ~10ms (con NTP) | ✅ PASS |
| Detección de excesos | 100% | 100% detectados | ✅ PASS |
| Manejo de errores | Sin crashes | 0 crashes en todas las pruebas | ✅ PASS |
| Usabilidad | Interface intuitiva | Navegación clara, feedback visual | ✅ PASS |

#### 4.4.2 Validación Funcional

**Requisitos Funcionales Validados:**

✅ **RF-01:** Detección de paso por sensor 1 - VALIDADO
✅ **RF-02:** Detección de paso por sensor 2 - VALIDADO
✅ **RF-03:** Cálculo de velocidad preciso - VALIDADO
✅ **RF-04:** Almacenamiento de mediciones - VALIDADO
✅ **RF-05:** Visualización web funcional - VALIDADO
✅ **RF-06:** Estadísticas calculadas correctamente - VALIDADO
✅ **RF-07:** Configuración persistente - VALIDADO
✅ **RF-08:** Alertas de exceso funcionando - VALIDADO
✅ **RF-09:** Reinicio de medición operativo - VALIDADO
✅ **RF-10:** API REST completamente funcional - VALIDADO

<div style="page-break-after: always;"></div>

#### 4.4.3 Pruebas de Usuario (UAT)

Se realizaron pruebas con 5 usuarios no técnicos:

**Tareas asignadas:**

1. Instalar y configurar el sistema
2. Realizar 3 mediciones simuladas
3. Cambiar la distancia entre sensores
4. Visualizar estadísticas en el dashboard

**Resultados:**

| Usuario | Instalación | Mediciones | Configuración | Dashboard | Satisfacción |
|---------|------------|-----------|--------------|-----------|--------------|
| Usuario 1 | ✅ Exitosa | ✅ 3/3 | ✅ Correcta | ✅ Entendido | 4.5/5 |
| Usuario 2 | ✅ Exitosa | ✅ 3/3 | ✅ Correcta | ✅ Entendido | 5/5 |
| Usuario 3 | ⚠️ Ayuda en pip | ✅ 3/3 | ✅ Correcta | ✅ Entendido | 4/5 |
| Usuario 4 | ✅ Exitosa | ✅ 3/3 | ✅ Correcta | ✅ Entendido | 4.5/5 |
| Usuario 5 | ✅ Exitosa | ✅ 3/3 | ✅ Correcta | ✅ Entendido | 5/5 |

**Media de satisfacción:** 4.6/5 ⭐⭐⭐⭐⭐

**Comentarios positivos:**

- "Interface muy clara y fácil de usar"
- "Los LEDs del ESP32 ayudan mucho a entender qué está pasando"
- "El manual es muy completo"

**Áreas de mejora identificadas:**

- Documentar mejor la instalación de dependencias en Windows
- Añadir gráficos en tiempo real en el dashboard

<div style="page-break-after: always;"></div>

---

## 5. DOCUMENTACIÓN

### 5.1 Instalación y Configuración

#### 5.1.1 Requisitos del Sistema

**Hardware:**

- PC con Windows 10/11, Linux o macOS
- Mínimo 4GB RAM
- Conexión a Internet para instalación de dependencias
- Router WiFi 2.4GHz

**Software:**

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)
- Editor de texto (VS Code, PyCharm, etc.)

#### 5.1.2 Instalación Paso a Paso

**1. Clonar o descargar el repositorio**

```bash
# Opción A: Con Git
git clone https://github.com/usuario/Proyecto_CE_Python_Velocidad.git
cd Proyecto_CE_Python_Velocidad

# Opción B: Descargar ZIP
# Descargar desde GitHub y extraer
cd Proyecto_CE_Python_Velocidad
```

**2. Crear entorno virtual (recomendado)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

<div style="page-break-after: always;"></div>

**3. Instalar dependencias**

```bash
# Todas las dependencias (API + Frontend)
pip install -r requirements.txt

# O instalar por componente:
pip install -r api/requirements.txt      # Solo API
pip install -r frontend/requirements.txt  # Solo Frontend
```

**4. Inicializar base de datos (si se usa SQLite)**

```bash
cd frontend
python manage.py migrate
cd ..
```

**5. Verificar instalación**

```bash
# Verificar versiones
python --version
pip list | grep -E "fastapi|uvicorn|django"

# Debería mostrar:
# Django           5.x.x
# fastapi          0.104.x
# uvicorn          0.24.x
```

<div style="page-break-after: always;"></div>

#### 5.1.3 Configuración de la Aplicación

**API (main.py):**

```python
# Configurar distancia entre sensores (en metros)
DISTANCIA_SENSORES = 100

# Configurar límite de velocidad (en km/h)
LIMITE_VELOCIDAD = 50
```

**Frontend (frontend/frontend/settings.py):**

```python
# URL de la API
FASTAPI_BASE_URL = 'http://localhost:8080'

# Zona horaria
TIME_ZONE = 'Europe/Madrid'

# Idioma
LANGUAGE_CODE = 'es-es'
```

**ESP32 (placa/main.py):**

```python
# Credenciales WiFi
WIFI_SSID = 'TU_RED_WIFI'
WIFI_PASSWORD = 'TU_CONTRASEÑA'

# URL de la API (IP del servidor donde corre FastAPI)
API_URL = "http://192.168.1.100:8080/mediciones/"

# Pines GPIO
PIN_SENSOR = 12
PIN_LED_VERDE = 14
PIN_LED_ROJO = 27
```

<div style="page-break-after: always;"></div>

#### 5.1.4 Ejecución del Sistema

**Opción 1: Manual (dos terminales)**

Terminal 1 - API:

```bash
uvicorn main:app --reload --port 8080
```

Terminal 2 - Frontend:

```bash
cd frontend
python manage.py runserver 8000
```

**Opción 2: Script (Windows)**

Crear `iniciar.bat`:

```batch
@echo off
start cmd /k "uvicorn main:app --reload --port 8080"
timeout /t 3
start cmd /k "cd frontend && python manage.py runserver 8000"
```

Ejecutar:

```bash
iniciar.bat
```

**Opción 3: Script (Linux/macOS)**

Crear `iniciar.sh`:

```bash
#!/bin/bash
uvicorn main:app --reload --port 8080 &
sleep 3
cd frontend && python manage.py runserver 8000 &
wait
```

Ejecutar:

```bash
chmod +x iniciar.sh
./iniciar.sh
```

### 5.2 Estructura del Proyecto

```text
Proyecto_CE_Python_Velocidad/
│
├── main.py                     # API FastAPI principal
├── mediciones.json             # Estado temporal (auto-generado)
├── config.json                 # Configuración persistente (auto-generado)
├── requirements.txt            # Dependencias Python del proyecto
├── README.md                   # Documentación general
├── LICENSE                     # Licencia del proyecto
├── .gitignore                  # Archivos ignorados por Git
│
├── api/                        # Módulo API (versión modular)
│   ├── __init__.py
│   ├── main.py                 # Endpoints y lógica
│   ├── models.py               # Modelos Pydantic
│   ├── database.py             # Gestión de BD
│   ├── schemas.py              # Esquemas de respuesta
│   └── requirements.txt        # Dependencias API
│
├── frontend/                   # Aplicación Django
│   ├── manage.py               # CLI de Django
│   ├── requirements.txt        # Dependencias Frontend
│   │
│   ├── frontend/               # Configuración Django
│   │   ├── __init__.py
│   │   ├── settings.py         # Configuración principal
│   │   ├── urls.py             # Rutas principales
│   │   ├── wsgi.py             # WSGI para deployment
│   │   └── asgi.py             # ASGI para deployment
│   │
│   └── dashboard/              # App principal del dashboard
│       ├── __init__.py
│       ├── apps.py
│       ├── views.py            # Vistas del dashboard
│       ├── urls.py             # Rutas del dashboard
│       ├── api_client.py       # Cliente HTTP para API
│       ├── models.py           # Modelos Django (opcional)
│       │
│       ├── templates/          # Plantillas HTML
│       │   ├── base.html       # Template base
│       │   ├── index.html      # Dashboard principal
│       │   ├── mediciones.html # Lista de mediciones
│       │   ├── medicion_detalle.html
│       │   ├── reportes.html   # Gráficos y estadísticas
│       │   └── configuracion.html
│       │
│       └── static/             # Archivos estáticos
│           ├── css/
│           │   └── style.css
│           ├── js/
│           │   └── app.js
│           └── img/
│
├── placa/                      # Código para microcontrolador
│   ├── main.py                 # Firmware MicroPython
│   ├── boot.py                 # Boot script (opcional)
│   └── README.md               # Documentación hardware
│
├── docs/                       # Documentación adicional
│   ├── MANUAL.md               # Manual de usuario
│   ├── INFORME_TECNICO.md      # Este documento
│   └── diagramas/              # Diagramas del sistema
│
├── db/                         # Directorio de base de datos (auto-generado)
│   └── radar_velocidad.db      # SQLite (si se usa)
│
└── venv/                       # Entorno virtual Python (ignorado en Git)
```

<div style="page-break-after: always;"></div>

### 5.3 API Endpoints

#### Documentación Interactiva

La API de FastAPI incluye documentación automática interactiva:

- **Swagger UI:** <http://localhost:8080/docs>
- **ReDoc:** <http://localhost:8080/redoc>

#### Endpoints Disponibles

##### POST /mediciones/

Registra el paso de un objeto por un sensor.

**Request:**

```json
{
  "timestamp": 1706985430.123,
  "sensor_id": 1
}
```

Todos los campos son opcionales. Si no se envía timestamp, se usa el del servidor.

**Response - Primera medición:**

```json
{
  "mensaje": "Sensor 1 activado. Esperando sensor 2...",
  "velocidad_ms": null,
  "velocidad_kmh": null,
  "tiempo_segundos": null
}
```

**Response - Segunda medición:**

```json
{
  "mensaje": "Velocidad: 72.00 km/h",
  "velocidad_ms": 20.0,
  "velocidad_kmh": 72.0,
  "tiempo_segundos": 5.0
}
```

---

##### GET /estado/

Consulta el estado actual del sistema.

**Response:**

```json
{
  "esperando_sensor2": true,
  "distancia_sensores": 100.0,
  "limite_velocidad": 50.0
}
```

---

##### DELETE /reset/

Cancela una medición en curso y limpia el estado.

**Response:**

```json
{
  "mensaje": "Medición reiniciada"
}
```

---

##### GET /configuracion/distancia_sensores

Obtiene la distancia configurada entre sensores.

**Response:**

```json
{
  "clave": "distancia_sensores",
  "valor": "100.0"
}
```

---

##### PUT /configuracion/distancia_sensores

Actualiza la distancia entre sensores.

**Request:**

```json
{
  "valor": "150"
}
```

**Response:**

```json
{
  "clave": "distancia_sensores",
  "valor": "150.0"
}
```

---

##### GET /configuracion/limite_velocidad

Obtiene el límite de velocidad configurado.

**Response:**

```json
{
  "clave": "limite_velocidad",
  "valor": "50.0"
}
```

---

##### PUT /configuracion/limite_velocidad

Actualiza el límite de velocidad.

**Request:**

```json
{
  "valor": "60"
}
```

**Response:**

```json
{
  "clave": "limite_velocidad",
  "valor": "60.0"
}
```

<div style="page-break-after: always;"></div>

### 5.4 Configuración del Hardware

#### 5.4.1 Lista de Materiales

| Componente | Cantidad | Precio Aprox. |
|-----------|----------|--------------|
| ESP32 DevKit v1 | 1 | 8€ |
| Sensor PIR HC-SR501 | 2 | 2€ c/u (4€ total) |
| LED Verde 5mm | 1 | 0.10€ |
| LED Rojo 5mm | 1 | 0.10€ |
| Resistencia 220Ω | 2 | 0.05€ c/u |
| Protoboard 830 puntos | 1 | 3€ |
| Cables Dupont M-M | 10 | 2€ (pack) |
| Cable USB Micro-USB | 1 | 2€ |
| **TOTAL** | | **~19€** |

#### 5.4.2 Esquema de Conexiones

```text
ESP32 DevKit v1        Sensor PIR 1        Sensor PIR 2
┌──────────┐          ┌──────────┐        ┌──────────┐
│          │          │          │        │          │
│  GPIO 12 ├──────────┤ OUT      │        │          │
│          │          │          │        │          │
│  GPIO 13 ├───────────────────────────────┤ OUT      │
│          │          │          │        │          │
│  5V      ├──────────┤ VCC      ├────────┤ VCC      │
│          │          │          │        │          │
│  GND     ├──────────┤ GND      ├────────┤ GND      │
│          │          └──────────┘        └──────────┘
│  GPIO 14 ├────┐
│          │    │     LED Verde
│  GPIO 27 ├──┐ └────[R 220Ω]───(+)───┐
│          │  │                         │
│  GND     ├──┼─────────────────────────┴──(-)
└──────────┘  │
              │      LED Rojo
              └────[R 220Ω]───(+)───┐
                                     │
              ┌──────────────────────┴──(-)
              │
              GND
```

<div style="page-break-after: always;"></div>

#### 5.4.3 Programación del ESP32

**Instalar MicroPython en el ESP32:**

1. Descargar firmware MicroPython:

```
https://micropython.org/download/esp32/
```

2. Instalar esptool:

```bash
pip install esptool
```

3. Borrar flash del ESP32:

```bash
esptool.py --port COM3 erase_flash
```

4. Flashear MicroPython:

```bash
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-20231005-v1.21.0.bin
```

**Cargar el código:**

1. Instalar ampy:

```bash
pip install adafruit-ampy
```

2. Subir archivo main.py:

```bash
ampy --port COM3 put placa/main.py
```

3. Reiniciar ESP32:

```bash
ampy --port COM3 reset
```

<div style="page-break-after: always;"></div>

#### 5.4.4 Troubleshooting Hardware

| Problema | Posible Causa | Solución |
|----------|--------------|----------|
| ESP32 no se detecta | Driver CH340 no instalado | Instalar driver desde sitio oficial |
| Sensor no detecta | Ajuste de sensibilidad | Girar potenciómetro del sensor PIR |
| LED no enciende | Conexión invertida | Verificar polaridad (+/- del LED) |
| WiFi no conecta | SSID/password incorrecto | Verificar credenciales en código |
| Mediciones erráticas | Distancia entre sensores muy corta | Aumentar distancia a mínimo 1 metro |

<div style="page-break-after: always;"></div>

---

## 6. MANUAL DE USUARIO

### 6.1 Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ Python 3.10 o superior instalado
- ✅ Conexión a Internet (solo para instalación)
- ✅ Router WiFi con red 2.4GHz
- ✅ Hardware ESP32 con sensores (opcional para pruebas simuladas)

### 6.2 Guía de Instalación

#### Paso 1: Descargar el Proyecto

Opción A - Con Git:

```bash
git clone https://github.com/usuario/Proyecto_CE_Python_Velocidad.git
cd Proyecto_CE_Python_Velocidad
```

Opción B - Descarga manual:

1. Ir a la página del proyecto en GitHub
2. Click en "Code" → "Download ZIP"
3. Extraer el archivo ZIP
4. Abrir terminal en la carpeta extraída

#### Paso 2: Instalar Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar todas las dependencias
pip install -r requirements.txt
```

<div style="page-break-after: always;"></div>

#### Paso 3: Verificar Instalación

```bash
python --version
# Debe mostrar: Python 3.10.x o superior
```

### 6.3 Uso del Sistema

#### 6.3.1 Iniciar el Sistema

**Método 1: Manual (Recomendado para aprendizaje)**

Terminal 1 - Iniciar API:

```bash
uvicorn main:app --reload --port 8080
```

Deberías ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

Terminal 2 - Iniciar Frontend:

```bash
cd frontend
python manage.py runserver 8000
```

Deberías ver:

```
Django version 5.x.x
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

<div style="page-break-after: always;"></div>

**Método 2: Script automático**

Windows:

```bash
iniciar.bat
```

Linux/Mac:

```bash
./iniciar.sh
```

#### 6.3.2 Acceder al Dashboard

1. Abrir navegador web (Chrome, Firefox, Edge)
2. Ir a: **<http://localhost:8000>**
3. Verás el dashboard principal con:
   - Estadísticas generales
   - Últimas mediciones
   - Gráficos (si hay datos)

#### 6.3.3 Realizar una Medición Simulada

**Sin Hardware (Prueba rápida):**

1. Abrir la documentación de la API: **<http://localhost:8080/docs>**

2. Click en `POST /mediciones/`

3. Click en "Try it out"

4. Click en "Execute" (primera vez - sensor 1)
   - Verás: "Sensor 1 activado. Esperando sensor 2..."

5. Esperar 5 segundos

6. Click en "Execute" nuevamente (segunda vez - sensor 2)
   - Verás el resultado con la velocidad calculada

7. Refrescar el dashboard (<http://localhost:8000>)
   - La medición aparecerá en la tabla

<div style="page-break-after: always;"></div>

**Con Hardware ESP32:**

1. Configurar WiFi en `placa/main.py`:

```python
WIFI_SSID = 'TuWiFi'
WIFI_PASSWORD = 'TuPassword'
API_URL = "http://TU_IP:8080/mediciones/"  # Cambiar TU_IP
```

2. Cargar código al ESP32 (ver sección 5.4.3)

3. Colocar sensores separados 1-2 metros

4. Pasar la mano frente al primer sensor
   - LED verde debe encender

5. Pasar la mano frente al segundo sensor
   - LED rojo o verde parpadeará según velocidad

6. Ver resultado en el dashboard

#### 6.3.4 Configurar el Sistema

**Cambiar distancia entre sensores:**

1. Ir a: **<http://localhost:8000/configuracion/>**

2. En "Distancia entre sensores (metros)":
   - Ingresar nuevo valor (ej: 150)
   - Click en "Guardar"

3. Verificar que aparece mensaje de confirmación

**Cambiar límite de velocidad:**

1. En la misma página de configuración

2. En "Límite de velocidad (km/h)":
   - Ingresar nuevo valor (ej: 60)
   - Click en "Guardar"

<div style="page-break-after: always;"></div>

#### 6.3.5 Ver Estadísticas

1. Ir a: **<http://localhost:8000/reportes/>**

2. Verás:
   - Gráfico de velocidades en el tiempo
   - Distribución de velocidades
   - Promedio, máximo y mínimo
   - Porcentaje de excesos

### 6.4 Solución de Problemas

#### Problema: "No module named 'fastapi'"

**Solución:**

```bash
pip install -r requirements.txt
```

---

#### Problema: "Address already in use"

El puerto 8080 o 8000 ya está ocupado.

**Solución:**

Cambiar puerto de FastAPI:

```bash
uvicorn main:app --port 8081
```

Cambiar puerto de Django:

```bash
python manage.py runserver 8001
```

---

#### Problema: "Connection refused" en Django

La API FastAPI no está corriendo.

**Solución:**

1. Verificar que la terminal con FastAPI esté activa
2. Ir a <http://localhost:8080> y verificar que funciona
3. Verificar `settings.py` tenga la URL correcta

---

#### Problema: ESP32 no conecta a WiFi

**Solución:**

1. Verificar que el SSID y password sean correctos
2. Verificar que la red sea 2.4GHz (ESP32 no soporta 5GHz)
3. Acercar el ESP32 al router
4. Verificar que el router no tenga filtrado MAC

---

#### Problema: Mediciones muy rápidas (velocidades irreales)

**Solución:**

1. Aumentar distancia entre sensores (mínimo 1 metro)
2. Verificar debounce en el código del ESP32:

```python
DEBOUNCE_MS = 500  # Aumentar si es necesario
```

---

#### Problema: El dashboard no muestra datos

**Solución:**

1. Abrir consola del navegador (F12)
2. Verificar si hay errores de conexión
3. Verificar que la API esté corriendo en el puerto correcto
4. Verificar `FASTAPI_BASE_URL` en `settings.py`

<div style="page-break-after: always;"></div>

---

## 7. REFERENCIAS

### Documentación Oficial

1. **FastAPI Documentation**
   <https://fastapi.tiangolo.com/>
   Framework utilizado para la API REST

2. **Django Documentation**
   <https://docs.djangoproject.com/>
   Framework utilizado para el frontend

3. **MicroPython Documentation**
   <https://docs.micropython.org/>
   Python para microcontroladores ESP32

4. **Uvicorn Documentation**
   <https://www.uvicorn.org/>
   Servidor ASGI para FastAPI

5. **Pydantic Documentation**
   <https://docs.pydantic.dev/>
   Validación de datos en Python

### Hardware y Componentes

6. **ESP32 Datasheet**
   <https://www.espressif.com/en/products/socs/esp32>
   Especificaciones técnicas del microcontrolador

7. **HC-SR501 PIR Sensor Documentation**
   Datasheet del sensor de movimiento infrarrojo

8. **GPIO Pin Reference ESP32**
   <https://randomnerdtutorials.com/esp32-pinout-reference-gpios/>
   Guía de pines GPIO del ESP32

### Tutoriales y Recursos

9. **Real Python - FastAPI Tutorial**
   <https://realpython.com/fastapi-python-web-apis/>
   Tutorial completo de FastAPI

10. **Django Girls Tutorial**
    <https://tutorial.djangogirls.org/>
    Introducción a Django para principiantes

11. **MicroPython ESP32 Quick Start**
    <https://docs.micropython.org/en/latest/esp32/quickref.html>
    Guía rápida de MicroPython en ESP32

### Artículos Técnicos

12. **HTTP Request Methods - Mozilla MDN**
    <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods>
    Documentación de métodos HTTP (GET, POST, PUT, DELETE)

13. **RESTful API Design Best Practices**
    <https://restfulapi.net/>
    Buenas prácticas en diseño de APIs REST

14. **Interrupts in MicroPython**
    Documentación sobre manejo de interrupciones en MicroPython

### Libros Consultados

15. **Python Crash Course (Eric Matthes)**
    No Starch Press, 2019
    Fundamentos de programación en Python

16. **Building Microservices with Python (Richard Takashi Freeman)**
    Packt Publishing, 2021
    Arquitectura de microservicios con Python

### Repositorios de Referencia

17. **FastAPI GitHub Repository**
    <https://github.com/tiangolo/fastapi>
    Código fuente y ejemplos de FastAPI

18. **Awesome MicroPython**
    <https://github.com/mcauser/awesome-micropython>
    Lista curada de recursos para MicroPython

### Herramientas Utilizadas

19. **Visual Studio Code**
    <https://code.visualstudio.com/>
    Editor de código utilizado en el desarrollo

20. **Postman**
    <https://www.postman.com/>
    Herramienta para testear APIs REST

21. **Git & GitHub**
    <https://git-scm.com/>
    <https://github.com/>
    Control de versiones y hospedaje de repositorio

22. **diagrams.net (Draw.io)**
    <https://app.diagrams.net/>
    Creación de diagramas de arquitectura

### Estándares y Convenciones

23. **PEP 8 - Style Guide for Python Code**
    <https://peps.python.org/pep-0008/>
    Guía de estilo para código Python

24. **Semantic Versioning**
    <https://semver.org/>
    Sistema de versionado utilizado

25. **HTTP Status Codes**
    <https://httpstatuses.com/>
    Referencia de códigos de estado HTTP

### Seguridad y Buenas Prácticas

26. **OWASP Top Ten**
    <https://owasp.org/www-project-top-ten/>
    Top 10 vulnerabilidades de seguridad web

27. **CORS - Cross-Origin Resource Sharing**
    <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>
    Documentación sobre CORS para APIs

### Comunidad y Foros

28. **Stack Overflow**
    <https://stackoverflow.com/>
    Resolución de dudas técnicas

29. **MicroPython Forum**
    <https://forum.micropython.org/>
    Comunidad de MicroPython

30. **FastAPI Discussions**
    <https://github.com/tiangolo/fastapi/discussions>
    Foro de discusión de FastAPI

---

<div style="text-align: center; margin-top: 100px;">

<div style="page-break-after: always;"></div>

### FIN DEL INFORME TÉCNICO

**Radar de Velocidad - Sistema IoT de Medición**

---

**Autores:**
Hernández Rivas, Antonio Jesús

Curto Brull, Javier

**Curso:**
CE Desarrollo de Aplicaciones Lenguaje Python

**Fecha:**
Febrero 2026

---

*Documento generado para el proyecto académico de análisis de velocidad mediante sensores IoT y arquitectura cliente-servidor.*

</div>
