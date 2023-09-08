# upython-update-file eduardostern
# Heater Controller uPython

import utime, update, machine, onewire, ds18x20, ubinascii, ntptime
from umqtt.simple import MQTTClient


pool_setpoint=30.0
pool_histeresis=1.0
heater_mode=0
nextpublish = utime.time()
nextled = utime.time()


def sub_cb(topic, msg):
    
    global pool_setpoint
    global heater_mode
    global nextpublish
    global nextled

    print(topic.decode(), msg.decode())
    mqtt_topic = topic.decode()
    mqtt_msg = msg.decode()
    mqtt_cmd = mqtt_topic.split('/')[2]
    if mqtt_cmd == 'Br':
        print('Berry Emulation persist object')
        br_cmd = mqtt_msg.split(';')[0]
        persist=br_cmd
        p_var = persist.split('=')[0]
        p_value = persist.split('=')[1]
        
        print(p_var, p_value)
        
        if p_var == 'persist.heater_mode':
            heater_mode=int(p_value)
            nextled = utime.time()
            nextpublish = utime.time()
        
        if p_var == 'persist.pool_setpoint':
            pool_setpoint=float(p_value)
            nextled = utime.time()
            nextpublish = utime.time()
            
    

def main():
    ntptime.settime()

  
    global pool_setpoint
    global heater_mode
    global nextpublish
    global pool_histeresis
    global nextled
    

    led = machine.Pin(2, machine.Pin.OUT)
    power = machine.Pin(4, machine.Pin.OUT)
    nextupdate = utime.time()+60
    nextled = utime.time()
    nextpublish = utime.time()

    running=0
  

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

        
        if utime.time() >= nextupdate:
            update.update_file()
            nextupdate=utime.time()+60
            
        
        if utime.time() >= nextled:
            led.value(0)
            ds_sensor.convert_temp()
            current_temp = ds_sensor.read_temp(roms[0])
            mqttClient.ping()
            led.value(1)
            
            if current_temp < (pool_setpoint-pool_histeresis):
                running=1
            if current_temp >= pool_setpoint:
                running=0
            
            if heater_mode==0:
                running=0
                
            power.value(running)
            
            nextled=utime.time()+1
        
        
        if utime.time() >= nextpublish:
            
            current_time = 946684800 + utime.time()
            message = '{"utc":'+str(current_time)+', "mode":'+str(heater_mode)+', "current_temp":'+str(current_temp)+', "pool_setpoint":'+str(pool_setpoint)+', "running": '+str(running)+'}'
            topic='tele/'+CLIENT_ID+'/RESULT'
            
            mqttClient.publish(topic, str(message).encode())
            print(message, topic)
            
            nextpublish=utime.time()+30
            
        

    
