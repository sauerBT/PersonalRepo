from opcua import Client
import pandas as pd
import time, csv
import datetime
import timeit

url = "opc.tcp://192.168.1.46:4840"

csvOut = "C:\\Users\\bsauer\\Desktop\\pythonScripts\\data.csv" 
#create dataframe
column_names = pd.Series(['datetime','Counter','RandomNumber','interval','TIME'])
df_OPC_Client = pd.DataFrame(columns = column_names)

client = Client(url)

client.connect()
print("Client Connected")

i = 0
start = 0
while True:
    
    
    count = client.get_node("ns=2;i=2")
    Counter = count.get_value()
    #print(Counter)

    Rand = client.get_node("ns=2;i=3")
    RandomNumber = Rand.get_value()
    #print(RandomNumber)

    Interv = client.get_node("ns=2;i=4")
    interval = Interv.get_value()
    #print(interval)

    Time = client.get_node("ns=2;i=5")
    TIME = Time.get_value()
    #print(TIME)

    #Time_CV = TIME = datetime.datetime.now()
    #datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    #append row to the dataframe
    #new_row = {'datetime':Time_CV, 'Counter':Counter, 'RandomNumber':RandomNumber, 'interval':interval, 'TIME':TIME}
    #df_OPC_Client = df_OPC_Client.append(new_row, ignore_index=True)

    
    #if i == 1000:
    #    df_OPC_Client.to_csv(csvOut, index=False)
    #    i = 0
    #else:
    #    i = i + 1
        
    stop = timeit.default_timer()

    print('Time: ', stop - start) 
    start = timeit.default_timer()

    time.sleep(.001)


