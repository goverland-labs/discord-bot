import asyncio
import discord
import requests
# import time

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def get_data_with_session(session_id):
    url = "https://inbox.goverland.xyz/dao/top?limit=1"

    headers = {
        "Cookie": f"session_id={'f1543764-a7c5-48d1-8438-aa4f08c68517'}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors

        data = response.json()  # Assuming the response is in JSON format
        return data

    except requests.RequestException as e:
        print(f"Error occurred while fetching data: {e}")
        return None


async def send_message_to_discord(channel, data):
    message = f"New event: {data}"
    await channel.send(message)


async def listen_to_url(session_id):
    last_data = None

    while True:
        try:
            data = get_data_with_session(session_id)

            # Check if new data is available
            if data and data != last_data:
                print(f"New data: {data}")
                last_data = data

                # Send the "hello" message to Discord chat
                await send_message_to_discord(channel, "hello")

                # Send the new event message to Discord chat
                await send_message_to_discord(channel, data)

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
    client.loop.create_task(listen_to_url(
        "f1543764-a7c5-48d1-8438-aa4f08c68517"))

if __name__ == "__main__":
    # Replace this with your actual Discord bot token
    token = "MTEzNTQ4OTkyMzk5NTE1MjQzNA.Gyvp-K.IDjKt-uNkZ3PMKBdzQQCu2JhqHfKVMeOWyh51A"

    client.run(token)
