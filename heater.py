# Main File
# Changed

import time, update, machine

power = machine.Pin(2, machine.Pin.OUT)

while 1:
    power.value(1)
    time.sleep(5)
    power.value(0)
    time.sleep(5)

    update.update_file()