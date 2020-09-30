import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from datetime import datetime
import variables
from data.items import categories
from helpers.auth import is_authorized
from helpers.notifications import send_rogue_error_webhook
import logging

# Start logging to discord.log file
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load environment variables
load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')

# Insert names of cogs that you don't want to initialize at startup (default = all cogs loaded)
DO_NOT_LOAD_COGS_AT_STARTUP = []

# Initialize Discord bot and add global command check from auth
client = commands.Bot(command_prefix=variables.command_prefix)
client.add_check(is_authorized)

# Set max length per check (If check time exceeds this time, it will send an error and stop tracking)
max_length_per_check = 180


# When bot is loaded and ready
@client.event
async def on_ready():
    # Set bot presence
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f'Fitness Stock | {variables.command_prefix}help'))
    print(f'{client.user} has connected to Discord and is ready!')

    # If bot lost connection, send status update to inform bot tracking has restarted
    if variables.is_tracking_rogue:
        send_rogue_error_webhook(f'ERROR #1: Cloud Server connection error. Bot reconnected and Rogue tracking has '
                                 f'automatically been restarted. Verify checks with {variables.command_prefix}status '
                                 f'or by viewing console logs.', stop_tracking=False)


# Compare current check time length every 60 seconds with max_length_per_check
# and if it exceeds, send error and stop tracking.
@tasks.loop(seconds=60)
async def verify_rogue_tracking_integrity():
    if not variables.is_tracking_rogue:
        return
    else:
        if variables.last_successful_check_datetime is not None:
            time_difference = datetime.now() - variables.last_successful_check_datetime
            print(f'\tTime Difference since last successful check: {time_difference.total_seconds()}')
            if time_difference.total_seconds() > max_length_per_check:
                send_rogue_error_webhook(f'ERROR #0: Cloud Server connection error. Rogue check script has frozen '
                                         f'with {time_difference.total_seconds()} seconds since last successful check '
                                         f'at {variables.last_successful_check}. Please restart Rogue tracking with '
                                         f'{variables.command_prefix}rogue.')
                variables.last_successful_check_datetime = None


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


# Specific error handler for authrole command
@authrole.error
async def role_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.message.delete()
        await ctx.send('Could not find that role.')


# Load cog specified in command
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


# Unload cog specified in command
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


# Reload cog specified in command
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


# Load all cogs initially except those in the DO_NOT_LOAD_COGS_AT_STARTUP list
for filename in os.listdir('./cogs'):
    if f'{filename.split(".", 1)[0]}' in DO_NOT_LOAD_COGS_AT_STARTUP:
        continue
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Start verify_rogue_tracking_integrity task
try:
    verify_rogue_tracking_integrity.start()
    variables.rogue_integrity_check = True
except Exception as e:
    variables.rogue_integrity_check = False
    send_rogue_error_webhook(f'{type(e)} - {e}: Unable to start Rogue tracking integrity. Please check console logs '
                             f'and restart Rogue tracking with {variables.command_prefix}rogue.')


# Start bot
client.run(TOKEN)

# Assign notify role ids and webhooks for all categories based on .env file
# Set .env file variables to:
# <CATEGORY>-role-id=<ROLE ID TO TAG FOR THIS ITEM> (If unassigned, it will tag @everyone when notifies are on)
# <CATEGORY>-webhook=<WEBHOOK URL TO POST STOCK UPDATE TO> (If unassigned, it will post to ROGUE_FITNESS_WEBHOOK_URL env variable
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

# Assign bot manager id based on .env file
# Set .env file variable to:
# bot-manager-id=<ROLE ID FOR BOT MANAGER TO TAG ON ERRORS> (If unassigned, will not tag anyone)
try:
    bot_manager_id = int(os.getenv('bot-manager-id'))
except:
    bot_manager_id = None
variables.bot_manager = discord.utils.find(lambda m: m.id == bot_manager_id, client.guilds[0].roles)
if variables.bot_manager is not None:
    print(f'Set Bot Manager to: {variables.bot_manager.name} (Role ID: {variables.bot_manager.id})')
else:
    print(f'No Bot Manager Set (use {variables.command_prefix}authrole to set a role)')
