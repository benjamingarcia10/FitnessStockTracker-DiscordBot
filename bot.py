import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '/'
DO_NOT_LOAD_COGS_AT_STARTUP = []

client = commands.Bot(command_prefix=COMMAND_PREFIX)


# When bot is loaded and ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name='Fitness Stock | /help'))
    print(f'{client.user} has connected to Discord and is ready!')
    print(f'Discord Token Found: {os.getenv("DISCORD_TOKEN")}')


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
    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send('Command not found.')
    else:
        print(error)


# Load cogs
@client.command(brief='Loads specified extension (ADMIN)')
@commands.has_permissions(administrator=True)
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
@commands.has_permissions(administrator=True)
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
@commands.has_permissions(administrator=True)
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
