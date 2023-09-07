# Main File
# Changed

import time, update, machine

global led = machine.Pin(2, machine.Pin.OUT)
global power = machine.Pin(4, machine.Pin.OUT)
global nextupdate = time.time()+60;
global nextpower = time.time()+4;
global nextled = time.time()+1;
global ledvalue=0;
global powervalue=0;


def main():
    if time.time() > nextupdate:
        update.update_file()
        nextupdate=time.time()+60
    if time.time() > nextpwer:
        power.value(powervalue);
        powervalue=0**powervalue
        nextpower=time.time()+1
    if time.time() > nextled:
        led.value(ledvalue)
        ledvalue=0**ledvalue
        nextled=time.time()+4

    
def loop():
    while 1:
        main()
