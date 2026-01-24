# Plan de Implementación: Integración Arduino Radar

## Visión General

Este plan implementa la integración completa de placas ESP32 con el sistema de radar de velocidad existente. La implementación se realizará en MicroPython para facilitar el desarrollo, configuración y mantenimiento de las placas. MicroPython ofrece sintaxis familiar, desarrollo más rápido y facilidad de configuración remota. Cada tarea construye incrementalmente sobre las anteriores, culminando en un sistema completo de sensores que se comunica con el backend FastAPI existente.

## Tareas

- [ ] 1. Configurar estructura del proyecto y dependencias
  - Instalar MicroPython en ESP32 y configurar entorno de desarrollo
  - Configurar librerías necesarias (urequests, ujson, ntptime, machine)
  - Definir estructura de archivos principales (main.py, config.py, wifi_manager.py)
  - _Requerimientos: Todos los requerimientos técnicos_

- [ ] 2. Implementar gestor de configuración y almacenamiento persistente
  - [ ] 2.1 Crear módulo config_manager.py con clase ConfigManager
    - Implementar carga y guardado en archivo JSON en sistema de archivos
    - Definir valores por defecto y validación de parámetros
    - _Requerimientos: 7.3, 7.4_
  
  - [ ]* 2.2 Escribir test de propiedad para persistencia de configuración
    - **Propiedad 14: Aplicación inmediata de configuración**
    - **Valida: Requerimientos 7.2, 7.4**
  
  - [ ]* 2.3 Escribir test de propiedad para validación de parámetros
    - **Propiedad 15: Validación de parámetros**
    - **Valida: Requerimientos 7.3**

- [ ] 3. Implementar controlador de LED de estado
  - [ ] 3.1 Crear módulo status_led.py con clase StatusLED
    - Implementar control RGB usando machine.PWM para patrones de parpadeo
    - Configurar pines GPIO para LED RGB (pines configurables)
    - _Requerimientos: 4.1, 4.2, 4.3, 4.4, 4.5, 5.3_
  
  - [ ]* 3.2 Escribir test de propiedad para correspondencia estado-LED
    - **Propiedad 8: Correspondencia estado-LED**
    - **Valida: Requerimientos 4.1, 4.2, 4.3, 4.4, 4.5**

- [ ] 4. Implementar gestor de conectividad WiFi
  - [ ] 4.1 Crear módulo wifi_manager.py con clase WiFiManager
    - Implementar punto de acceso temporal usando network.WLAN(network.AP_IF)
    - Crear servidor web simple con socket para introducir credenciales
    - _Requerimientos: 1.1, 1.2_
  
  - [ ] 4.2 Implementar conexión y reconexión automática
    - Lógica de reconexión usando network.WLAN(network.STA_IF)
    - Timer para reconexión cada 30 segundos tras pérdida de conexión
    - Activar modo configuración tras 10 fallos consecutivos
    - _Requerimientos: 1.3, 1.4, 1.5_
  
  - [ ]* 4.3 Escribir test de propiedad para configuración WiFi inicial
    - **Propiedad 1: Configuración WiFi inicial**
    - **Valida: Requerimientos 1.1, 1.2**
  
  - [ ]* 4.4 Escribir test de propiedad para persistencia y conexión WiFi
    - **Propiedad 2: Persistencia y conexión WiFi**
    - **Valida: Requerimientos 1.3**
  
  - [ ]* 4.5 Escribir test de propiedad para reconexión automática
    - **Propiedad 3: Reconexión automática WiFi**
    - **Valida: Requerimientos 1.4, 1.5**

- [ ] 5. Checkpoint - Verificar conectividad básica
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.

- [ ] 6. Implementar controlador de sensor ultrasónico
  - [ ] 6.1 Crear módulo ultrasonic_sensor.py con clase UltrasonicSensor
    - Configurar pines GPIO para trigger y echo usando machine.Pin
    - Implementar lectura de distancia con machine.time_pulse_us()
    - _Requerimientos: 2.1, 5.2_
  
  - [ ] 6.2 Implementar filtrado de detecciones múltiples
    - Filtro temporal de 2 segundos usando time.ticks_ms()
    - Validación de lecturas consistentes (filtro anti-ruido)
    - _Requerimientos: 2.2_
  
  - [ ] 6.3 Implementar recuperación automática de sensor
    - Detección de fallos y reinicio automático del sensor
    - Modo error crítico tras 3 fallos consecutivos
    - _Requerimientos: 6.4, 6.5_
  
  - [ ]* 6.4 Escribir test de propiedad para detección y filtrado
    - **Propiedad 4: Detección y filtrado de objetos**
    - **Valida: Requerimientos 2.1, 2.2**
  
  - [ ]* 6.5 Escribir test de propiedad para disponibilidad continua
    - **Propiedad 6: Disponibilidad continua del sensor**
    - **Valida: Requerimientos 2.4**
  
  - [ ]* 6.6 Escribir test de propiedad para configuración de hardware
    - **Propiedad 9: Configuración correcta de hardware**
    - **Valida: Requerimientos 5.2, 5.3**
  
  - [ ]* 6.7 Escribir test de propiedad para recuperación automática
    - **Propiedad 12: Recuperación automática de sensor**
    - **Valida: Requerimientos 6.4, 6.5**

