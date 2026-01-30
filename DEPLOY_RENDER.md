# Despliegue en Render - Sistema Radar de Velocidad

Este documento explica cómo desplegar el sistema de radar de velocidad en Render con dos aplicaciones separadas.

## 🏗️ Arquitectura de Despliegue

El sistema se despliega como **dos servicios web independientes**:

1. **API Backend** (FastAPI) - `radar-velocidad-api`
2. **Frontend Web** (Django) - `radar-velocidad-frontend`

## 📋 Requisitos Previos

- Cuenta en [Render.com](https://render.com)
- Repositorio Git con el código del proyecto
- Rama `feature/integracion-arduino-radar` actualizada

## 🚀 Pasos para Desplegar

### 1. Preparar el Repositorio

Asegúrate de que tienes todos los archivos necesarios:

```
├── render.yaml                 # Configuración de Render
├── api/
│   ├── requirements.txt        # Dependencias del API
│   ├── start.py               # Script de inicio
│   ├── main.py                # Aplicación FastAPI
│   └── ...
└── frontend/
    ├── requirements.txt        # Dependencias del frontend
    ├── manage.py              # Django management
    └── ...
```

### 2. Conectar con Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Haz clic en "New +" → "Blueprint"
3. Conecta tu repositorio de GitHub
4. Selecciona la rama `feature/integracion-arduino-radar`
5. Render detectará automáticamente el archivo `render.yaml`

### 3. Configurar Variables de Entorno

Render configurará automáticamente las siguientes variables:

**API Backend:**
- `PYTHON_VERSION`: 3.11
- `DATABASE_URL`: sqlite:///./radar_velocidad.db
- `PORT`: Asignado automáticamente por Render

**Frontend:**
- `PYTHON_VERSION`: 3.11
- `DEBUG`: False
- `SECRET_KEY`: Generado automáticamente
- `API_URL`: URL del servicio API (configurado automáticamente)
- `PORT`: Asignado automáticamente por Render

### 4. Proceso de Despliegue

Render ejecutará automáticamente:

**Para el API:**
1. `cd api && pip install -r requirements.txt`
2. `cd api && python start.py`

**Para el Frontend:**
1. `cd frontend && pip install -r requirements.txt`
2. `cd frontend && python manage.py collectstatic --noinput`
3. `cd frontend && python manage.py migrate`
4. `cd frontend && gunicorn frontend.wsgi:application --bind 0.0.0.0:$PORT`

## 🔗 URLs de Acceso

Una vez desplegado, tendrás:

- **API**: `https://radar-velocidad-api.onrender.com`
  - Documentación: `https://radar-velocidad-api.onrender.com/docs`
  - Endpoint mediciones: `https://radar-velocidad-api.onrender.com/mediciones/`

- **Frontend**: `https://radar-velocidad-frontend.onrender.com`
  - Dashboard principal: `https://radar-velocidad-frontend.onrender.com/`

## 🧪 Verificar el Despliegue

### Probar el API

```bash
# Crear una medición de prueba
curl -X POST https://radar-velocidad-api.onrender.com/mediciones/

# Esperar unos segundos y crear otra para completar la medición
curl -X POST https://radar-velocidad-api.onrender.com/mediciones/

# Ver las mediciones
curl https://radar-velocidad-api.onrender.com/mediciones/
```

### Probar el Frontend

1. Visita `https://radar-velocidad-frontend.onrender.com/`
2. Verifica que se muestren las mediciones
3. Prueba la navegación entre páginas

## 🔧 Configuración para Arduino

Una vez desplegado, configura tus placas Arduino para enviar datos a:

```
POST https://radar-velocidad-api.onrender.com/mediciones/
```

Ejemplo de código Arduino:
```cpp
const char* serverURL = "https://radar-velocidad-api.onrender.com";
const char* endpoint = "/mediciones/";

// En tu función de detección:
HTTPClient http;
http.begin(serverURL + String(endpoint));
http.addHeader("Content-Type", "application/json");
int httpResponseCode = http.POST("{}");
```

## 📊 Monitoreo

Render proporciona:
- **Logs en tiempo real** para ambos servicios
- **Métricas de rendimiento** (CPU, memoria, requests)
- **Alertas automáticas** en caso de errores
- **Reinicio automático** si el servicio falla

## 🛠️ Troubleshooting

### Problemas Comunes

1. **Error de CORS**: Verifica que `API_URL` esté configurado correctamente
2. **Base de datos no inicializada**: Los logs del API mostrarán el proceso de inicialización
3. **Archivos estáticos no cargan**: Verifica que `collectstatic` se ejecutó correctamente

### Ver Logs

En el dashboard de Render:
1. Selecciona el servicio (API o Frontend)
2. Ve a la pestaña "Logs"
3. Filtra por tipo de log (Build, Deploy, Runtime)

## 🔄 Actualizaciones

Para actualizar el despliegue:
1. Haz push de los cambios a la rama `feature/integracion-arduino-radar`
2. Render detectará automáticamente los cambios
3. Se ejecutará un nuevo despliegue automáticamente

## 💰 Costos

Render ofrece:
- **Plan gratuito**: Suficiente para desarrollo y pruebas
- **Plan de pago**: Para producción con mayor rendimiento

El plan gratuito incluye:
- 750 horas de cómputo por mes
- Suspensión automática tras inactividad
- Reinicio automático al recibir requests

## 🔒 Seguridad

Configuraciones de seguridad aplicadas:
- `DEBUG=False` en producción
- `SECRET_KEY` generado automáticamente
- CORS configurado para dominios específicos
- HTTPS habilitado automáticamente por Render

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en el dashboard de Render
2. Consulta la [documentación de Render](https://render.com/docs)
3. Verifica la configuración en `render.yaml`