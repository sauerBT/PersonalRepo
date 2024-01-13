import asyncio
import paho.mqtt.client as mqtt

# define MQTT broker and topics
broker_address = 'localhost'
broker_port = 1883
subscribe_topic = "ml/input"
publish_topic = "ml/output"

async def main():

    # Create an MQTT Client instance
    client = mqtt.Client()

    # Configure the MQTT client callbacks
    from mlcallbacks import on_connect, on_disconnect, on_message, on_publish
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Connect to the MQTT Broker
    client.connect(broker_address, broker_port)

    # Start the MQTT network loop
    client.loop_start()

    try:
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        client.loop_stop()
        await client.disconnect()

asyncio.run(main())