# import discord
# import asyncio

# intents = discord.Intents.default()
# intents.messages = True
# intents.guilds = True
# intents.message_content = True  # Required to read message content

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'Logged in as {client.user}')
#     channel = client.get_channel(1363627466253537291)
    
#     async for message in channel.history(limit=100):
#         print(f"{message.author}: {message.content}")


#     await client.close()


import discord
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.dm_messages = True  # ⚡ important
intents.message_content = True  # ⚡ required to read message text

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    user = await client.fetch_user(1275510960047784080)  # Fetch the user (not channel!)
    dm_channel = await user.create_dm()  # Create (or get) DM channel
    
    async for message in dm_channel.history(limit=100):
        print(f"{message.author}: {message.content}")
    
    await client.close()

import os
client.run(os.environ["DISCORD_TOKEN"])
