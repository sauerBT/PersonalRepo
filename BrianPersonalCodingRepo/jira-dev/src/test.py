import psutil
import platform
import socket
import json
import time
import paho.mqtt.client as mqtt
import jira_request as jr

# MQTT broker details
mqtt_broker = '10.10.2.75'
mqtt_port = 1883
mqtt_username = 'YOUR_MQTT_USERNAME'
mqtt_password = 'YOUR_MQTT_PASSWORD'
mqtt_topic = 'diagnostics/me'

def get_system_info():
    # Get basic system information
    system_info = {
        'hostname': socket.gethostname(),
        'system': platform.system(),
        'platform': platform.platform(),
        'architecture': platform.architecture(),
        'processor': platform.processor(),
    }
    return system_info

def get_cpu_usage():
    # Get CPU usage information
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_info = {'cpu_percent': cpu_percent}
    return cpu_info

def get_memory_usage():
    # Get memory usage information
    memory = psutil.virtual_memory()
    memory_info = {
        'total_memory': memory.total,
        'used_memory': memory.used,
        'free_memory': memory.free,
        'percent_memory_used': memory.percent,
    }
    return memory_info

def get_network_info():
    # Get network interface information
    network_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        network_info[interface] = [addr.address for addr in addrs]

    return network_info

def publish_to_mqtt(data):
    # Publish data to MQTT broker
    client = mqtt.Client()
    #client.username_pw_set(username=mqtt_username, password=mqtt_password)
    client.connect(mqtt_broker, mqtt_port, 60)

    payload = json.dumps(data)
    client.publish(mqtt_topic, payload)
    print("done")
    client.disconnect()

if __name__ == '__main__':
    try:
        while True:
            # Collect system information
            system_info = get_system_info()

            # Collect CPU usage information
            cpu_info = get_cpu_usage()

            # Collect memory usage information
            memory_info = get_memory_usage()

            # Collect network information
            network_info = get_network_info()

            # Combine all information into a single dictionary
            diagnostics_data = {
                'system_info': system_info,
                'cpu_info': cpu_info,
                'memory_info': memory_info,
                'network_info': network_info,
            }
            print(jr.iter_dict(diagnostics_data))
            # Publish data to MQTT broker
            publish_to_mqtt(diagnostics_data)

            # Wait for the next iteration
            time.sleep(60)  # Adjust the sleep duration as needed

    except KeyboardInterrupt:
        print("Script terminated by user.")