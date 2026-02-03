from machine import Pin
import time
import micropython
import network
import ujson
import urequests
import ntptime

url_servicio="https://radar-velocidad-api.onrender.com/mediciones/"
micropython.alloc_emergency_exception_buf(100) #habilito las interrupciones
UNIX_OFFSET = 946684800
motion_detected = False
last_trigger = 0
DEBOUNCE_MS = 1500

def motion_handler(pin):
    global motion_detected, last_trigger
    now = time.ticks_ms()
    if time.ticks_diff(now, last_trigger) > DEBOUNCE_MS:
        last_trigger = now
        motion_detected = True
    
print("Conectando a la wifi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Radar', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Conecteda!")

# NTP
ntptime.settime()

# Base de tiempo
epoch_base = time.time() + UNIX_OFFSET
ticks_base = time.ticks_ms()

def epoch_unix_float():
    return epoch_base + time.ticks_diff(time.ticks_ms(), ticks_base) / 1000


green_pin_led = 26  # Cambia esto al número de pin que estás utilizando
red_pin_led = 25
motion_pin = 27
sensor_pin = Pin (motion_pin, Pin.IN, Pin.PULL_UP)
sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=motion_handler)
green_led = Pin(green_pin_led, Pin.OUT)
red_led = Pin(red_pin_led, Pin.OUT)

while True:
    if motion_detected:
        motion_detected = False
        datos = {
            "timestamp": epoch_unix_float()
        }
        try:
            response = urequests.post(
                url_servicio,
                data=ujson.dumps(datos),
                headers={"Content-Type": "application/json"}
            )
            response.close()
            print("Medición enviada:", datos["detector1"])
        except Exception as e:
            print("Error enviando:", e)

    green_led.value(1)
    red_led.value(0)
    time.sleep(1)
    green_led.value(0)
    red_led.value(1)
    time.sleep(1)
