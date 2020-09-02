import variables
from discord.ext import commands

developer_id = 433083891109330945


async def is_authorized(ctx):
    if ctx.author.permissions_in(ctx.channel).administrator:
        return True
    if ctx.author.id == developer_id:
        return True
    if variables.bot_manager in ctx.author.roles:
        return True
    raise commands.MissingRole(variables.bot_manager)
