# upython-update-file eduardostern
# Heater Controller uPython

import time, update, machine, onewire, ds18x20, ubinascii
from umqtt.simple import MQTTClient





def sub_cb(topic, msg):
    print((topic.decode(), msg.decode()))

def main():

    led = machine.Pin(2, machine.Pin.OUT)
    power = machine.Pin(4, machine.Pin.OUT)
    nextupdate = time.time()+60
    nextread = time.time()
    nextled = time.time()

    running=0
    pool_setpoint=30
    heater_mode=0


    ds_pin = machine.Pin(0)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    current_temp = ds_sensor.read_temp(roms[0])

    MQTT_BROKER = "mqtt.safetoken.net"
    CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode()

    print("Client ID:", CLIENT_ID)    

    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.connect()
    mqttClient.set_callback(sub_cb)
    mqttClient.subscribe('cmnd/'+CLIENT_ID+'/#')


    while 1:
            
        mqttClient.check_msg()

        
        if time.time() >= nextupdate:
            update.update_file()
            nextupdate=time.time()+60
            
        if time.time() >= nextread:
            
            current_time = time.time()
            message = '{"utc":'+str(current_time)+', "mode":'+str(heater_mode)+', "current_temp":'+str(current_temp)+', "pool_setpoint":'+str(pool_setpoint)+', "running": 0}'
            
            mqttClient.publish('/tele/'+CLIENT_ID+'/RESULT', str(message).encode())
            print(message)
            
            nextread=time.time()+30
            
        if time.time() >= nextled:
            led.value(0)
            ds_sensor.convert_temp()
            current_temp = ds_sensor.read_temp(roms[0])
            mqttClient.ping()
            led.value(1)
            nextled=time.time()+1

    
