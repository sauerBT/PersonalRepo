# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



def fileInitRead(filename):
    import csv
    with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            line_count = 0
            headerList = ['']*1000
            a = {}
            for row in csv_reader:
                numRows = len(row)
                if line_count == 0:
                    for j in range(numRows):
                        headerList[j] = row[j]
                        key = row[j]
                        a.setdefault(key, [])
                        
                    line_count += 1
                else:
                    for j in range(numRows):
                        a[headerList[j]].append(row[j])  
                    line_count += 1
            print(f'Processed {line_count} lines.')
            lineCountHold = line_count - 1
            publishTransmission = True
            return (a, headerList, lineCountHold, publishTransmission)
        
def fileOnChangeRead(a, headerList, filename, lineCountHold = 0, fileSizeInit = 0):  
    import csv, os
    
    fileSizeOld = fileSizeInit
    fileSizeNew = os.stat(filename).st_size
        
    if fileSizeNew > fileSizeOld:
        fileSizeOld = fileSizeNew
        print("File Changed")

        # Second time
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                    #print(row)
                if line_count > lineCountHold:
                    numRows = len(row)
                    for j in range(numRows):
                        a[headerList[j]].append(row[j])
                line_count += 1                           
            print(f'Processed {line_count} lines.')
            lineCountHold = line_count
            publishTransmission = True
    else:
        a = a
        lineCountHold = lineCountHold
        publishTransmission = False
    return (a, lineCountHold, fileSizeOld, publishTransmission)


"""
-------------------------------------------------------------------------------
Logic Starts Here
-------------------------------------------------------------------------------
"""        


import os, time  
   
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
client.publish_flag = False
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    client.publish_flag = True
    pass

client.on_publish = on_publish  
ret= client.publish("house/bulb1","on")  



path_to_watch = "C:\\Users\\brian\Desktop\Shared" 
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
sleepTime = 1
initializeFileRead = 0
try:
    while 1:
        time.sleep(sleepTime)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added: 
            
            print("Added: ", ", ".join (added))
            file = added[0]
            filename = path_to_watch + '\\' +  file
            fileSizeOld = os.stat(filename).st_size
            # First time
            [a, headerList, lineCountHold, publishTransmission] = fileInitRead(filename)
            initializeFileRead = 1
            if removed: print("Removed: ", ", ".join (removed))
            before = after
    
        if initializeFileRead != 0:
            if publishTransmission:
                for i in range(len(headerList)):
                    transmission = a[headerList[i]]
                    topic = "csvread/" + headerList[i]
                    for j in range(len(transmission)):
                        ret= client.publish(topic,transmission[j]) 
                        while 1:
                            if not client.publish_flag:
                                print('In publish loop')
                                time.sleep(1)
                            else:
                                break
                publishTransmission = False            
            [a, lineCountHold, fileSizeOld, publishTransmission] = fileOnChangeRead(a, headerList, filename, lineCountHold, fileSizeOld)
            
                
                    
except KeyboardInterrupt:
    client.loop_stop()    #Stop loop 
    print('Loop stopped')
    client.disconnect() # disconnect
    print('MQTT client disconnected')
    pass

