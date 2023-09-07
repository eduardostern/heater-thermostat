# upython-update-file eduardostern
# Heater Controller uPython

import time, update, machine

led = machine.Pin(4, machine.Pin.OUT)
power = machine.Pin(2, machine.Pin.OUT)
nextupdate = time.time()+60
nextpower = time.time()+4
nextled = time.time()+1
ledvalue=0
powervalue=0


def main():
    global nextupdate
    global nextpower
    global nextled
    global powervalue
    global ledvalue
    
    if time.time() >= nextupdate:
        update.update_file()
        nextupdate=time.time()+60
    if time.time() >= nextpower:
        power.value(powervalue)
        powervalue=0**powervalue
        nextpower=time.time()+1
    if time.time() >= nextled:
        led.value(ledvalue)
        ledvalue=0**ledvalue
        nextled=time.time()+4

    
def loop():
    while 1:
        main()
