from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import discord
import asyncio
import threading
from concurrent.futures import CancelledError
import time
import random

import re

def find_emojis(s):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F900-\U0001F9FF"  # Supplemental
        u"\U00002600-\U000026FF"  # Misc symbols
        u"\U0001FA70-\U0001FAFF"  # Extended-A
        "]+", 
        flags=re.UNICODE
    )
    matches = emoji_pattern.findall(s)
    return matches if matches else None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Global list to store messages
fetched_messages = []

# Discord Bot Setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)

DISCORD_TOKEN = 'REDACTED_DISCORD_TOKEN'
CHANNEL_ID_Julia = 1275510960047784080
CHANNEL_ID_Chris = 748914683687469169

CHANNEL_ID = [CHANNEL_ID_Julia, CHANNEL_ID_Chris]


# Background task to fetch messages
async def discord_task():
    print("discord_task")
    await client.start(DISCORD_TOKEN)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    for _uid in CHANNEL_ID:
        user = await client.fetch_user(_uid)  # Fetch the user (not channel!)
        dm_channel = await user.create_dm()  # Create (or get) DM channel

        msgs = []
        async for message in dm_channel.history(limit=100):
            

            if message.attachments:
                for attachment in message.attachments:
                    print(f"Image URL: {attachment.url}")
                    msgs.append(f"img:idx/msg:{attachment.url}")
                    print(f"{message.author}: {attachment.url}")
            else:
                msgs.append(f"chatting:idx/msg:{message.content}")
                print(f"{message.author}: {message.content}")

        global fetched_messages
        fetched_messages.append(list(reversed(msgs)))
    
    await client.close()



# Start Discord client in background thread
def run_discord():
    print("run_discord")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(discord_task())

# -------- MQTT Subscribe Setup --------
def mqtt_subscribe():
    from awscrt import io, mqtt, auth, http
    from awsiot import mqtt_connection_builder
    import time
    import json
    import logging

    # Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
    ENDPOINT = "a2jx2mgo671gkv-ats.iot.us-east-2.amazonaws.com"
    CLIENT_ID = "testDevice"
    PATH_TO_CERTIFICATE = "../AWS_KEY/certificate.pem.crt"
    PATH_TO_PRIVATE_KEY = "../AWS_KEY/private.pem.key"
    PATH_TO_AMAZON_ROOT_CA_1 = "../AWS_KEY/root.pem"
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

    # Define the callback
    def on_message_received(topic, payload, **kwargs):
        message_text = payload.decode('utf-8')
        message_text = json.loads(message_text)
        message_text = message_text["message"]
        print(f"Received on '{topic}': {message_text}")

        if message_text == "flower" or message_text == "chris":
            asyncio.run(send_discord_dm())
        if message_text:
            if message_text == "julia":
                content = random.choice(fetched_messages[0])
            if message_text == "chris":
                content = random.choice(fetched_messages[1])
            msg = content.split(":idx/msg:")
            if msg[0] == "img":
                socketio.emit('server_response', {'data': '<div id="cover_msg"><img src="' + str(msg[1]) + '"></div>'})
            else:
                socketio.emit('server_response', {'data': str(msg[1])})

    # Subscribe
    print(f"Subscribing to '{SUB_TOPIC}'...")
    subscribe_future, _ = mqtt_connection.subscribe(
        topic=SUB_TOPIC,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )
    subscribe_future.result()
    print(f"Subscribed to {SUB_TOPIC}")

    # Keep running forever to listen for messages
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")

with app.app_context():
    # run_discord()
    threading.Thread(target=run_discord, daemon=True).start()
    threading.Thread(target=mqtt_subscribe, daemon=True).start()

async def send_discord_dm():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            user = await client.fetch_user(CHANNEL_ID_Julia)
            await user.send("💐 🪷 🌺 🌹 🌼")
            print("DM sent!")
        except Exception as e:
            print("Error sending DM:", e)
        await client.close()

    await client.start(DISCORD_TOKEN)

@app.route('/send', methods=['GET'])
def send():
    asyncio.run(send_discord_dm())  # Run the async DM sender
    return 'DM sent (if user ID and permissions are valid)'


# Flask route
@app.route('/')
def home():
    print("=======================home")
    print("fetched_messages: ", generate_content())
    scroll1 = generate_content()
    return render_template_string(html_template, scroll1=generate_content(), scroll2=generate_content(), scroll3=generate_content(), scroll4=generate_content())


