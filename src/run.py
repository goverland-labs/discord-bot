from dotenv import dotenv_values
import discord
from discord.ext import commands
from src.commands import test, hybrid


def main():
    intents = discord.Intents.default()
    intents.message_content = True

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

    config = dotenv_values(".env")
    bot.run(config["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
