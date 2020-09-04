import variables
from discord.ext import commands

developer_id = 433083891109330945
allowed_commands = ['help']


# Global command check to see if user is authorized to use command
# Commands in the allowed_commands list will be authorized by anyone
async def is_authorized(ctx):
    if ctx.command.name in allowed_commands:
        return True
    if ctx.author.permissions_in(ctx.channel).administrator:
        return True
    if ctx.author.id == developer_id:
        return True
    if variables.bot_manager in ctx.author.roles:
        return True
    raise commands.MissingRole(variables.bot_manager)
