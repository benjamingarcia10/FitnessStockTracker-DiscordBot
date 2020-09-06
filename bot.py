import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import variables
from data.items import categories
from helpers.auth import is_authorized
from helpers.notifications import send_rogue_error_webhook
from helpers.threadedChecker import reset_rogue_variables, start_tracking_rogue

load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
DO_NOT_LOAD_COGS_AT_STARTUP = []

client = commands.Bot(command_prefix=variables.command_prefix)
client.add_check(is_authorized)


# When bot is loaded and ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f'Fitness Stock | {variables.command_prefix}help'))
    if variables.is_tracking_rogue:
        send_rogue_error_webhook(f'Cloud Server connection error. Attempting to restart Rogue tracking.',
                                 stop_tracking=False)
        try:
            variables.rogue_persist = True
            reset_rogue_variables()
            start_tracking_rogue()
        except Exception as e:
            send_rogue_error_webhook(f'Unable to automatically restart: {type(e)} - {e}. Bot managers or server admins '
                                     f'please restart Rogue tracking ({variables.command_prefix}rogue).')
        else:
            send_rogue_error_webhook(f'Rogue tracking has been successfully restarted with persist mode enabled.',
                                     stop_tracking=False)
        # TODO Restart Rogue tracking if bot was previously tracking before being shut down.
    for category in categories:
        try:
            role_id = int(os.getenv(f'{category}-role-id'))
        except:
            role_id = None
        variables.rogue_category_data[category] = {
            'notify_role': discord.utils.find(lambda m: m.id == role_id, client.guilds[0].roles),
            'webhook_url': os.getenv(f'{category}-webhook')
        }
    print(f'Category Tracking: {variables.rogue_category_data}')
    print(f'{client.user} has connected to Discord and is ready!')


# Command error handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("You don't have the permissions to run this command!")
    elif isinstance(error, commands.MissingRole):
        await ctx.message.delete()
        await ctx.send("You don't have the proper role(s) to run this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send('Please pass in all required arguments.')
    else:
        print(f'{type(error)} - {error}')


# Logout and close all bot connections to Discord
@client.command(aliases=['logout', 'close', 'disconnect', 'exit'],
                brief='Take bot offline for maintenance and send message. (ADMIN)')
async def maintenance(ctx):
    await ctx.message.delete()
    await ctx.send(f'Bot going offline for maintenance and updates.')
    await client.close()


# Authorize role by id or name to use bot commands
@client.command(brief='Gets or sets authorized bot manager role. (ADMIN)')
async def authrole(ctx, role: discord.Role = None):
    await ctx.message.delete()
    if role is None:
        if variables.bot_manager is None:
            await ctx.send(f'No authorized bot manager role is currently assigned.')
        else:
            await ctx.send(f'Current authorized bot manager role set to: {variables.bot_manager.mention}')
    else:
        variables.bot_manager = role
        await ctx.send(f'Set the authorized bot manager role to: {role.mention}')


@authrole.error
async def role_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.message.delete()
        await ctx.send('Could not find that role.')


# Load cogs
@client.command(brief='Loads specified extension (ADMIN)')
async def load(ctx, extension):
    await ctx.message.delete()
    try:
        client.load_extension(f'cogs.{extension}')
    except commands.ExtensionError as e:
        await ctx.send(f'**`ERROR:`** {e.name} - {e}')
    else:
        await ctx.send(f'{extension.capitalize()} cog has been loaded.')
        print(f'{extension.capitalize()} cog has been loaded.')


# Unload cogs
@client.command(brief='Unloads specified extension (ADMIN)')
async def unload(ctx, extension):
    await ctx.message.delete()
    try:
        client.unload_extension(f'cogs.{extension}')
    except commands.ExtensionError as e:
        await ctx.send(f'**`ERROR:`** {e.name} - {e}')
    else:
        await ctx.send(f'{extension.capitalize()} cog has been unloaded.')
        print(f'{extension.capitalize()} cog has been unloaded.')


# Reload cogs
@client.command(brief='Reloads specified extension (ADMIN)')
async def reload(ctx, extension=None):
    await ctx.message.delete()
    if extension is None:
        reload_message = await ctx.send(f'Reloading all cogs.')
        for filename in os.listdir('./cogs'):
            if f'{filename.split(".", 1)[0]}' in DO_NOT_LOAD_COGS_AT_STARTUP:
                continue
            if filename.endswith('.py'):
                extension_name = filename.split(".", 1)[0].capitalize()
                cog_extension = f'cogs.{filename[:-3]}'
                try:
                    client.unload_extension(cog_extension)
                except:
                    client.load_extension(cog_extension)
                else:
                    client.load_extension(cog_extension)
                await ctx.send(f'{extension_name} cog has been reloaded.')
        await reload_message.delete()
    else:
        try:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
        except commands.ExtensionError as e:
            await ctx.send(f'**`ERROR:`** {e.name} - {e}')
        else:
            await ctx.send(f'{extension.capitalize()} cog has been reloaded.')
            print(f'{extension.capitalize()} cog has been reloaded.')


# Load all cogs except those in the DO_NOT_LOAD_COGS_AT_STARTUP list
for filename in os.listdir('./cogs'):
    if f'{filename.split(".", 1)[0]}' in DO_NOT_LOAD_COGS_AT_STARTUP:
        continue
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
