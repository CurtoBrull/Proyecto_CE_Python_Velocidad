#--------DETECTOR 1----------------------
from machine import Pin
import time
import network
import ujson
import urequests
import ntptime

url_servicio="https://radarpythonapi.onrender.com/mediciones/"
UNIX_OFFSET = 946684800

print("Conectando a la wifi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Conectada!")

ntptime.settime()

epoch_base = time.time() + UNIX_OFFSET
ticks_base = time.ticks_ms()

def epoch_unix_ms():
    """Timestamp Unix en milisegundos (entero, sin pérdida de precisión)."""
    return (epoch_base * 1000) + time.ticks_diff(time.ticks_ms(), ticks_base)


# ---------------- SENSOR ----------------
motion_pin = 12
sensor = Pin(motion_pin, Pin.IN)   # SIN PULL_UP

COOLDOWN_MS = 4000      # tiempo mínimo entre eventos
CONFIRM_MS = 50         # validación anti-ruido

last_event = 0
armed = True
# ---------------------------------------

while True:
    val = sensor.value()

    # Detección
    if val == 1 and armed:
        time.sleep_ms(CONFIRM_MS)
        if sensor.value() == 1:
            now = time.ticks_ms()
            if time.ticks_diff(now, last_event) > COOLDOWN_MS:
                last_event = now
                armed = False

                datos = {"detector1": epoch_unix_ms()}
                print("Medición válida:", datos["detector1"])

                try:
                    r = urequests.post(
                        url_servicio,
                        data=ujson.dumps(datos),
                        headers={"Content-Type": "application/json"}
                    )
                    r.close()
                except Exception as e:
                    print("Error enviando:", e)

    # Rearme cuando el sensor vuelve a reposo
    if val == 0:
        armed = True

    time.sleep_ms(20)