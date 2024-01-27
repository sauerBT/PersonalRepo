# Replace these variables with your own values
from jira_request import get_jira_project_issues, generate_jira_url, iter_dict, iter_list
import dictionary_funcs as df
jira_url = "https://control-associates.atlassian.net"
project_key = "BP"
username = "bsauerborn@control-associates.com"
password_or_api_token = "ATATT3xFfGF0Ehtj-S9-TJGq_Fesxa9O6papkXqK0Ay8cqIFWRrikS7rThC6XF099HFq8ZChee-ADT6WpOxmY0r-3o5ZPZccj0yL22vdsg63zjM_891cO6eJt2K9jggeCacfP_Vs1hSKh0zIIEQT9DTQ4lYGfiYcrvXU2mkeOww0bSWXQJZwHUU=3731FEC8" # "ATATT3xFfGF0rV8vMjTWh3UqKvbXw3uHVfcKleNp8N7O5h6D5k51jI16sEvujZkkl3M5gfmba-fvCrixImyhjsS_ChMZdbyYKmdmAc8A722TdQNr62GiiGgTLMg6AGTARhg_oRp88aRCMwx1TQ-UdS5hq4355R0zDcBC9rSNgSX7uZocbfgTvEA=9EC2BB84"

# JQL (Jira Query Language) to filter issues by project
jql = f"project={project_key}"

# Function to get Jira issues in a project

from paho.mqtt import client as mqtt_client
from paho import mqtt
from random import randint
from logging import info,error
from time import sleep

broker = "27b6c7523fba4a3b8ffc1962b8090a7a.s1.eu.hivemq.cloud"
port = 8883
topic = "python/mqtt/#"
client_id = f'python-mqtt-{randint(0,1000)}'
username_mqtt = "admin"
password_mqtt = "DeltaVE1"
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # enable TLS
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    if username != "":
        client.username_pw_set(username_mqtt, password_mqtt)
    client.on_connect = on_connect
    client.connect(broker, port)

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
    old_dict = {}
    while True:
        sleep(20)
        print("New Transmission")
        new_dict = iter_dict(get_jira_project_issues(username, password_or_api_token, jql, generate_jira_url(jira_url)))
        temp_dict = df.dictionary_compare(new_dict,old_dict)
        old_dict = new_dict
        for key in iter(temp_dict):
            topic = "jira/MBPR/" + key
            result = client.publish(topic, temp_dict[key])

            msg = f"messages: {msg_count}"
            result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}` with value '{temp_dict[key]}'")
            else:
                print(f"Failed to send message to topic {topic} with value '{temp_dict[key]}'")
            msg_count += 1
            if msg_count > 1000000:
                break

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    
# Main script
def main():
    run()
                
if __name__ == "__main__":
    main()
