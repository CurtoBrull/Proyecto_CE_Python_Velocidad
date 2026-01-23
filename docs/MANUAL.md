# Radar de Velocidad - Manual de Usuario

Sistema de medicion de velocidad utilizando Arduino con sensores de movimiento, API FastAPI y frontend Django.

## Indice

1. [Descripcion General](#descripcion-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Requisitos Previos](#requisitos-previos)
4. [Instalacion](#instalacion)
5. [Configuracion](#configuracion)
6. [Arranque del Sistema](#arranque-del-sistema)
7. [Uso de la Aplicacion](#uso-de-la-aplicacion)
8. [API Endpoints](#api-endpoints)
9. [Solucion de Problemas](#solucion-de-problemas)

---

## Descripcion General

El Radar de Velocidad es un sistema que permite medir la velocidad de objetos (vehiculos, personas, etc.) utilizando dos sensores de movimiento conectados a una placa Arduino. El sistema calcula la velocidad basandose en el tiempo que tarda un objeto en recorrer la distancia entre ambos sensores.

### Componentes del Sistema

- **Arduino + Sensores**: Detectan el paso del objeto y envian senales a la API
- **FastAPI (Backend)**: Recibe las senales, calcula velocidades y almacena datos
- **Django (Frontend)**: Muestra los datos en un dashboard web interactivo
- **SQLite**: Base de datos para almacenar mediciones y configuracion

---

## Arquitectura del Sistema

```text
+------------------+          +------------------+
|     Arduino      |   HTTP   |     FastAPI      |
| Sensor 1 ------> | POST --> |   Puerto 8080    |
| Sensor 2 ------> |          |   (API REST)     |
+------------------+          +--------+---------+
                                       |
                                       v
                              +--------+---------+
                              |     SQLite       |
                              | radar_velocidad.db|
                              +--------+---------+
                                       ^
                                       | HTTP
                              +--------+---------+
                              |     Django       |
                              |   Puerto 8000    |
                              |   (Frontend)     |
                              +------------------+
```

### Flujo de Datos

1. El **Sensor 1** detecta movimiento y Arduino envia POST a `/mediciones/`
2. FastAPI registra el timestamp inicial (medicion incompleta)
3. El **Sensor 2** detecta movimiento y Arduino envia otro POST
4. FastAPI calcula: `velocidad = distancia / tiempo_transcurrido`
5. Django consulta la API y muestra los datos en el dashboard

---

## Requisitos Previos

### Software Necesario

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Hardware (para mediciones reales)

- Placa Arduino (Uno, Nano, ESP32, etc.)
- 2 sensores de movimiento (PIR, ultrasonicos, o infrarojos)
- Conexion WiFi o USB para comunicacion con el servidor

---

## Instalacion

### Paso 1: Clonar o Descargar el Proyecto

```bash
git clone https://github.com/tu-usuario/Proyecto_CE_Python_Velocidad.git
cd Proyecto_CE_Python_Velocidad
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias de FastAPI

```bash
cd api
pip install -r requirements.txt
```

Dependencias instaladas:

- `fastapi` - Framework web asincrono
- `uvicorn` - Servidor ASGI
- `sqlalchemy` - ORM para base de datos
- `pydantic` - Validacion de datos

### Paso 4: Instalar Dependencias de Django

```bash
cd ../frontend
pip install -r requirements.txt
```

Dependencias instaladas:

- `Django` - Framework web
- `requests` - Cliente HTTP

### Paso 5: Configurar Django

```bash
# Desde la carpeta frontend/
python manage.py migrate
```

---

## Configuracion

### Configuracion de FastAPI

El archivo `api/database.py` contiene la configuracion de la base de datos:

```python
DATABASE_URL = "sqlite:///db/radar_velocidad.db"
```

Para cambiar a otra base de datos (ej. PostgreSQL):

```python
DATABASE_URL = "postgresql://usuario:password@localhost/radar_velocidad"
```

### Configuracion de Django

El archivo `frontend/frontend/settings.py` contiene:

```python
# URL de la API FastAPI
FASTAPI_BASE_URL = 'http://localhost:8080'

# Zona horaria
TIME_ZONE = 'Europe/Madrid'

# Idioma
LANGUAGE_CODE = 'es-es'
```

### Configuracion de Distancia entre Sensores

La distancia entre sensores se puede configurar de dos formas:

1. **Via API**: PUT a `/configuracion/distancia_sensores`
2. **Via Frontend**: En la pagina de Configuracion (`/configuracion/`)

---

## Arranque del Sistema

### Opcion A: Arranque Manual (Desarrollo)

Necesitas **dos terminales** abiertas:

**Terminal 1 - FastAPI:**

```bash
cd api
uvicorn main:app --reload --port 8080
```

Salida esperada:

```text
INFO:     Uvicorn running on http://127.0.0.1:8080
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete
```

**Terminal 2 - Django:**

```bash
cd frontend
python manage.py runserver
```

Salida esperada:

```text
Django version 5.x.x
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Opcion B: Script de Arranque (Windows)

Crear archivo `iniciar.bat` en la raiz del proyecto:

```batch
@echo off
start cmd /k "cd api && uvicorn main:app --reload --port 8080"
timeout /t 3
start cmd /k "cd frontend && python manage.py runserver"
echo Servidores iniciados!
echo FastAPI: http://localhost:8080
echo Django: http://localhost:8000
```

### Opcion C: Script de Arranque (Linux/Mac)

Crear archivo `iniciar.sh` en la raiz del proyecto:

```bash
#!/bin/bash
cd api && uvicorn main:app --reload --port 8080 &
sleep 3
cd ../frontend && python manage.py runserver &
echo "Servidores iniciados!"
echo "FastAPI: http://localhost:8080"
echo "Django: http://localhost:8000"
```

---

## Uso de la Aplicacion

### Acceso al Frontend

Abrir en el navegador: **http://localhost:8000**

### Paginas Disponibles

| URL | Descripcion |
|-----|-------------|
| `/` | Dashboard principal con estadisticas y ultimas mediciones |
| `/mediciones/` | Lista completa de mediciones con filtros por fecha |
| `/mediciones/<id>/` | Detalle de una medicion especifica |
| `/reportes/` | Graficos y estadisticas avanzadas |
| `/configuracion/` | Configurar distancia entre sensores |

### Dashboard Principal

El dashboard muestra:

- **Total de mediciones** registradas
- **Velocidad promedio** de todas las mediciones
- **Velocidad maxima** registrada
- **Excesos de velocidad** (superiores a 50 km/h)
- **Tabla** con las ultimas 10 mediciones

### Registro de Mediciones (Simulacion)

Para probar el sistema sin Arduino, puedes simular mediciones usando curl o Postman:

```bash
# Primera senal (sensor 1)
curl -X POST http://localhost:8080/mediciones/

# Esperar unos segundos...

# Segunda senal (sensor 2) - Esto completara la medicion
curl -X POST http://localhost:8080/mediciones/
```

O acceder a la documentacion interactiva: **http://localhost:8080/docs**

### Interpretacion de Datos

- **Velocidad (km/h)**: Velocidad en kilometros por hora
- **Velocidad (m/s)**: Velocidad en metros por segundo
- **Tiempo recorrido**: Segundos entre sensor 1 y sensor 2
- **Exceso**: Indica si supera 50 km/h (limite configurable)

---

## API Endpoints

### Documentacion Interactiva

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Endpoints Disponibles

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| POST | `/mediciones/` | Registrar nueva medicion |
| GET | `/mediciones/` | Listar mediciones (paginado) |
| GET | `/mediciones/{id}` | Obtener medicion por ID |
| GET | `/estadisticas/` | Obtener estadisticas generales |
| GET | `/configuracion/` | Listar configuracion |
| GET | `/configuracion/{clave}` | Obtener configuracion por clave |
| PUT | `/configuracion/{clave}` | Actualizar configuracion |

### Ejemplos de Uso

**Registrar medicion:**

```bash
curl -X POST http://localhost:8080/mediciones/
```

**Listar ultimas 10 mediciones:**

```bash
curl "http://localhost:8080/mediciones/?limit=10"
```

**Obtener estadisticas:**

```bash
curl http://localhost:8080/estadisticas/
```

**Cambiar distancia de sensores:**

```bash
curl -X PUT http://localhost:8080/configuracion/distancia_sensores \
  -H "Content-Type: application/json" \
  -d '{"valor": "150"}'
```

---

## Solucion de Problemas

### Error: "No module named 'fastapi'"

```bash
pip install -r api/requirements.txt
```

### Error: "No module named 'django'"

```bash
pip install -r frontend/requirements.txt
```

### Error: "Address already in use"

El puerto ya esta ocupado. Soluciones:

```bash
# Cambiar puerto de FastAPI
uvicorn main:app --port 8081

# Cambiar puerto de Django
python manage.py runserver 8001
```

### Error: "Connection refused" en Django

FastAPI no esta ejecutandose. Verificar que el servidor este activo en el puerto 8080.

### La base de datos no se crea

Verificar que existe la carpeta `db/`:

```bash
mkdir db
```

### Las mediciones no aparecen en Django

1. Verificar que FastAPI este corriendo
2. Verificar la URL en `settings.py`: `FASTAPI_BASE_URL`
3. Revisar la consola del navegador para errores

---

## Codigo Arduino (Ejemplo)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "TU_WIFI";
const char* password = "TU_PASSWORD";
const char* serverUrl = "http://192.168.1.100:8080/mediciones/";

const int SENSOR_1_PIN = 2;
const int SENSOR_2_PIN = 3;

void setup() {
  Serial.begin(115200);
  pinMode(SENSOR_1_PIN, INPUT);
  pinMode(SENSOR_2_PIN, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi conectado");
}

void enviarMedicion() {
  HTTPClient http;
  http.begin(serverUrl);
  int httpCode = http.POST("");
  http.end();
}

void loop() {
  if (digitalRead(SENSOR_1_PIN) == HIGH) {
    enviarMedicion();
    delay(500); // Anti-rebote
  }

  if (digitalRead(SENSOR_2_PIN) == HIGH) {
    enviarMedicion();
    delay(500); // Anti-rebote
  }
}
```

---

## Contacto y Soporte

Para reportar problemas o sugerencias, crear un issue en el repositorio del proyecto.
