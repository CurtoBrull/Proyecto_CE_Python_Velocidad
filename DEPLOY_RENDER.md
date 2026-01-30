# Despliegue en Render - Sistema Radar de Velocidad (Plan Gratuito)

Este documento explica cómo desplegar el sistema de radar de velocidad en Render con dos aplicaciones separadas usando el plan gratuito.

## 🏗️ Arquitectura de Despliegue

El sistema se despliega como **dos servicios web independientes**:

1. **API Backend** (FastAPI) - `radar-velocidad-api`
2. **Frontend Web** (Django) - `radar-velocidad-frontend`

## 📋 Requisitos Previos

- Cuenta gratuita en [Render.com](https://render.com)
- Repositorio Git con el código del proyecto
- Rama `feature/deploy-render` actualizada

## 🚀 Pasos para Desplegar (Plan Gratuito)

### 1. Preparar el Repositorio

Asegúrate de que tienes todos los archivos necesarios:

```
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

### 2. Desplegar API Backend (Servicio 1)

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Haz clic en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Selecciona la rama `feature/deploy-render`
5. Configura el servicio:

**Configuración del API:**
- **Name**: `radar-velocidad-api`
- **Environment**: `Python 3`
- **Build Command**: `cd api && pip install -r requirements.txt`
- **Start Command**: `cd api && python start.py`
- **Plan**: `Free`

**Variables de Entorno del API:**
- `PYTHON_VERSION`: `3.11`
- `DATABASE_URL`: `sqlite:///./radar_velocidad.db`

6. Haz clic en "Create Web Service"
7. **¡IMPORTANTE!** Anota la URL generada (ej: `https://radar-velocidad-api-xxxx.onrender.com`)

### 3. Desplegar Frontend (Servicio 2)

1. En el Dashboard, haz clic en "New +" → "Web Service"
2. Conecta el mismo repositorio
3. Selecciona la rama `feature/deploy-render`
4. Configura el servicio:

**Configuración del Frontend:**
- **Name**: `radar-velocidad-frontend`
- **Environment**: `Python 3`
- **Build Command**: `cd frontend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command**: `cd frontend && gunicorn frontend.wsgi:application --bind 0.0.0.0:$PORT`
- **Plan**: `Free`

**Variables de Entorno del Frontend:**
- `PYTHON_VERSION`: `3.11`
- `DEBUG`: `False`
- `SECRET_KEY`: `tu-clave-secreta-muy-segura-aqui-cambiar-en-produccion`
- `API_URL`: `https://radar-velocidad-api-xxxx.onrender.com` (URL del paso anterior)

5. Haz clic en "Create Web Service"

### 4. Actualizar CORS en el API

Una vez que tengas la URL del frontend, necesitas actualizar el API:

1. Ve al servicio del API en Render
2. Añade una variable de entorno:
   - **Key**: `FRONTEND_URL`
   - **Value**: `https://radar-velocidad-frontend-yyyy.onrender.com` (URL de tu frontend)
3. Redespliega el servicio API

### 5. Configurar Variables de Entorno

**API Backend:**
```
PYTHON_VERSION=3.11
DATABASE_URL=sqlite:///./radar_velocidad.db
FRONTEND_URL=https://radar-velocidad-frontend-yyyy.onrender.com
```

**Frontend:**
```
PYTHON_VERSION=3.11
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiar-en-produccion
API_URL=https://radar-velocidad-api-xxxx.onrender.com
ALLOWED_HOST=radar-velocidad-frontend-yyyy.onrender.com
```

### 6. Proceso de Despliegue

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

- **API**: `https://radar-velocidad-api-xxxx.onrender.com`
  - Documentación: `https://radar-velocidad-api-xxxx.onrender.com/docs`
  - Endpoint mediciones: `https://radar-velocidad-api-xxxx.onrender.com/mediciones/`

- **Frontend**: `https://radar-velocidad-frontend-yyyy.onrender.com`
  - Dashboard principal: `https://radar-velocidad-frontend-yyyy.onrender.com/`

*Nota: Las URLs exactas dependerán de los nombres que asigne Render automáticamente.*

## 🧪 Verificar el Despliegue

### Probar el API

```bash
# Reemplaza con tu URL real del API
API_URL="https://radar-velocidad-api-xxxx.onrender.com"

# Crear una medición de prueba
curl -X POST $API_URL/mediciones/

# Esperar unos segundos y crear otra para completar la medición
sleep 3
curl -X POST $API_URL/mediciones/

# Ver las mediciones
curl $API_URL/mediciones/
```

### Probar el Frontend

1. Visita tu URL del frontend
2. Verifica que se muestren las mediciones
3. Prueba la navegación entre páginas

## 🔧 Configuración para Arduino

Una vez desplegado, configura tus placas Arduino para enviar datos a tu URL del API:

```cpp
// Reemplaza con tu URL real
const char* serverURL = "https://radar-velocidad-api-xxxx.onrender.com";
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

1. **Error de CORS**: 
   - Verifica que `FRONTEND_URL` esté configurado en el API
   - Verifica que `API_URL` esté configurado en el frontend
   
2. **Base de datos no inicializada**: 
   - Los logs del API mostrarán el proceso de inicialización
   
3. **Archivos estáticos no cargan**: 
   - Verifica que `collectstatic` se ejecutó correctamente en el build
   
4. **Frontend no puede conectar al API**:
   - Verifica que las URLs estén correctas en las variables de entorno
   - Revisa los logs del frontend para errores de conexión

### Ver Logs

En el dashboard de Render:
1. Selecciona el servicio (API o Frontend)
2. Ve a la pestaña "Logs"
3. Filtra por tipo de log (Build, Deploy, Runtime)

### Comandos de Verificación

Puedes usar el script incluido para verificar el despliegue:

```bash
# Edita las URLs en test_deployment.py con tus URLs reales
python test_deployment.py
```

## � Actualizaciones

Para actualizar el despliegue:
1. Haz push de los cambios a la rama `feature/deploy-render`
2. Ve al dashboard de Render
3. Selecciona cada servicio y haz clic en "Manual Deploy"
4. O configura auto-deploy desde GitHub en la configuración del servicio

## � Limitaciones del Plan Gratuito

El plan gratuito de Render incluye:
- **750 horas de cómputo por mes** (suficiente para 2 servicios)
- **Suspensión automática** tras 15 minutos de inactividad
- **Reinicio automático** al recibir requests (puede tardar 30-60 segundos)
- **Límite de ancho de banda**: 100GB/mes

**Importante**: Los servicios se suspenden automáticamente, por lo que la primera request después de inactividad será más lenta.

## 🔒 Seguridad

Configuraciones de seguridad aplicadas:
- `DEBUG=False` en producción
- `SECRET_KEY` configurado manualmente (cámbialo por uno seguro)
- CORS configurado para dominios específicos
- HTTPS habilitado automáticamente por Render
- Variables de entorno para configuración sensible

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en el dashboard de Render
2. Consulta la [documentación de Render](https://render.com/docs)
3. Verifica que las variables de entorno estén configuradas correctamente
4. Asegúrate de que las URLs entre servicios sean correctas

## 🎯 Checklist de Despliegue

- [ ] API desplegado y funcionando
- [ ] Frontend desplegado y funcionando  
- [ ] Variables de entorno configuradas en ambos servicios
- [ ] CORS actualizado con URL del frontend
- [ ] Pruebas de conectividad exitosas
- [ ] URLs documentadas para configuración Arduino