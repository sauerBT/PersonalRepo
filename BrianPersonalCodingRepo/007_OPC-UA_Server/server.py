from opcua import Server
from random import randint
import serial
import time
import datetime

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        if ch=='\r' or ch=='' or ch=='\n':
            return rv
        rv += ch
        

server = Server()

url = "opc.tcp://192.168.1.125:4840"
server.set_endpoint(url)

name = "OPCUA_IMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
Interv = Param.add_variable(addspace, "Interval", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Press.set_writable()
Interv.set_writable()
Time.set_writable()

Pressure = 0
Temperature = 0
interval = 0

server.start()
print("Server started at {}".format(url))


port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)


while True:
    #port.write("\r\nSay something:")
    rcv = readlineCR(port)
    [Pressure, Temperature, interval] = rcv.split()
    #port.write("\r\nYou sent:" + repr(rcv))

    #Temperature = randint(10,50)
    #Pressure = randint(200, 999)
    TIME = datetime.datetime.now()

    print(Temperature, Pressure, interval, TIME)

    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Interv.set_value(interval)
    Time.set_value(TIME)

    time.sleep(2)


