# Radar de Velocidad

Sistema para medir velocidad de objetos usando dos sensores con ESP32/ESP8266.

## Arquitectura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   ESP32     │      │   FastAPI   │      │   Django    │
│   Sensores  │─────▶│   API       │◀─────│   Frontend  │
│   :placa/   │ HTTP │   :8080     │ HTTP │   :8000     │
└─────────────┘      └─────────────┘      └─────────────┘
```

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Activar entorno (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar en local

### Opción 1: Dos terminales (recomendado para desarrollo)

**Terminal 1 - API FastAPI:**
```bash
uvicorn main:app --reload --port 8080
```

**Terminal 2 - Frontend Django:**
```bash
cd frontend
python manage.py runserver 8000
```

### Opción 2: Script único (Windows PowerShell)

```powershell
# Crear archivo run.ps1
Start-Process powershell -ArgumentList "-Command", "uvicorn main:app --reload --port 8080"
Start-Process powershell -ArgumentList "-Command", "cd frontend; python manage.py runserver 8000"
```

### Opción 3: Script único (Linux/Mac)

```bash
# Crear archivo run.sh
#!/bin/bash
uvicorn main:app --reload --port 8080 &
cd frontend && python manage.py runserver 8000 &
wait
```

## URLs locales

| Servicio | URL |
|----------|-----|
| **Frontend** | http://localhost:8000 |
| **API** | http://localhost:8080 |
| **API Docs** | http://localhost:8080/docs |

## Endpoints

### POST `/mediciones/` o `/`

Registra el paso por un sensor.

**Request (opcional):**
```json
{
  "timestamp": 1706985432.123,
  "sensor_id": 1
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `timestamp` | float | Unix timestamp desde la placa (opcional, si no se envía usa el del servidor) |
| `sensor_id` | int | Identificador del sensor (opcional) |

**Response - Primer sensor:**
```json
{
  "mensaje": "Sensor 1 activado. Esperando sensor 2..."
}
```

**Response - Segundo sensor:**
```json
{
  "mensaje": "Velocidad: 72.00 km/h",
  "velocidad_ms": 20.0,
  "velocidad_kmh": 72.0,
  "tiempo_segundos": 5.0
}
```

---

### GET `/estado/`

Consulta el estado actual del sistema.

**Response:**
```json
{
  "esperando_sensor2": true,
  "distancia_sensores": 100
}
```

---

### DELETE `/reset/`

Reinicia la medición pendiente.

**Response:**
```json
{
  "mensaje": "Medición reiniciada"
}
```

## Configuración

En `main.py`:

```python
DISTANCIA_SENSORES = 100  # metros entre sensores
```

## Cálculo de velocidad

```
velocidad (m/s) = distancia / tiempo
velocidad (km/h) = velocidad (m/s) × 3.6
```

## Flujo de medición

```
┌─────────────────────────────────────────────────────────────┐
│                      SENSOR 1                                │
│  POST /mediciones/ {"timestamp": 1706985430.000}            │
│  Response: {"mensaje": "Sensor 1 activado..."}              │
└─────────────────────────────────────────────────────────────┘
                            │
                            │  (objeto en movimiento)
                            │  5 segundos
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      SENSOR 2                                │
│  POST /mediciones/ {"timestamp": 1706985435.000}            │
│  Response: {                                                 │
│    "mensaje": "Velocidad: 72.00 km/h",                      │
│    "velocidad_ms": 20.0,                                    │
│    "velocidad_kmh": 72.0,                                   │
│    "tiempo_segundos": 5.0                                   │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

## Pruebas con cURL

```bash
# Simular sensor 1
curl -X POST http://localhost:8080/mediciones/

# Esperar unos segundos...

# Simular sensor 2
curl -X POST http://localhost:8080/mediciones/

# Ver estado
curl http://localhost:8080/estado/

# Reiniciar medición
curl -X DELETE http://localhost:8080/reset/
```

## Pruebas con timestamp manual

```bash
# Sensor 1 con timestamp específico
curl -X POST http://localhost:8080/mediciones/ \
  -H "Content-Type: application/json" \
  -d '{"timestamp": 1706985430.000}'

# Sensor 2 (5 segundos después = 72 km/h con 100m)
curl -X POST http://localhost:8080/mediciones/ \
  -H "Content-Type: application/json" \
  -d '{"timestamp": 1706985435.000}'
```

## Estructura de archivos

```
├── main.py                  # API FastAPI
├── mediciones.json          # Estado temporal (auto-generado)
├── frontend/                # Frontend Django
│   ├── manage.py
│   ├── frontend/            # Configuración Django
│   │   └── settings.py
│   └── dashboard/           # App principal
│       ├── views.py
│       ├── api_client.py    # Cliente para la API
│       └── templates/
├── placa/                   # Código para microcontrolador
│   ├── main.py              # MicroPython para ESP32
│   └── README.md            # Documentación de la placa
└── README.md                # Este archivo
```

## Componentes

| Componente | Tecnología | Puerto | Descripción |
|------------|------------|--------|-------------|
| API | FastAPI | 8080 | Backend REST |
| Frontend | Django | 8000 | Dashboard web |
| Placa | MicroPython | - | ESP32 con sensores |

## Integración con hardware

Ver [placa/README.md](placa/README.md) para configurar el ESP32/ESP8266 con sensores.

## Configurar DBeaver para PostgreSQL

Para conectarte a la base de datos PostgreSQL (local o en Render):

### 1. Nueva conexión

- Abre DBeaver
- Clic en **New Database Connection** (icono de enchufe) o `Ctrl+Shift+N`
- Selecciona **PostgreSQL** → **Next**

### 2. Configurar conexión

| Campo | Valor (ejemplo Render) |
|-------|------------------------|
| **Host** | `dpg-xxx.frankfurt-postgres.render.com` |
| **Port** | `5432` |
| **Database** | `radar_velocidad_db` |
| **Username** | `radar_velocidad_db_user` |
| **Password** | `(tu password)` |

Para **local con Docker**:

| Campo | Valor |
|-------|-------|
| **Host** | `localhost` |
| **Port** | `5432` |
| **Database** | `radar_velocidad` |
| **Username** | `radar` |
| **Password** | `radar123` |

### 3. Configurar SSL (solo para Render)

- Ve a la pestaña **SSL**
- Marca **Use SSL**
- En **SSL mode** selecciona: `require`

### 4. Probar conexión

- Clic en **Test Connection**
- Si pide descargar drivers, acepta
- Debe mostrar "Connected"
- Clic en **Finish**

### 5. Consultas útiles

```sql
-- Ver todas las mediciones
SELECT * FROM mediciones ORDER BY timestamp DESC;

-- Ver configuración
SELECT * FROM configuracion;

-- Mediciones con exceso de velocidad
SELECT * FROM mediciones WHERE velocidad_kmh > 50;

-- Estadísticas
SELECT
    COUNT(*) as total,
    AVG(velocidad_kmh) as promedio,
    MAX(velocidad_kmh) as maxima,
    MIN(velocidad_kmh) as minima
FROM mediciones
WHERE medicion_completa = true;
```