- [ ] 7. Implementar cliente HTTP y comunicación con backend
  - [ ] 7.1 Crear módulo http_client.py con clase HTTPClient
    - Implementar peticiones POST usando urequests a /mediciones/ con formato JSON
    - Configurar headers Content-Type: application/json usando ujson
    - _Requerimientos: 3.1, 3.2_
  
  - [ ] 7.2 Implementar manejo de respuestas y reintentos
    - Lógica de reintentos (3 intentos con time.sleep() de 1 segundo)
    - Manejo de códigos de respuesta 200, 4xx, 5xx
    - _Requerimientos: 3.3, 3.4, 3.5_
  
  - [ ] 7.3 Implementar almacenamiento offline y sincronización
    - Lista local para hasta 50 mediciones durante desconexión
    - Envío en orden cronológico tras reconexión
    - Gestión FIFO cuando se llena la memoria
    - _Requerimientos: 6.1, 6.2, 6.3_
  
  - [ ]* 7.4 Escribir test de propiedad para transmisión HTTP
    - **Propiedad 5: Transmisión HTTP tras detección**
    - **Valida: Requerimientos 2.3, 3.1, 3.2**
  
  - [ ]* 7.5 Escribir test de propiedad para manejo de respuestas
    - **Propiedad 7: Manejo de respuestas HTTP**
    - **Valida: Requerimientos 3.3, 3.4, 3.5**
  
  - [ ]* 7.6 Escribir test de propiedad para almacenamiento offline
    - **Propiedad 10: Almacenamiento offline**
    - **Valida: Requerimientos 6.1, 6.3**
  
  - [ ]* 7.7 Escribir test de propiedad para sincronización tras reconexión
    - **Propiedad 11: Sincronización tras reconexión**
    - **Valida: Requerimientos 6.2**

- [ ] 8. Implementar sincronización temporal NTP
  - [ ] 8.1 Crear módulo ntp_client.py con funciones de sincronización
    - Sincronización inicial usando ntptime.settime()
    - Resincronización automática tras reconexión WiFi
    - Manejo de fallos NTP con time.time() interno
    - _Requerimientos: 8.1, 8.3, 8.4_
  
  - [ ] 8.2 Implementar timestamps precisos en mediciones
    - Inclusión de marca de tiempo usando time.ticks_ms() en peticiones HTTP
    - Marcado de mediciones como "no sincronizadas" cuando falla NTP
    - _Requerimientos: 8.2, 8.3_
  
  - [ ]* 8.3 Escribir test de propiedad para gestión NTP
    - **Propiedad 17: Gestión completa de NTP**
    - **Valida: Requerimientos 8.1, 8.3, 8.4**
  
  - [ ]* 8.4 Escribir test de propiedad para timestamps precisos
    - **Propiedad 18: Timestamps precisos en mediciones**
    - **Valida: Requerimientos 8.2**

- [ ] 9. Implementar interfaz web de configuración
  - [ ] 9.1 Crear módulo web_server.py con servidor web embebido
    - Página HTML simple usando socket para ajustar parámetros
    - Endpoints REST para GET/POST de configuración
    - _Requerimientos: 7.1_
  
  - [ ] 9.2 Implementar página de diagnóstico
    - Información de tiempo de funcionamiento usando time.ticks_ms()
    - Estado de componentes y estadísticas de conectividad
    - _Requerimientos: 7.5_
  
  - [ ]* 9.3 Escribir test de propiedad para interfaz web
    - **Propiedad 13: Interfaz web de configuración**
    - **Valida: Requerimientos 7.1**
  
  - [ ]* 9.4 Escribir test de propiedad para información de diagnóstico
    - **Propiedad 16: Información de diagnóstico**
    - **Valida: Requerimientos 7.5**

- [ ] 10. Checkpoint - Verificar funcionalidad completa
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.

- [ ] 11. Integrar todos los componentes en loop principal
  - [ ] 11.1 Crear main.py con estructura principal del firmware
    - Inicialización de todos los módulos (import de clases)
    - Loop principal con gestión de estados usando asyncio si es necesario
    - Integración de machine.WDT() para estabilidad del sistema
    - _Requerimientos: Todos_
  
  - [ ] 11.2 Implementar máquina de estados del sistema
    - Estados: INIT, CONFIG_MODE, CONNECTING, OPERATIONAL, ERROR
    - Transiciones entre estados según eventos
    - Coordinación entre LED, WiFi, sensor y HTTP usando threading si es necesario
    - _Requerimientos: Todos_
  
  - [ ]* 11.3 Escribir tests de integración para sistema completo
    - Verificar transiciones de estado correctas
    - Simular escenarios de fallo y recuperación
    - _Requerimientos: Todos_

- [ ] 12. Crear documentación de instalación y configuración
  - [ ] 12.1 Escribir guía de instalación de MicroPython y hardware
    - Instrucciones para flashear MicroPython en ESP32
    - Esquema de conexiones para sensor HC-SR04 y LED RGB
    - Lista de componentes necesarios y especificaciones
    - _Requerimientos: 5.1, 5.4, 5.5_
  
  - [ ] 12.2 Crear manual de configuración inicial
    - Proceso de subida de archivos .py al ESP32 usando ampy o Thonny
    - Configuración WiFi mediante AP temporal
    - Configuración de parámetros del sistema
    - _Requerimientos: 1.1, 1.2, 7.1, 7.5_
  
  - [ ] 12.3 Documentar integración con backend existente
    - Configuración de IP del servidor FastAPI en config.json
    - Verificación de comunicación con endpoints usando REPL
    - Troubleshooting de problemas comunes en MicroPython
    - _Requerimientos: 3.1, 3.2_

- [ ] 13. Checkpoint final - Verificar sistema completo
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.

## Notas

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia requerimientos específicos para trazabilidad
- Los checkpoints aseguran validación incremental
- Los tests de propiedades validan corrección universal
- Los tests unitarios validan ejemplos específicos y casos límite
- La implementación usa MicroPython para facilitar desarrollo y configuración