# Documento de Requerimientos

## Introducción

Este documento especifica los requerimientos para completar la integración de placas Arduino/ESP32 con el sistema de radar de velocidad existente. El sistema actual cuenta con un backend FastAPI funcional que maneja la lógica de medición de velocidad mediante un mecanismo de dos etapas, donde el primer sensor crea una medición incompleta y el segundo sensor completa la medición calculando la velocidad basada en el tiempo transcurrido entre ambas detecciones.

La integración Arduino proporcionará la capa física de sensores que se comunicará con el backend existente mediante peticiones HTTP, completando así la arquitectura del sistema de radar de velocidad.

## Glosario

- **Sistema_Radar**: El sistema completo de medición de velocidad incluyendo backend, frontend y sensores Arduino
- **Placa_Arduino**: Microcontrolador Arduino o ESP32 con capacidades WiFi
- **Sensor_Ultrasonico**: Sensor físico para detección de objetos (HC-SR04 o similar)
- **Backend_FastAPI**: Servidor FastAPI existente que procesa las mediciones
- **Endpoint_Mediciones**: Ruta HTTP POST /mediciones/ del backend para registrar activaciones
- **Red_WiFi**: Conexión inalámbrica para comunicación entre Arduino y backend
- **LED_Estado**: Indicador visual del estado de conexión y funcionamiento
- **Medicion_Incompleta**: Registro creado por el primer sensor sin velocidad calculada
- **Medicion_Completa**: Registro finalizado por el segundo sensor con velocidad calculada

## Requerimientos

### Requerimiento 1: Conectividad WiFi

**Historia de Usuario:** Como técnico instalador, quiero configurar fácilmente la conexión WiFi en las placas Arduino, para que puedan comunicarse con el servidor backend sin complicaciones técnicas.

#### Criterios de Aceptación

1. CUANDO se enciende una placa Arduino por primera vez, EL Sistema_Radar DEBERÁ crear un punto de acceso WiFi temporal para configuración inicial
2. CUANDO un usuario se conecta al punto de acceso de configuración, EL Sistema_Radar DEBERÁ mostrar una interfaz web simple para introducir credenciales WiFi
3. CUANDO se introducen credenciales WiFi válidas, LA Placa_Arduino DEBERÁ almacenar las credenciales en memoria no volátil y conectarse a la red especificada
4. CUANDO la conexión WiFi se pierde, LA Placa_Arduino DEBERÁ intentar reconectarse automáticamente cada 30 segundos
5. SI la reconexión falla después de 10 intentos, LA Placa_Arduino DEBERÁ reactivar el modo de configuración temporal

### Requerimiento 2: Detección de Objetos

**Historia de Usuario:** Como operador del sistema, quiero que los sensores detecten vehículos u objetos que pasen por el área de medición, para que el sistema pueda calcular su velocidad con precisión.

#### Criterios de Aceptación

1. CUANDO un objeto entra en el rango del sensor ultrasónico, EL Sensor_Ultrasonico DEBERÁ detectar la presencia del objeto a una distancia configurable
2. CUANDO se detecta un objeto, LA Placa_Arduino DEBERÁ filtrar detecciones múltiples del mismo objeto durante un período de 2 segundos
3. CUANDO se confirma una detección válida, LA Placa_Arduino DEBERÁ enviar inmediatamente una petición HTTP POST al Endpoint_Mediciones
4. CUANDO el objeto sale del rango de detección, EL Sensor_Ultrasonico DEBERÁ estar listo para la siguiente detección sin demora
5. CUANDO las condiciones ambientales afecten la detección, EL Sistema_Radar DEBERÁ mantener una precisión mínima del 95% en condiciones normales

### Requerimiento 3: Comunicación HTTP

**Historia de Usuario:** Como desarrollador del sistema, quiero que las placas Arduino se comuniquen correctamente con el backend FastAPI, para que las mediciones se registren de forma confiable en la base de datos.

#### Criterios de Aceptación

1. CUANDO se detecta un objeto, LA Placa_Arduino DEBERÁ enviar una petición HTTP POST a http://[IP_SERVIDOR]:8080/mediciones/
2. CUANDO se envía la petición HTTP, LA Placa_Arduino DEBERÁ incluir headers Content-Type: application/json
3. CUANDO el backend responde con código 200, LA Placa_Arduino DEBERÁ considerar la transmisión exitosa
4. SI el backend responde con error (4xx o 5xx), LA Placa_Arduino DEBERÁ reintentar el envío hasta 3 veces con intervalos de 1 segundo
5. SI todos los reintentos fallan, LA Placa_Arduino DEBERÁ registrar el error localmente y continuar con las siguientes detecciones

### Requerimiento 4: Indicadores Visuales

**Historia de Usuario:** Como técnico de mantenimiento, quiero ver el estado de funcionamiento de cada placa Arduino mediante indicadores LED, para poder diagnosticar problemas rápidamente sin herramientas adicionales.

