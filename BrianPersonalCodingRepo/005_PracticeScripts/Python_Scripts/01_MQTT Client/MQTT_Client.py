# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import requests
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code= ",rc)
        client.bad_connection_flag=True
def on_disconnect(client, userdata, rc):
    logging.info("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True
mqtt.Client.connected_flag=False
mqtt.Client.bad_connection_flag=False
mqtt.Client.disconnect_flag=True

client = mqtt.Client('PythonMQTT1') #create new instance 
broker = '192.168.1.112'
port = 1883

client.on_connect = on_connect #bind call back function
client.loop_start()  #Start loop 
print("Connecting to broker ",broker)
try:
    client.connect(broker, port) #connect to broker
except:
    print('connection failed')
    exit(1) #Should quit or raise flag to quit or retry
print(client.bad_connection_flag)
print(client.disconnect_flag)
print(client.connected_flag)
while not client.connected_flag and not client.bad_connection_flag: #wait in loop
    print('In wait loop')
    time.sleep(1)
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    print('Loop stopped due to bad connection')
    #sys.exit()   
print('In main loop')

client.loop_stop()    #Stop loop 
print('Loop stopped')
client.disconnect() # disconnect
print('MQTT client disconnected')

#payload = {'pan':'120','tilt':'111'}
#r = requests.post('http://192.168.1.109/pantilt', json=payload)