def generate_content():
    final = ""

    holder2 = []
    _chatting = []
    _bigfont = []

    holder1 = ['<div class="word largefont holder1">??</div>', '<div class="word largefont holder1">!!</div>', '<div class="word largefont holder1">$$</div>', '<div class="word largefont holder1">@@</div>']

    emoji = []
    _fetched_messages = []

    for _fm in fetched_messages:
        _fetched_messages += _fm

    for content in _fetched_messages:
        msg = content.split(":idx/msg:")

        if msg[0] == "chatting":
            _emoji = find_emojis(msg[1])
            if not _emoji == None:
                for e in _emoji:
                    holder1.append('<div class="word emoji holder1">'+e+'</div>')
            print("len(msg[1]) < 20: ", len(msg[1]) < 20, msg[1])
            if len(msg[1]) < 20:
                if len(_bigfont) >= 2:
                    temp = '<div class="word bigfont holder2">'
                    for b in _bigfont:
                        temp += "<div>" + b + "</div>"
                    temp += "</div>"
                    holder2.append(temp)
                    _bigfont = []
                _bigfont.append(msg[1])

            if len(_chatting) >= 3:
                temp = '<div class="word chatting holder2">'
                for c in _chatting:
                    temp += "<div>" + c + "</div>"
                temp += "</div>"
                holder2.append(temp)
                _chatting = []
            _chatting.append(msg[1])

        elif msg[0] == "img":
            holder1.append('<div class="word holder1"><img src="' + msg[1] + '"></div>')

    while len(holder1) > 0 and len(holder2) > 0:
        random.shuffle(holder1)
        random.shuffle(holder2)
        _img = holder1.pop()
        _chatting = holder2.pop()
        final += '<div class="holder">' + _img + _chatting + '</div>'

    return final+final


# HTML template (embed your full html here)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Jersey+25&display=swap" rel="stylesheet">
  <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
  <title>Auto Scrolling Word Box</title>
  <style>
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background: #000;
      font-family: sans-serif;
      color: white;
      font-weight: 600;

      font-family: "Jersey 25", sans-serif;
      margin: 0;
      padding: 0;
    }

    .cover {
      position: absolute;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, .7);
      z-index: 1000;
      display: none;
      justify-content: center;
      align-items: center;
    }

    .coverbox {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      font-size: 40px;
      gap: 10px;
      width: 92vw;
      padding: 2vw;
    }

    #cover_msg {
      width: 92vw;
      height: 100vh;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    #cover_msg img {
      width: 100%;
      height: 100%;
      object-fit: cover;  /* Keeps aspect ratio, fills space */
    }

    .word-box {
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      display: flex;
      position: relative;
      margin: 0;
      padding: 0;
    }

    .words {
      height: 20vh;
      position: absolute;
      display: flex;
    }

    .words0{
/*      background: blue;*/
      margin-top: 0vh;
      animation: scrollWords 22s linear infinite;
    }

    .words1{
/*      background: red;*/
      margin-top: 25vh;
      animation: scrollWords 17s linear infinite;
    }

    .words2{
/*      background: blue;*/
      margin-top: 50vh;
      animation: scrollWords 25s linear infinite;
    }

    .words3{
/*      background: blue;*/
      margin-top: 75vh;
      animation: scrollWords 19s linear infinite;
    }

    .holder {
      width: 100vh;
      margin-right: 10px;
      margin-left: 10px;
      animation: scrollWords 18s linear infinite;
      overflow: hidden;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }

    .holder1{
      width: 20vh;
    }

    .holder2{
      margin: 0 5vh;
      width: 70vh;
    }

    .word {
      height: 20vh;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
    }

    .word img {
      height: 100%;
    }

    .chatting {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      font-size: 20px;
      
    }

    .chatting div:nth-child(odd){
      align-self: flex-start;
    }

    .chatting div:nth-child(even){
      align-self: flex-end;
    }

    .largefont {
      font-size: 170px;
    }

    .emoji {
      font-size: 160px;
    }

    .paragraph {
      font-size: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: flex-start;
      gap: 5px;
    }

    .bigfont {
      font-size: 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .bigfont div:nth-child(odd){
      align-self: flex-start;
      margin: 0 20px;
    }

    .bigfont div:nth-child(even){
      align-self: flex-end;
      margin: 0 20px;
    }

    @keyframes scrollWords {
      from { transform: translateX(0); }
      to { transform: translateX(-50%); }
    }
  </style>
</head>
<body>
<script>
    const socket = io();

    socket.on('connect', () => {
      console.log('Connected to server');
    });

    socket.on('server_response', (msg) => {
        console.log("msg: ", msg)
      document.getElementById("cover").style.display = "flex";
      document.getElementById("cover_msg").innerHTML = msg.data;
      setTimeout(() => {
          document.getElementById("cover").style.display = "none";
        }, 5000);
    });
  </script>



<div class="cover" id="cover">
  <div class="coverbox">
    <div id="cover_msg"></div>
  </div>
</div>

<!-- your scrolling word-box goes here -->
<div class="word-box">
  <div class="words words0">
    {{ scroll1|safe }}
  </div>
  <div class="words words1">
    {{ scroll2|safe }}
  </div>
  <div class="words words2">
    {{ scroll3|safe }}
  </div>
  <div class="words words3">
    {{ scroll4|safe }}
  </div>
</div>
</body>
</html>
"""




if __name__ == "__main__":
    # start_mqtt()
    app.run(port=5000)



