#### Criterios de Aceptación

1. CUANDO la placa está encendida pero sin conexión WiFi, EL LED_Estado DEBERÁ parpadear en rojo cada segundo
2. CUANDO la placa está conectada a WiFi pero sin comunicación con el backend, EL LED_Estado DEBERÁ parpadear en amarillo cada 2 segundos
3. CUANDO la placa está completamente operativa, EL LED_Estado DEBERÁ mostrar luz verde fija
4. CUANDO se detecta un objeto, EL LED_Estado DEBERÁ hacer un destello azul breve (200ms) manteniendo el color de estado base
5. CUANDO ocurre un error crítico, EL LED_Estado DEBERÁ alternar entre rojo y apagado cada 500ms

### Requerimiento 5: Configuración de Hardware

**Historia de Usuario:** Como instalador del sistema, quiero una configuración de hardware estandarizada y documentada, para poder instalar y mantener múltiples puntos de medición de forma consistente.

#### Criterios de Aceptación

1. CUANDO se instala una nueva placa, EL Sistema_Radar DEBERÁ funcionar con sensores ultrasónicos HC-SR04 o compatibles
2. CUANDO se conectan los sensores, LA Placa_Arduino DEBERÁ usar pines digitales estándar (Trigger: pin 2, Echo: pin 3)
3. CUANDO se instala el LED de estado, LA Placa_Arduino DEBERÁ usar un LED RGB conectado a los pines 9, 10 y 11
4. CUANDO se alimenta la placa, EL Sistema_Radar DEBERÁ funcionar con alimentación de 5V mediante adaptador externo o USB
5. DONDE se requiera instalación exterior, LA Placa_Arduino DEBERÁ funcionar en un rango de temperatura de -10°C a +50°C

### Requerimiento 6: Gestión de Errores

**Historia de Usuario:** Como administrador del sistema, quiero que las placas Arduino manejen errores de forma robusta, para que el sistema continúe funcionando incluso ante fallos temporales de red o hardware.

#### Criterios de Aceptación

1. CUANDO falla la conexión WiFi durante el funcionamiento, LA Placa_Arduino DEBERÁ continuar detectando objetos y almacenar hasta 50 mediciones en memoria local
2. CUANDO se restablece la conexión, LA Placa_Arduino DEBERÁ enviar todas las mediciones almacenadas en orden cronológico
3. SI la memoria local se llena, LA Placa_Arduino DEBERÁ descartar las mediciones más antiguas para hacer espacio a las nuevas
4. CUANDO el sensor ultrasónico falla o da lecturas inconsistentes, LA Placa_Arduino DEBERÁ reiniciar el sensor automáticamente
5. SI el reinicio del sensor falla 3 veces consecutivas, LA Placa_Arduino DEBERÁ activar el modo de error crítico y notificar mediante LED

### Requerimiento 7: Configuración Remota

**Historia de Usuario:** Como operador del sistema, quiero poder ajustar parámetros de los sensores remotamente, para optimizar la detección según las condiciones específicas de cada ubicación.

#### Criterios de Aceptación

1. CUANDO se accede a la IP de la placa Arduino, EL Sistema_Radar DEBERÁ mostrar una página web de configuración
2. CUANDO se modifica la distancia de detección, LA Placa_Arduino DEBERÁ aplicar el nuevo valor inmediatamente sin reinicio
3. CUANDO se cambia la sensibilidad del sensor, LA Placa_Arduino DEBERÁ validar que el valor esté en el rango permitido (10-400 cm)
4. CUANDO se actualiza la configuración, LA Placa_Arduino DEBERÁ guardar los cambios en memoria no volátil
5. DONDE se requiera mantenimiento, LA Placa_Arduino DEBERÁ proporcionar información de diagnóstico incluyendo tiempo de funcionamiento y número de detecciones

### Requerimiento 8: Sincronización Temporal

**Historia de Usuario:** Como analista de datos, quiero que las mediciones tengan marcas de tiempo precisas, para poder correlacionar correctamente las detecciones de ambos sensores en el cálculo de velocidad.

#### Criterios de Aceptación

1. CUANDO se inicia la placa Arduino, EL Sistema_Radar DEBERÁ sincronizar su reloj interno con un servidor NTP
2. CUANDO se detecta un objeto, LA Placa_Arduino DEBERÁ incluir una marca de tiempo precisa en milisegundos en la petición HTTP
3. CUANDO la sincronización NTP falla, LA Placa_Arduino DEBERÁ usar su reloj interno y marcar las mediciones como "no sincronizadas"
4. CUANDO se restablece la conexión NTP, LA Placa_Arduino DEBERÁ resincronizar automáticamente su reloj
5. MIENTRAS funciona sin sincronización NTP, LA Placa_Arduino DEBERÁ mantener la precisión relativa entre mediciones con una deriva máxima de 1 segundo por hora