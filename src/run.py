import os

from dotenv import load_dotenv
import interactions
from interactions import ButtonStyle

from src.application.components import ComponentsService, ButtonAction

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = int(os.getenv("DISCORD_GUILD"))


def main():
    bot = interactions.Client(
        command_prefix="/", token=DISCORD_TOKEN, default_scope=DISCORD_GUILD
    )

    # --- EVENTS ---

    @bot.event
    async def on_ready():
        print(f"{bot.me.name} is connected to the following guilds:\n")
        for guild in bot.guilds:
            print(f"{guild.name}(id: {guild.id})")

    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f"Hi {member.name}, welcome to {bot.guilds[0].name} 🤖! All you have to do is type a slash “/” to bring "
            f"up a list of commands that Goverland Bot can do!"
        )

    @bot.event
    async def on_error(event, *args):
        """
        This call back function will be executed in case of any error happened
        in the server side of the bot. You can think about it as a global error handler.
        We don't handle specific errors at the moment.
        """
        if event == "on_message":
            print(f"Unhandled message: {args[0]}\n")
        else:
            raise

    # --- COMMANDS ---

    # --- INFO ---
    @bot.command(
        name="help",
        description="👩🏻‍💻🔜Here will be a link to the documentation (public notion page)",
    )
    async def bot_help(ctx):
        message = "Help documentation is in progress: \n🔜🐣"
        await ctx.send(message)

    @bot.command(
        name="support",
        description="👩🏻‍💻🔜Join Goverland Bot-Support channel.",
    )
    async def support(ctx):
        message = "Goverland Bot Support is in progress: \n🔜🐣 "
        await ctx.send(message)

    @bot.command(
        name="info",
        description="👩🏻‍💻🔜Read basic info about Goverland.",
    )
    async def info(ctx):
        message = """About Goverland: \n🔜🐣  (Copyright, Privacy Policy and Terms of Service):
        About: https://www.goverland.xyz
        Privacy Policy: https://www.goverland.xyz/privacy
        """

        # button_link ("About Goverland")
        # button_link ("Privacy Policy")
        await ctx.send(message)

    # --- ADMIN ---

    @bot.command(
        name="start",
        description="Responds with a start command",
    )
    async def start(ctx):
        message = "All you have to do is type a slash “/” to bring up a list of commands that Goverland Bot can do!"
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

    @bot.component(ComponentsService.get_custom_id(ButtonAction.UNSUBSCRIBE))
    async def unsubscribe_button_response(ctx):
        await ctx.send(f"You unsubscribed!", ephemeral=True)

    @bot.command(
        name="subscriptions",
        description="👩🏻‍💻🔜Show all user subscriptions",
        # Uncomment when we go to production
        # default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    )
    async def subscriptions(ctx):
        message = """
### Aave (73,9k voters)

https://icodrops.com/wp-content/uploads/2017/10/aave_logo-150x150.jpg
"""
        await ctx.send(
            message,
            components=[
                ComponentsService.create_button(
                    action=ButtonAction.UNSUBSCRIBE,
                    style=ButtonStyle.DANGER,
                    label="Unsubscribe",
                )
            ],
        )

    bot.start()


if __name__ == "__main__":
    main()
