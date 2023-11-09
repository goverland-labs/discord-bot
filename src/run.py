import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from src.commands import test, hybrid

load_dotenv()


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="$", intents=intents)
    bot.add_command(test)
    bot.add_command(hybrid)

    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")
        for guild in bot.guilds:
            print(f"Guild {guild}. ID: {guild.id}")
        print("All channels:")
        for channel in bot.get_all_channels():
            print(channel)

    bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
