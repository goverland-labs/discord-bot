import asyncio
import discord
from discord.ext import commands
import requests
import os
import pandas as pd
import urllib.parse
import sqlite3
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

govid = os.getenv("GOVID")
discordtoken = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)
listening = False


@bot.command()
async def start(ctx):
    global listening  # Use the global flag
    listening = True
    await ctx.send("Goverland bot activated. Now listening for proposals.")


@bot.command()
async def stop(ctx):
    global listening  # Use the global flag
    listening = False
    await ctx.send("Goverland bot deactivated. No longer listening for proposals.")


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


def mark_item_as_read(feed_id):
    base_url = "https://inbox.goverland.xyz/feed"
    url = f"{base_url}/{feed_id}/mark-as-read"

    headers = {
        "Authorization": govid
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return True  # Feed marked as read successfully
    else:
        print("Failed to mark feed as read. Status code:", response.status_code)
        print("Response content:", response.text)
        return False


async def send_message_to_discord(channel, title, link):
    message = f"New proposal: [{title}]({link})"
    await channel.send(message)


async def listen_to_url(session_id):

    while True:
        if listening:
            try:
                rawdata = get_data_with_session(session_id)
                data = pd.DataFrame(rawdata)
                title = data["proposal"][0]["title"]
                link = data["proposal"][0]["link"]
                formatted_url = urllib.parse.quote(link, safe=':/#')
                feed_id = data['id'][0]

                # print(f"New data: {title}")

                # Send the new event message to Discord chat
                await send_message_to_discord(channel, title, formatted_url)

                mark_item_as_read(feed_id)

            except Exception as e:
                print(f"Error occurred: {e}")

            # Set the interval (in seconds) to wait before checking for updates
        await asyncio.sleep(10)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    # Get the channel where the bot is connected (assuming it is only connected to one channel)
    global channel
    channel = bot.get_channel(bot.guilds[0].text_channels[0].id)

    # Start the listening task
    bot.loop.create_task(listen_to_url(govid))

if __name__ == "__main__":
    # Replace this with your actual Discord bot token
    token = discordtoken
    bot.run(token)
