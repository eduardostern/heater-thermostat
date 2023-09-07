# upython-update-file eduardostern
# Heater Controller uPython

import time, update, machine, onewire, ds18x20

led = machine.Pin(2, machine.Pin.OUT)
power = machine.Pin(4, machine.Pin.OUT)
nextupdate = time.time()+60
nextread = time.time()
nextled = time.time()

ledvalue=0


ds_pin = machine.Pin(0)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()



def main():
    global nextupdate
    global nextread
    global nextled
    global powervalue
    global ledvalue
    
    if time.time() >= nextupdate:
        update.update_file()
        nextupdate=time.time()+60
    if time.time() >= nextread:
        ds_sensor.convert_temp()
        print(ds_sensor.read_temp(roms[0]))
        nextread=time.time()+30
    if time.time() >= nextled:
        led.value(ledvalue)
        ledvalue=0**ledvalue
        nextled=time.time()+1

    
def loop():
    while 1:
        main()
