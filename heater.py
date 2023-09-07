# Main File
# Changed

import time, update, machine

led = machine.Pin(2, machine.Pin.OUT)
power = machine.Pin(0, machine.Pin.OUT)


def main():
    led.value(1)
    power.value(0)
    time.sleep(1)
    led.value(0)
    time.sleep(1)

    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)

    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)

    power.value(1)

    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)

    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)

    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)


    update.update_file()

def loop():
    while 1:
        main()

try:
    loop()
except:
    machine.reset()
    