import variables
from discord.ext import commands

developer_id = 433083891109330945


async def is_authorized(ctx):
    is_developer = False
    has_bot_manager_role = False
    if ctx.author.id == developer_id:
        is_developer = True
    for role in ctx.author.roles:
        if str(role.id) == variables.bot_manager or role.name == variables.bot_manager:
            has_bot_manager_role = True
    if not is_developer and not has_bot_manager_role:
        raise commands.MissingRole(variables.bot_manager)
    return is_developer or has_bot_manager_role
