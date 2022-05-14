from opcua import Server
from random import randint
import time
import datetime
        
server = Server()

url = "opc.tcp://192.168.1.125:4840"
server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Temp = Param.add_variable(addspace, "Counter", 0)
Press = Param.add_variable(addspace, "RandomNumber", 0)
Interv = Param.add_variable(addspace, "Interval", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Press.set_writable()
Interv.set_writable()
Time.set_writable()

Counter = 0
RandomNumber = 0
interval = 0

server.start()
print("Server started at {}".format(url))

while True:
    Counter = Counter + 1
    RandomNumber = randint(200, 999)
    TIME = datetime.datetime.now()

    print(Counter, RandomNumber, interval, TIME)

    Temp.set_value(float(Counter))
    Press.set_value(float(RandomNumber))
    Interv.set_value(float(interval))
    Time.set_value(TIME)

    time.sleep(.1)


