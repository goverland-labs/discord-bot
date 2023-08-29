from discord.ext import commands
from discord.ext.commands import Context


@commands.command(name="test")
async def test(ctx: Context, arg):
    print("Channel: ", ctx.channel)
    await ctx.send(arg)


@commands.hybrid_command(name="hybrid")
async def hybrid(ctx: Context, name):
    await ctx.send(f"Got param: {name}")
