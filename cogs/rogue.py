from data.items import search_urls
import discord
from discord.ext import commands
from datetime import datetime
from threadedChecker import start_tracking_rogue, stop_tracking_rogue, reset_rogue_variables
from helpers.notifications import send_test_discord_webhook
from helpers.auth import is_authorized

import variables


class Rogue(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['startrogue'], brief='Start tracking Rogue items. (ADMIN)')
    # @commands.has_permissions(administrator=True)
    @commands.check(is_authorized)
    async def rogue(self, ctx):
        command_author = ctx.message.author
        await ctx.message.delete()

        if variables.is_tracking_rogue:
            await ctx.send(f'Rogue is currently tracking {len(variables.items_to_check)} products. Stop checking '
                           f'before starting a new task by running /roguestop (admin command only).')
            return

        variables.items_to_check = {}
        variables.checked_items = {}

        timeout_time = 30
        timeout_msg = 'Timed Out or Invalid Input.'

        embed_description = f'Please enter all Rogue items you want tracked separated by line breaks. ' \
                            f'Find all available items here (use the name in the command column): ' \
                            f'https://roguestockbot.com/current-items. {timeout_time} second timeout.'
        embed_msg = discord.Embed(title='Rogue Stock Tracker', color=5111552, description=embed_description)
        # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
        embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
        rogue_items_to_track_message = await ctx.send(embed=embed_msg)

        def check(message):
            return message.author == command_author and message.content.strip()[0] != variables.command_prefix

        try:
            items_response = await self.client.wait_for('message', check=check, timeout=timeout_time)
        except:
            await ctx.send(timeout_msg)
            await rogue_items_to_track_message.delete()
            variables.is_tracking_rogue = False
        else:
            embed_description = ''
            item_number = 1
            for item in items_response.content.lower().strip().split('\n'):
                formatted_item = item.lower().strip()
                try:
                    if len(formatted_item) <= 0 or formatted_item[0] == '#' or formatted_item[0:2] == '//':
                        continue
                    elif formatted_item not in variables.items_to_check:
                        variables.items_to_check[formatted_item] = search_urls[formatted_item]
                        embed_description += f'{item_number}: {variables.items_to_check[formatted_item]["product_name"]}\n'
                        print(
                            f'Tracking stock for "{formatted_item}": {variables.items_to_check[formatted_item]["product_name"]}')
                        item_number += 1
                    else:
                        print(f'Found "{formatted_item}" which has already been added.')
                except KeyError:
                    print(f'Found "{formatted_item}" which is not a valid product item. Skipping this item.')

            await items_response.delete()

            if len(variables.items_to_check) <= 0:
                await ctx.send('No valid items found.')
                await rogue_items_to_track_message.delete()
                variables.is_tracking_rogue = False
            else:
                embed_msg.title = 'Starting Rogue Stock Tracking'
                start_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                embed_msg.description = f'**Start Time:** {start_time}\n\n{embed_description}'
                embed_msg.set_footer(text=f'Started: {start_time}', icon_url='https://i.imgur.com/LbZlRjA.png')
                await rogue_items_to_track_message.edit(embed=embed_msg)
                reset_rogue_variables()
                start_tracking_rogue()

    @commands.command(brief='Stop tracking Rogue items. (ADMIN)')
    # @commands.has_permissions(administrator=True)
    @commands.check(is_authorized)
    async def roguestop(self, ctx):
        await ctx.message.delete()

        if variables.is_tracking_rogue:
            stop_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

            embed_description = f'**Stop Time:** {stop_time}\n\n**Stopped Tracking:**\n'

            item_number = 1
            for item in variables.items_to_check:
                embed_description += f'{item_number}: {variables.items_to_check[item]["product_name"]}\n'
                item_number += 1

            embed_msg = discord.Embed(title='Stopping Rogue Stock Tracking', color=16711680,
                                      description=embed_description)
            embed_msg.set_footer(text=f'Stopped: {stop_time}', icon_url='https://i.imgur.com/LbZlRjA.png')
            # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
            embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
            stop_tracking_message = await ctx.send(embed=embed_msg)
            stop_tracking_rogue()
        else:
            await ctx.send('Rogue stock is not currently being tracked.')

    @commands.command(brief='Send a test Rogue stock webhook. (ADMIN)')
    # @commands.has_permissions(administrator=True)
    @commands.check(is_authorized)
    async def roguetest(self, ctx):
        await ctx.message.delete()
        send_test_discord_webhook()

    @commands.command(brief='Toggle Rogue persist logging. (ADMIN)')
    # @commands.has_permissions(administrator=True)
    @commands.check(is_authorized)
    async def roguepersist(self, ctx):
        await ctx.message.delete()
        if variables.rogue_persist:
            variables.rogue_persist = False
            await ctx.send('Rogue Persist Mode turned off. Bot will notify any in stock items at every startup.')
        else:
            variables.rogue_persist = True
            await ctx.send('Rogue Persist Mode turned on. Bot will not notify items that were previously '
                           'notified if they are still in stock upon next startup.')

    @commands.command(brief='Toggle Rogue persist logging. (ADMIN)')
    # @commands.has_permissions(administrator=True)
    @commands.check(is_authorized)
    async def roguestatus(self, ctx):
        await ctx.message.delete()

        current_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

        embed_description = f'''
**Current Time:** {current_time}

**Rogue Status:**
- Max Threads for checking: {variables.max_threads}
- Play sound on stock notification? {variables.play_notification_sound}
- Send text on stock notification? {variables.send_text_notification}
- Currently tracking Rogue? {variables.is_tracking_rogue}
- Rogue Debug Mode enabled? {variables.rogue_debug_mode}
- Rogue Persist Mode enabled? {variables.rogue_persist}
'''

        embed_msg = discord.Embed(title='Rogue Bot Status', color=16711680,
                                  description=embed_description)
        embed_msg.set_footer(text=f'Current Time: {current_time}', icon_url='https://i.imgur.com/LbZlRjA.png')
        # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
        embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
        status_message = await ctx.send(embed=embed_msg)

    @commands.command(brief='Toggles Rogue debug mode. (ADMIN)')
    # @commands.has_permissions(administrator=True)
    @commands.check(is_authorized)
    async def roguedebug(self, ctx):
        await ctx.message.delete()
        if variables.rogue_debug_mode:
            variables.rogue_debug_mode = False
            await ctx.send('Rogue Debug Mode turned off.')
        else:
            variables.rogue_debug_mode = True
            await ctx.send('Rogue Debug Mode turned on. Enabling additional console output.')


def setup(client):
    client.add_cog(Rogue(client))
