# Código MicroPython - Sensor de Velocidad

## Configuración

Editar las constantes al inicio de `main.py`:

```python
WIFI_SSID = 'TU_WIFI'
WIFI_PASSWORD = 'TU_PASSWORD'
API_URL = "http://IP_SERVIDOR:8080/mediciones/"
```

## Pines

| Pin | Función |
|-----|---------|
| 14 | LED Verde (sistema OK) |
| 27 | LED Rojo (error/exceso) |
| 12 | Sensor de movimiento (PIR/IR) |

## Flujo de funcionamiento

```
┌─────────────────┐
│  Iniciar placa  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Conectar WiFi  │──Error──▶ Parpadeo LED rojo
└────────┬────────┘
         ▼
┌─────────────────┐
│  Sincronizar    │
│  tiempo NTP     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  LED verde ON   │
│  Sistema listo  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Esperar        │◀─────────────────┐
│  detección      │                  │
└────────┬────────┘                  │
         ▼                           │
┌─────────────────┐                  │
│  Sensor activado│                  │
│  (interrupción) │                  │
└────────┬────────┘                  │
         ▼                           │
┌─────────────────┐                  │
│  Enviar POST    │                  │
│  con timestamp  │                  │
└────────┬────────┘                  │
         ▼                           │
┌─────────────────┐                  │
│  ¿Velocidad?    │──No──────────────┤
└────────┬────────┘                  │
         │ Sí                        │
         ▼                           │
┌─────────────────┐                  │
│  > 50 km/h?     │                  │
│  Rojo : Verde   │──────────────────┘
└─────────────────┘
```

## Mejoras implementadas

### 1. Debounce de sensor
Evita detecciones múltiples por rebote del sensor:
```python
DEBOUNCE_MS = 500  # Ignora activaciones en 500ms
```

### 2. Envío fuera de interrupción
Las peticiones HTTP no se hacen dentro del handler de interrupción (causa crashes):
```python
micropython.schedule(lambda _: enviar_medicion(timestamp), None)
```

### 3. Feedback visual
| LED | Significado |
|-----|-------------|
| Verde fijo | Sistema OK, esperando |
| Verde parpadeo (3x) | Velocidad normal |
| Rojo parpadeo (3x) | Exceso de velocidad (>50 km/h) |
| Rojo parpadeo (5x) | Error de conexión |
| Rojo parpadeo continuo | Error WiFi inicial |

### 4. Timestamps precisos
Usa NTP + ticks para precisión de milisegundos:
```python
epoch_base + time.ticks_diff(time.ticks_ms(), ticks_base) / 1000
```

## Datos enviados a la API

```json
POST /mediciones/
{
  "timestamp": 1706985432.123
}
```

## Respuesta esperada

**Primer sensor:**
```json
{
  "mensaje": "Sensor 1 activado. Esperando sensor 2..."
}
```

**Segundo sensor:**
```json
{
  "mensaje": "Velocidad: 72.00 km/h",
  "velocidad_ms": 20.0,
  "velocidad_kmh": 72.0,
  "tiempo_segundos": 5.0
}
```

## Simulador

Puedes probar el código en [Wokwi](https://wokwi.com/) con la configuración WiFi:
```python
WIFI_SSID = 'Wokwi-GUEST'
WIFI_PASSWORD = ''
```
