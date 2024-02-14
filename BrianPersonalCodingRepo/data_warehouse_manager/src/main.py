import json
import psycopg2
import paho.mqtt.client as mqtt

# TimescaleDB connection details
DB_HOST = "usnutsdb1"
DB_PORT = "5432"
DB_NAME = "iot_data"
DB_USER = "postgres"
DB_PASSWORD = "DeltaVE1"

# MQTT broker details
MQTT_BROKER_HOST = "192.168.1.99"
MQTT_BROKER_PORT = 1883  # Change if using a different port
MQTT_TOPIC = "sauerborn/330_chestnut_st_nutley_nj/+/+/Edge/+/#"  # Change to your MQTT topic


def insert_data_to_db(connection, cursor, payload):
    try:
        data = json.loads(payload)
        for metric in data["metrics"]:
            value = metric["value"]
            timestamp = metric["timestamp"]
            metric_name = metric["name"]
            # Parse metric name to extract device and metric
            instrument_id, reading_type = metric_name.split("/")
            cursor.execute("""
                INSERT INTO sensor_data (sensor_value, timestamp, instrument_id, reading_type)
                VALUES (%s, %s, %s, %s)
            """, (value, timestamp, instrument_id, reading_type))
        connection.commit()
        print("Message Transmission Success")
    except Exception as e:
        print(f"Error inserting data into database: {e}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"new message {msg.payload}")
    insert_data_to_db(userdata["connection"], userdata["cursor"], payload)


def main():
    # Connect to TimescaleDB
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Set up MQTT client
    mqtt_client = mqtt.Client(userdata={"connection": conn, "cursor": cursor})
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    mqtt_client.subscribe(MQTT_TOPIC)

    # Start the MQTT loop
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
