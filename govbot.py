import asyncio
import discord
from discord.ext import commands
import requests
import os
import pandas as pd
import urllib.parse
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

govid = os.getenv("GOVID")
discordtoken = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)
listening = False

con = sqlite3.connect("subs.db")
cur = con.cursor()


@bot.command()
async def gov_sub(ctx):
    server_id = ctx.guild.id
    print(server_id)

    query = "SELECT serverid FROM subs WHERE serverid = ?"
    res = cur.execute(query, (server_id,))
    check = res.fetchone() is True

    if check:
        value = server_id
        result_string = f"{value}"
        url = "https://inbox.goverland.xyz/auth/guest"
        data = {
            "device_id": result_string
        }
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for any HTTP errors

        data = response.json()  # Assuming the response is in JSON format
        session_id = data["session_id"]

        query = "INSERT INTO subs (serverid, sessionid) VALUES (?, ?)"
        cur.execute(query, (server_id, session_id))
        con.commit()
        await ctx.send("Successfully subscribed to Goverland bot")

    else:
        await ctx.send("You are already subscribed")


@bot.command()
async def gov_start(ctx):
    server_id = ctx.guild.id

    query = "SELECT serverid FROM subs WHERE serverid = ?"
    res = cur.execute(query, (server_id,))
    check = res.fetchone() is True

    if check:
        await ctx.send("You are already subscribed")
    else:
        global listening  # Use the global flag
        listening = True
        await ctx.send("Goverland bot activated. Now listening for proposals.")


@bot.command()
async def gov_stop(ctx):
    global listening  # Use the global flag
    listening = False
    await ctx.send("Goverland bot deactivated. No longer listening for proposals.")


@bot.command()
async def gov_add_dao(ctx, dao_identifier: str):
    server_id = ctx.guild.id
    query = "SELECT sessionid FROM subs WHERE serverid = ?"
    res = cur.execute(query, (server_id,))
    data = res.fetchone()
    session_id = data[0]

    url = "https://inbox.goverland.xyz/subscriptions"
    headers = {
        "Authorization": session_id
    }
    data = {
        "dao": dao_identifier
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Check for any HTTP errors

    await ctx.send(f"You subscribed to DAO: {dao_identifier}")


def subscribe():
    url = "https://inbox.goverland.xyz/auth/guest"


def get_data_with_session(session_id):
    url = "https://inbox.goverland.xyz/feed?limit=1&offset=0&unread="

    headers = {
        "Authorization": session_id
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


def mark_item_as_read(feed_id, session_id):
    base_url = "https://inbox.goverland.xyz/feed"
    url = f"{base_url}/{feed_id}/mark-as-read"

    headers = {
        "Authorization": session_id
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return True  # Feed marked as read successfully
    else:
        print("Failed to mark feed as read. Status code:", response.status_code)
        print("Response content:", response.text)
        return False


async def send_message_to_discord(channel, title, link):
    print(channel)
    message = f"New proposal: [{title}]({link})"
    await channel.send(message)


async def listen_to_url(session_id):

    while True:
        if listening:
            try:
                rawdata = get_data_with_session(session_id)
                data = pd.DataFrame(rawdata)
                print(data)
                provided_datetime = str(data["created_at"][0])
                provided_datetime_obj = datetime.strptime(
                    provided_datetime, '%Y-%m-%dT%H:%M:%SZ')
                current_datetime = datetime.utcnow()
                one_day_ago = current_datetime - timedelta(days=1)

                if provided_datetime_obj > one_day_ago:
                    title = data["proposal"][0]["title"]
                    link = data["proposal"][0]["link"]
                    formatted_url = urllib.parse.quote(link, safe=':/#')
                    feed_id = data['id'][0]

                    # print(f"New data: {title}")

                    # Send the new event message to Discord chat
                    await send_message_to_discord(channel, title, formatted_url)

                    mark_item_as_read(feed_id, session_id)
                else:
                    print(
                        "The provided datetime is not higher than current timestamp minus one day.")

            except Exception as e:
                print(f"Error occurred: {e}")

            # Set the interval (in seconds) to wait before checking for updates
        await asyncio.sleep(10)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    for guild in bot.guilds:
        server_id = guild.id

        # Get the channel where the bot is connected (assuming it is only connected to one channel)
        global channel
        channel = bot.get_channel(bot.guilds[0].text_channels[0].id)

        server_id = guild.id
        query = "SELECT sessionid FROM subs WHERE serverid = ?"
        res = cur.execute(query, (server_id,))
        data = res.fetchone()

        if data:
            session_id = data[0]
            print(session_id)
            for text_channel in guild.text_channels:
                # Start the listening task
                bot.loop.create_task(listen_to_url(session_id))

if __name__ == "__main__":
    # Replace this with your actual Discord bot token
    token = discordtoken
    bot.run(token)
