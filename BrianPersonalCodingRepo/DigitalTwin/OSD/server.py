from paho.mqtt import client as mqtt_client
from random import randint
from logging import info,error
from time import sleep

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt/#"
client_id = f'python-mqtt-{randint(0,1000)}'
# username = ...
# password = ...
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)

    # client.username_pw_set(username, password)
    client.on_connect = on_connect

    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60

    def on_disconnect(client, userdata, rc):
        info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            info("Reconnecting in %d seconds...", reconnect_delay)
            sleep(reconnect_delay)

            try:
                client.reconnect()
                info("Reconnected successfully!")
                return
            except Exception as err:
                error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

        client.on_disconnect = on_disconnect

    return client

def publish(client):
    msg_count = 1
    while True:
        sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.connect(broker, port)
    client.loop_forever()


if __name__ == '__main__':
    run()
    while True:
        sleep(1)
        print("another scan")


