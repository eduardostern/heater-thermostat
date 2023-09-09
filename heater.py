# upython-update-file eduardostern
# Heater Controller uPython

import utime, update, machine, onewire, ds18x20, ubinascii, ntptime, json, network
from umqtt.simple import MQTTClient
#import config


nextpublish = utime.time()
nextled = utime.time()


led = machine.Pin(2, machine.Pin.OUT)
power = machine.Pin(4, machine.Pin.OUT)


def sub_cb(topic, msg):
    
    global pool_setpoint
    global pool_histeresis
    global heater_mode
    global nextpublish
    global nextled

    print(topic.decode(), msg.decode())
    if topic.decode().split('/')[2].lower() == 'restart':
        machine.reset()
    if topic.decode().split('/')[2].lower() == 'reset':
        machine.reset()
        
    
    if topic.decode().split('/')[2] == 'Br':
        print('Berry Emulation persist object')
        p_var = msg.decode().split(';')[0].split('=')[0].lower()
        try:
            p_value = msg.decode().split(';')[0].split('=')[1]
        except:
            p_value=''

        print(p_var, p_value)
        
        if p_var == 'restart':
            machine.reset()
        if p_var == 'reset':
            machine.reset()

        if p_var == 'persist.heater_mode':
            heater_mode=int(p_value)
            write_persist()
            nextled = utime.time()
            nextpublish = utime.time()
        
        if p_var == 'persist.pool_histeresis':
            pool_histeresis=float(p_value)
            write_persist()
            nextled = utime.time()
            nextpublish = utime.time()
            
        
        if p_var == 'persist.pool_setpoint':
            ntc_setpoint=int(p_value)
            pool_setpoint=float(p_value)
            
            if ntc_setpoint == 14355:
                pool_setpoint=29.0
            if ntc_setpoint == 14496:
                pool_setpoint=29.5
            if ntc_setpoint == 14637:
                pool_setpoint=30.0
            if ntc_setpoint == 14777:
                pool_setpoint=30.5
            if ntc_setpoint == 14917:
                pool_setpoint=31.0
            if ntc_setpoint == 15055:
                pool_setpoint=31.5
            if ntc_setpoint == 15192:
                pool_setpoint=32.0
            if ntc_setpoint == 15328:
                pool_setpoint=32.5
            if ntc_setpoint == 15462:
                pool_setpoint=33.0
                
            write_persist()
            
            nextled = utime.time()
            nextpublish = utime.time()
            
    
def read_persist():
    global pool_setpoint
    global pool_histeresis
    global heater_mode

    try:
        f = open('_persist.json', 'r')
        contents=f.read()
        f.close()
        js=json.loads(contents)
        print(js)
        pool_setpoint=js["pool_setpoint"]
        pool_histeresis=js["pool_histeresis"]
        heater_mode=js["heater_mode"]
        js=""
        
    except:
        print('Unable to load _persist.json. Loading Defaults')
        pool_setpoint=30.0
        pool_histeresis=1.0
        heater_mode=0

    
def write_persist():
    global pool_setpoint
    global pool_histeresis
    global heater_mode

    try:
        
        contents= {"pool_setpoint":pool_setpoint, "pool_histeresis":pool_histeresis, "heater_mode":heater_mode}
        f = open('_persist.json', 'w')
        f.write(json.dumps(contents))
        f.close()
        print(contents)
        contents=""
        
    except:
        print('Unable to write _persist.json.')
       

def main():
    ntptime.settime()
    
    #print(config.config)

  
    global pool_setpoint
    global pool_histeresis
    global heater_mode
    global nextpublish
    global pool_histeresis
    global nextled
    
    
    read_persist()



    global led
    global power
    
    nextupdate = utime.time()+3600
    nextled = utime.time()
    nextpublish = utime.time()

    running=0
    power.value(running)

    ds_pin = machine.Pin(0)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    current_temp = ds_sensor.read_temp(roms[0])
    current_temp = round(current_temp,2)


    MQTT_BROKER = "mqtt.safetoken.net"
    #CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode()
    CLIENT_ID = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac')).decode().upper()    
     

    print("Client ID:", CLIENT_ID)    

    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.connect()
    mqttClient.set_callback(sub_cb)
    mqttClient.subscribe('cmnd/{:s}/#'.format(CLIENT_ID))


    while 1:
            
        mqttClient.check_msg()

        
        if utime.time() >= nextupdate:
            ntptime.settime()
            update.update_file()
            nextupdate=utime.time()+3600
            nextled=utime.time()
            nextpublish=utime.time()
            
        
        if utime.time() >= nextled:
            led.value(running)
            ds_sensor.convert_temp()
            current_temp = ds_sensor.read_temp(roms[0])
            current_temp = round(current_temp,2)
            mqttClient.ping()
            led.value(0**running)
            
            lastrunning=running;
            if current_temp < (pool_setpoint-pool_histeresis):
                running=1
            if current_temp >= pool_setpoint:
                running=0
            
            if heater_mode==0:
                running=0
            
            
            if lastrunning != running:
                power.value(running)
                nextpublish=utime.time()
                
            nextled=utime.time()+1
        
        
        if utime.time() >= nextpublish:
            
            current_time = 946684800 + utime.time()
            #message = '{"utc":'+str(current_time)+', "mode":'+str(heater_mode)+', "current_temp":'+str(current_temp)+', "pool_setpoint":'+str(pool_setpoint)+', "running": '+str(running)+'}'

            message = json.dumps({"utc":str(current_time), "mode":str(heater_mode), "current_temp":str(current_temp), "pool_setpoint":str(pool_setpoint), "running":str(running)}) 
            #topic='tele/'+CLIENT_ID+'/RESULT'
            topic='tele/{:s}/RESULT'.format(CLIENT_ID)
            mqttClient.publish(topic, str(message).encode())
            print(message, topic)
            
            nextpublish=utime.time()+30
            
        

    



