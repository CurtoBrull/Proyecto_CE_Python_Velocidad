# 🚀 Guía Paso a Paso - Despliegue en Render (Plan Gratuito)

Esta guía te llevará paso a paso para desplegar tu sistema de radar de velocidad en Render usando el plan gratuito.

## 📋 Antes de Empezar

- ✅ Cuenta gratuita en [render.com](https://render.com)
- ✅ Repositorio en GitHub con el código
- ✅ Rama `feature/deploy-render` con los cambios

## 🎯 Paso 1: Desplegar el API Backend

### 1.1 Crear el Servicio API

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"Web Service"**
3. Selecciona **"Build and deploy from a Git repository"**
4. Haz clic en **"Connect"** junto a tu repositorio
5. Si no aparece, haz clic en **"Configure account"** y autoriza Render

### 1.2 Configurar el API

**Configuración básica:**
- **Name**: `radar-velocidad-api`
- **Branch**: `feature/deploy-render`
- **Root Directory**: Dejar vacío
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  cd api && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  cd api && python start.py
  ```

### 1.3 Variables de Entorno del API

En la sección **"Environment Variables"**, añade:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DATABASE_URL` | `sqlite:///./radar_velocidad.db` |

### 1.4 Finalizar API

1. Selecciona **"Free"** plan
2. Haz clic en **"Create Web Service"**
3. **¡IMPORTANTE!** Copia la URL generada (ej: `https://radar-velocidad-api-abc123.onrender.com`)
4. Guarda esta URL, la necesitarás para el frontend

---

## 🎯 Paso 2: Desplegar el Frontend

### 2.1 Crear el Servicio Frontend

1. En el dashboard, haz clic en **"New +"** → **"Web Service"**
2. Selecciona **"Build and deploy from a Git repository"**
3. Conecta el **mismo repositorio**
4. Selecciona la rama `feature/deploy-render`

### 2.2 Configurar el Frontend

**Configuración básica:**
- **Name**: `radar-velocidad-frontend`
- **Branch**: `feature/deploy-render`
- **Root Directory**: Dejar vacío
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  cd frontend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start Command**: 
  ```
  cd frontend && gunicorn frontend.wsgi:application --bind 0.0.0.0:$PORT
  ```

### 2.3 Variables de Entorno del Frontend

En la sección **"Environment Variables"**, añade:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | `tu-clave-secreta-muy-segura-cambiar-en-produccion` |
| `API_URL` | `https://radar-velocidad-api-abc123.onrender.com` |

⚠️ **Importante**: Reemplaza `https://radar-velocidad-api-abc123.onrender.com` con la URL real de tu API del Paso 1.4

### 2.4 Finalizar Frontend

1. Selecciona **"Free"** plan
2. Haz clic en **"Create Web Service"**
3. **¡IMPORTANTE!** Copia la URL generada (ej: `https://radar-velocidad-frontend-xyz789.onrender.com`)

---

## 🎯 Paso 3: Configurar CORS en el API

### 3.1 Actualizar Variables del API

1. Ve al servicio **API** en tu dashboard
2. Ve a **"Environment"** en el menú lateral
3. Añade una nueva variable:

| Key | Value |
|-----|-------|
| `FRONTEND_URL` | `https://radar-velocidad-frontend-xyz789.onrender.com` |

⚠️ **Importante**: Reemplaza con la URL real de tu frontend del Paso 2.4

### 3.2 Redeploy del API

1. Ve a la pestaña **"Manual Deploy"**
2. Haz clic en **"Deploy latest commit"**
3. Espera a que termine el despliegue

---

## 🎯 Paso 4: Verificar el Despliegue

### 4.1 Probar el API

1. Ve a tu URL del API + `/docs` (ej: `https://radar-velocidad-api-abc123.onrender.com/docs`)
2. Deberías ver la documentación de FastAPI
3. Prueba el endpoint `/mediciones/` haciendo POST

### 4.2 Probar el Frontend

1. Ve a tu URL del frontend
2. Deberías ver el dashboard del radar de velocidad
3. Verifica que no hay errores de conexión al API

### 4.3 Script de Verificación

1. Edita el archivo `test_deployment.py`
2. Actualiza las URLs con las reales:
   ```python
   API_URL = "https://radar-velocidad-api-abc123.onrender.com"
   FRONTEND_URL = "https://radar-velocidad-frontend-xyz789.onrender.com"
   ```
3. Ejecuta: `python test_deployment.py`

---

## 🎯 Paso 5: Configurar Arduino

Una vez que todo funcione, configura tus placas Arduino:

```cpp
const char* serverURL = "https://radar-velocidad-api-abc123.onrender.com";
const char* endpoint = "/mediciones/";
```

---

## 🔧 Troubleshooting

### Problema: "Application failed to respond"

**Causa**: El servicio está iniciándose (plan gratuito)
**Solución**: Espera 1-2 minutos y recarga la página

### Problema: CORS Error en el frontend

**Causa**: `FRONTEND_URL` no configurado en el API
**Solución**: 
1. Ve al servicio API → Environment
2. Añade `FRONTEND_URL` con la URL del frontend
3. Redeploy el API

### Problema: Frontend no puede conectar al API

**Causa**: `API_URL` incorrecto en el frontend
**Solución**:
1. Ve al servicio Frontend → Environment
2. Verifica que `API_URL` sea correcto
3. Redeploy el frontend

### Problema: Base de datos vacía

**Causa**: Normal en primer despliegue
**Solución**: Haz algunas peticiones POST al endpoint `/mediciones/` para crear datos

---

## 📝 Checklist Final

- [ ] API desplegado y respondiendo en `/docs`
- [ ] Frontend desplegado y cargando correctamente
- [ ] Variables de entorno configuradas en ambos servicios
- [ ] CORS configurado (FRONTEND_URL en API)
- [ ] Script de verificación ejecutado exitosamente
- [ ] URLs documentadas para configuración Arduino

## 🎉 ¡Listo!

Tu sistema de radar de velocidad está desplegado y listo para recibir datos de las placas Arduino.

**URLs importantes:**
- API: `https://radar-velocidad-api-abc123.onrender.com`
- Frontend: `https://radar-velocidad-frontend-xyz789.onrender.com`
- Docs: `https://radar-velocidad-api-abc123.onrender.com/docs`