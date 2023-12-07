import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from src.commands import test, hybrid

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = int(os.getenv('DISCORD_GUILD'))


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.dm_messages = True
    intents.messages = True

    bot = commands.Bot(intents=intents, command_prefix="/")

    @bot.event
    async def on_ready():
        await bot.tree.sync(guild=discord.Object(id=DISCORD_GUILD))

        guild = bot.get_guild(DISCORD_GUILD)

        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    @bot.event
    async def on_member_join(member):
        guild = bot.get_guild(DISCORD_GUILD)

        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to {guild.name} 🤖!'
        )

    @bot.tree.command(
        name='start',
        description='Responds with a start command',
        guild=discord.Object(id=DISCORD_GUILD)
    )
    async def start(interaction):
        message = 'I\'m the human form of the 💯 emoji.'
        await interaction.response.send_message(message)

    @bot.event
    async def on_error(event, *args):
        if event == 'on_message':
            print(f'Unhandled message: {args[0]}\n')
        else:
            raise

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
