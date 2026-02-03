from machine import Pin
import time
import micropython
import network
import ujson
import urequests
import ntptime

url_servicio="https://postman-echo.com/post"
micropython.alloc_emergency_exception_buf(100) #habilito las interrupciones
UNIX_OFFSET = 946684800

def motion_handler(pin):
    datos={
        "detector1": epoch_unix_float()
    }
    print(epoch_unix_float())
    response = urequests.post(
        url_servicio,
        data=ujson.dumps(datos),
        headers={"Content-Type": "application/json"}
    )
    response.close()
    print(epoch_unix_float())
    
print("Conectando a la wifi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
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


green_pin_led = 14  # Cambia esto al número de pin que estás utilizando
red_pin_led = 27
motion_pin = 12
sensor_pin = Pin (motion_pin, Pin.IN, Pin.PULL_UP)
sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=motion_handler)
green_led = Pin(green_pin_led, Pin.OUT)
red_led = Pin(red_pin_led, Pin.OUT)

while True:
    green_led.value(1)
    red_led.value(0)  # Encender el LED
    time.sleep(1)  # Esperar 1 segundo
    green_led.value(0)
    red_led.value(1)  # Apagar el LED
    time.sleep(1)  # Esperar 1 segundo
