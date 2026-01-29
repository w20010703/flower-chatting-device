from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time
import json
import logging

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2jx2mgo671gkv-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "./AWS_KEY/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "./AWS_KEY/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./AWS_KEY/root.pem"
MESSAGE = "Hello World"
PUB_TOPIC = "esp32/sub"
SUB_TOPIC = "esp32/pub"
RANGE = 20

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )








# publish

# print("Connecting to {} with client ID '{}'...".format(
#         ENDPOINT, CLIENT_ID))
# connect_future = mqtt_connection.connect()
# connect_future.result()
# print("Connected!")
# print('Begin Publish')

# mqtt_connection.publish(topic=PUB_TOPIC, payload=json.dumps({"message": "180"}), qos=mqtt.QoS.AT_LEAST_ONCE)
# t.sleep(5)
# mqtt_connection.publish(topic=PUB_TOPIC, payload=json.dumps({"message": "0"}), qos=mqtt.QoS.AT_LEAST_ONCE)













# subscribe

# -------- Connect --------
print("Connecting to AWS IoT...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

# -------- Define Callback Function --------
def on_message_received(topic, payload, **kwargs):
    print(f"\nMessage received on topic '{topic}':")
    print(payload.decode('utf-8'))

# -------- Subscribe --------
print(f"Subscribing to topic '{SUB_TOPIC}'...")
subscribe_future, _ = mqtt_connection.subscribe(
    topic=SUB_TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)
subscribe_future.result()
print(f"Successfully subscribed to {SUB_TOPIC}")

# -------- Keep the connection alive --------
try:
    print("\nListening for messages (press Ctrl+C to exit)...")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nDisconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")









