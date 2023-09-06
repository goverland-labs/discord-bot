import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View
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
intents.typing = False
intents.presences = False

govid = os.getenv("GOVID")
discordtoken = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)
listening = False

con = sqlite3.connect("subs.db")
cur = con.cursor()


@bot.command()
async def gov_help(ctx):
    await ctx.send("The following commands are available: \n"
                   "gov_sub - needs to be called once to generate subscription for your server \n"
                   "gov_start - actviate to start sending notifications \n"
                   "gov_stop - stops sending notifications till resumed \n"
                   "search_dao - helps search for the DAO you need to subscribe. Search word needs to be specified such as !search_dao_key 'search word' \n"
                   "add_dao - adds subscription to a particular dao to notifications feed. Format !add_dao 'name' \n"
                   "remove_dao - removes subscription to a particular dao from notifications feed. Format !remove_dao 'name'")


@bot.command()
async def gov_sub(ctx):
    server_id = ctx.guild.id
    print(server_id)

    query = "SELECT distinct(serverid) FROM subs WHERE serverid = ?"
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

    query = "SELECT distinct(serverid) FROM subs WHERE serverid = ?"
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


def search_dao_key(dao, session_id):
    url = f"https://inbox.goverland.xyz/dao?query={dao}&offset=0&limit=1"
    headers = {
        "Authorization": session_id
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for any HTTP errors
    data = response.json()
    data = pd.DataFrame(data)
    daoid = data['id'][0]
    return daoid


@bot.command()
async def search_dao(ctx, dao_name: str):
    server_id = ctx.guild.id
    query = "SELECT distinct(sessionid) FROM subs WHERE serverid = ?"
    res = cur.execute(query, (server_id,))
    data = res.fetchone()
    session_id = data[0]

    url = f"https://inbox.goverland.xyz/dao?query={dao_name}&offset=0&limit=5"
    headers = {
        "Authorization": session_id
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for any HTTP errors
    data = response.json()
    data = pd.DataFrame(data)

    for index, row in data.iterrows():

        df_str = data['name'][index]
        button = Button(label=df_str, custom_id=df_str)

        async def button_callback(interaction):
            server_id = ctx.guild.id
            query = "SELECT distinct(sessionid) FROM subs WHERE serverid = ?"
            res = cur.execute(query, (server_id,))
            data = res.fetchone()
            session_id = data[0]
            dao_name = interaction.data['custom_id']

            dao_identifier = search_dao_key(dao_name, session_id)

            url = "https://inbox.goverland.xyz/subscriptions"
            headers = {
                "Authorization": session_id
            }
            data = {
                "dao": dao_identifier
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Check for any HTTP errors

            # await ctx.send(f"You subscribed to DAO: {dao_name}")
            await interaction.response.send_message(f"You subscribed to DAO: {dao_name}")

        button.callback = button_callback

        view = View()
        view.add_item(button)
        await ctx.send(view=view)


@bot.command()
async def add_dao(ctx, dao_name: str):
    server_id = ctx.guild.id
    query = "SELECT distinct(sessionid) FROM subs WHERE serverid = ?"
    res = cur.execute(query, (server_id,))
    data = res.fetchone()
    session_id = data[0]

    dao_identifier = search_dao_key(dao_name, session_id)

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


@bot.command()
async def remove_dao(ctx, dao_name: str):
    server_id = ctx.guild.id
    query = "SELECT distinct(sessionid) FROM subs WHERE serverid = ?"
    res = cur.execute(query, (server_id,))
    data = res.fetchone()
    session_id = data[0]

    dao_identifier = search_dao_key(dao_name, session_id)

    url = f"https://inbox.goverland.xyz/subscriptions/{dao_identifier}"
    headers = {
        "Authorization": session_id
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()  # Check for any HTTP errors

    await ctx.send(f"You unsubscribed from DAO: {dao_identifier}")


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
        query = "SELECT distinct(sessionid) FROM subs WHERE serverid = ?"
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
