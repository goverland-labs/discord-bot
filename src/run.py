import os
from dotenv import load_dotenv
import interactions
from src.components import ButtonHello

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = int(os.getenv('DISCORD_GUILD'))


def main():
    bot = interactions.Client(command_prefix='/', token=DISCORD_TOKEN, default_scope=DISCORD_GUILD)

    # --- EVENTS ---

    @bot.event
    async def on_ready():
        print(
            f'{bot.me.name} is connected to the following guild:\n'
            f'{bot.guilds[0].name}(id: {bot.guilds[0].id})'
        )

    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to {bot.guilds[0].name} 🤖! All you have to do is type a slash “/” to bring '
            f'up a list of commands that Goverland Bot can do!')

    @bot.event
    async def on_error(event, *args):
        if event == 'on_message':
            print(f'Unhandled message: {args[0]}\n')
        else:
            raise

    # --- COMMANDS ---

    @bot.command(
        name='help',
        description='👩🏻‍💻🔜Here will be a link to the documentation (public notion page)',
    )
    async def bot_help(ctx):
        message = 'Read the documentation here: \n🔜🐣  '
        await ctx.send(message)

    @bot.command(
        description="Search your favorite DAO",
        name="search_dao",
        options=[
            interactions.Option(
                name="text",
                description="What DAO do you want to search?",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def search_dao(ctx: interactions.CommandContext, text: str):
        await ctx.send(f"You are searching for '{text}'!")

    @bot.command(
        name="button_test",
        description="This is the first command I made!",
    )
    async def button_test(ctx):
        await ctx.send("testing", components=ButtonHello)

    @bot.component("hello")
    async def button_response(ctx):
        await ctx.send("You clicked the Button :O", ephemeral=True)

    @bot.command(
        name='start',
        description='Responds with a start command',
    )
    async def start(ctx):
        message = 'All you have to do is type a slash “/” to bring up a list of commands that Goverland Bot can do!'
        await ctx.send(message)

    @bot.command(
        name='info',
        description='👩🏻‍💻🔜Read basic info about Goverland.',
    )
    async def info(ctx):
        message = '''About Goverland: \n🔜🐣  (Copyright, Privacy Policy and Terms of Service):
About: https://www.goverland.xyz
Privacy Policy: https://www.goverland.xyz/privacy
'''
        await ctx.send(message)

    @bot.command(
        name='support',
        description='👩🏻‍💻🔜Join Goverland Bot-Support channel.',
    )
    async def support(ctx):
        message = 'Here will be a link to Goverland Bot-Support channel: \n🔜🐣 '
        await ctx.send(message)

    @bot.command(
        name='subscriptions',
        description='👩🏻‍💻🔜Show all user subscriptions',
    )
    async def subscriptions(ctx):
        message = 'There are the results: \n🔜☕️'
        await ctx.send(message)
        await ctx.send("https://imgur.com/gallery/x8qFLU8")

    bot.start()


if __name__ == '__main__':
    main()
