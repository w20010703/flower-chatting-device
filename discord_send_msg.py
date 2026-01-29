import discord

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time
import json
import logging
import time

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


print("Connecting to AWS IoT...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")








# Create an instance of the Client
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content == "close":
        mqtt_connection.publish(topic=PUB_TOPIC, payload=json.dumps({"message": "9"}), qos=mqtt.QoS.AT_LEAST_ONCE)
    else:
        # Print message content
        print(f'{message.author} said: {message.content}')
        mqtt_connection.publish(topic=PUB_TOPIC, payload=json.dumps({"message": "10"}), qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(10)
        mqtt_connection.publish(topic=PUB_TOPIC, payload=json.dumps({"message": "9"}), qos=mqtt.QoS.AT_LEAST_ONCE)

    # Optional: reply to the user
    if message.content.lower() == 'hello':
        await message.channel.send(f'Hi {message.author.name}!')

# Run the bot with your token
client.run('REDACTED_DISCORD_TOKEN')











































