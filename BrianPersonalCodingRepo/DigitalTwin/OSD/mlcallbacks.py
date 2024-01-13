import blender_model as bm
import feeder_model as fm
from helper import listStrToFloat,parseMqttTopic,parseMqttPayload,createOuputTopic

BASE_TOPIC = "ml/models"
INPUT_KEYWORD = "input"
OUTPUT_KEYWORD = "output"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(f"{BASE_TOPIC}/#")
    client.publish(BASE_TOPIC + "/info/instructions", "Publish here as '<modelname>/input/...,...,...'")

def on_message(client, userdata, msg):
    # Call the machine learning function with the message payload
    parsedTopic = parseMqttTopic(msg.topic)
    if parsedTopic[3] == INPUT_KEYWORD:
        result = run_ml_model(parsedTopic[2],parseMqttPayload(msg.payload))
        # Publish the result to the output topic
        client.publish(createOuputTopic(parsedTopic, INPUT_KEYWORD, OUTPUT_KEYWORD), result)

def on_publish(client, userdata, mid):
    print("Published message")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

# Define the machine learning function
def run_ml_model(function, input_data):
    inputs = listStrToFloat(input_data)
    
    def filter_str(s1: str,s2: str):
        filter_iter = filter(lambda ch: ch not in s2,s1)
        def f(i, acc):
            s = next(i, None)
            if (s == None): return acc
            else: return(f(i, acc + s))
        return(f(filter_iter, ""))

    # Replace with function
    try:
        result = eval(filter_str(function + "(" + str(inputs) + ")","[]"))
        return result
    except:
        print(BASE_TOPIC + "/error","SyntaxError")
        pass
    