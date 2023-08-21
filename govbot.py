import asyncio
import discord
import requests
import os
import pandas as pd
import urllib.parse
from dotenv import load_dotenv
# import time

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

govid = os.getenv("GOVID")
discordtoken = os.getenv("DISCORD_TOKEN")


def get_data_with_session(session_id):
    url = "https://inbox.goverland.xyz/feed?limit=1&offset=0&unread="

    headers = {
        "Authorization": govid
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors

        data = response.json()  # Assuming the response is in JSON format
        # print(data)
        return data

    except requests.RequestException as e:
        print(f"Error occurred while fetching data: {e}")
        return None


async def send_message_to_discord(channel, title, link):
    message = f"New proposal: [{title}]({link})"
    await channel.send(message)


async def listen_to_url(session_id):
    last_data = None

    while True:
        try:
            rawdata = get_data_with_session(session_id)
            data = pd.DataFrame(rawdata)
            title = data["proposal"][0]["title"]
            link = data["proposal"][0]["link"]
            formatted_url = urllib.parse.quote(link, safe=':/#')

            # print(f"New data: {title}")

            # Send the new event message to Discord chat
            await send_message_to_discord(channel, title, formatted_url)

        except Exception as e:
            print(f"Error occurred: {e}")

        # Set the interval (in seconds) to wait before checking for updates
        await asyncio.sleep(10)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Get the channel where the bot is connected (assuming it is only connected to one channel)
    global channel
    channel = client.get_channel(client.guilds[0].text_channels[0].id)

    # Start the listening task
    client.loop.create_task(listen_to_url(govid))

if __name__ == "__main__":
    # Replace this with your actual Discord bot token
    token = discordtoken

    client.run(token)
