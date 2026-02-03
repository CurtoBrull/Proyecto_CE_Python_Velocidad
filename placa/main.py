from machine import Pin
import time
import micropython
import network
import ujson
import urequests
import ntptime

# ============ CONFIGURACIÓN ============
WIFI_SSID = 'Wokwi-GUEST' # TODO cambiar SSID
WIFI_PASSWORD = '' # TODO cambiar pass
API_URL = "http://192.168.1.100:8080/mediciones/"  # TODO Cambiar IP del servidor


# Pines
GREEN_LED_PIN = 14
RED_LED_PIN = 27
SENSOR_PIN = 12

# ============ INICIALIZACIÓN ============
micropython.alloc_emergency_exception_buf(100)
UNIX_OFFSET = 946684800

# Variables globales
ultima_deteccion = 0
DEBOUNCE_MS = 500  # Evitar detecciones múltiples

def epoch_unix_float():
    """Retorna timestamp Unix con precisión de milisegundos."""
    return epoch_base + time.ticks_diff(time.ticks_ms(), ticks_base) / 1000


def enviar_medicion(timestamp):
    """Envía el timestamp al servidor FastAPI."""
    datos = {"timestamp": timestamp}
    try:
        response = urequests.post(
            API_URL,
            data=ujson.dumps(datos),
            headers={"Content-Type": "application/json"}
        )
        resultado = response.json()
        response.close()

        # Mostrar resultado
        if "velocidad_kmh" in resultado and resultado["velocidad_kmh"]:
            print(f"Velocidad: {resultado['velocidad_kmh']} km/h")
            # Parpadear LED verde si velocidad OK, rojo si exceso
            if resultado["velocidad_kmh"] > 50:
                parpadear_led(red_led, 3)
            else:
                parpadear_led(green_led, 3)
        else:
            print(resultado.get("mensaje", "Sensor registrado"))

    except Exception as e:
        print(f"Error al enviar: {e}")
        parpadear_led(red_led, 5)


def motion_handler(pin):
    """Handler de interrupción del sensor de movimiento."""
    global ultima_deteccion

    ahora = time.ticks_ms()
    if time.ticks_diff(ahora, ultima_deteccion) < DEBOUNCE_MS:
        return  # Ignorar rebotes

    ultima_deteccion = ahora
    timestamp = epoch_unix_float()
    print(f"Sensor activado: {timestamp}")

    # Encolar envío (no hacer HTTP en interrupción)
    micropython.schedule(lambda _: enviar_medicion(timestamp), None)


def parpadear_led(led, veces):
    """Parpadea un LED n veces."""
    for _ in range(veces):
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        time.sleep(0.1)


def conectar_wifi():
    """Conecta a la red WiFi."""
    print("Conectando a WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

    intentos = 0
    while not sta_if.isconnected() and intentos < 50:
        print(".", end="")
        time.sleep(0.2)
        intentos += 1

    if sta_if.isconnected():
        print(f"\nConectado! IP: {sta_if.ifconfig()[0]}")
        return True
    else:
        print("\nError de conexión WiFi")
        return False


# ============ PROGRAMA PRINCIPAL ============
# Configurar LEDs
green_led = Pin(GREEN_LED_PIN, Pin.OUT)
red_led = Pin(RED_LED_PIN, Pin.OUT)

# Apagar LEDs
green_led.value(0)
red_led.value(0)

# Conectar WiFi
if conectar_wifi():
    # Sincronizar tiempo NTP
    try:
        ntptime.settime()
        print("Tiempo NTP sincronizado")
    except OSError as e:
        print(f"Error NTP ({e}), usando tiempo local")

    # Base de tiempo para timestamps precisos
    epoch_base = time.time() + UNIX_OFFSET
    ticks_base = time.ticks_ms()

    # Configurar sensor con interrupción
    sensor_pin = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)
    sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=motion_handler)

    print(f"Sistema listo. Enviando a: {API_URL}")
    green_led.value(1)  # LED verde = sistema OK

    # Loop principal - mantener vivo
    while True:
        time.sleep(1)
else:
    # Error WiFi - parpadear rojo
    while True:
        red_led.value(1)
        time.sleep(0.5)
        red_led.value(0)
        time.sleep(0.5)
