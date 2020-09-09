from data.items import search_urls, categories, get_items_by_category
import discord
from discord.ext import commands
from datetime import datetime
from helpers.threadedChecker import start_tracking_rogue, stop_tracking_rogue, reset_rogue_variables
from helpers.notifications import send_test_rogue_webhook
import variables
import asyncio.exceptions


class Rogue(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Start Rogue tracking
    @commands.command(aliases=['startrogue', 'roguestart'], brief='Start tracking Rogue items. (ADMIN)')
    async def rogue(self, ctx):
        command_author = ctx.message.author
        await ctx.message.delete()

        # Check if bot is already tracking Rogue
        if variables.is_tracking_rogue:
            await ctx.send(f'Rogue is currently tracking {len(variables.items_to_check)} products. Stop checking '
                           f'before starting a new task by running /roguestop (admin command only).')
            return

        # Reset variables to prevent overlap from previous instance
        variables.items_to_check = {}
        variables.checked_items = {}

        timeout_time = 30
        timeout_msg = 'Timed Out or Invalid Input.'

        # Prompt for what items to track
        embed_description = f'Please enter all Rogue items you want tracked separated by line breaks. ' \
                            f'Find all available items here (use the name in the command column): ' \
                            f'https://roguestockbot.com/current-items. {timeout_time} second timeout. If you would ' \
                            f'like to track an entire category, on a new line, type "category:" followed by the ' \
                            f'category name you want to track. Available categories: {categories}'
        embed_msg = discord.Embed(title='Rogue Stock Tracker', color=5111552, description=embed_description)
        # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
        embed_msg.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
        embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
        rogue_items_to_track_message = await ctx.send(embed=embed_msg)

        def check(message):
            return message.author == command_author and message.content.strip()[0] != variables.command_prefix

        # Add all items separated by new lines to items_to_check and set embed description
        try:
            items_response = await self.client.wait_for('message', check=check, timeout=timeout_time)
        except asyncio.exceptions.TimeoutError as e:
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
                    elif formatted_item.split(':')[0].strip() == 'category':
                        category_name = formatted_item.split(':')[1].strip()
                        category_items = get_items_by_category(category_name)
                        if len(category_items) > 0:
                            if len(embed_description) > 0:
                                embed_description += '\n'
                            embed_description += f'**Category: {category_name}**\n'
                            for category_item in category_items:
                                if category_item not in variables.items_to_check:
                                    variables.items_to_check[category_item] = search_urls[category_item]
                                    embed_description += f'{item_number}: ' \
                                                         f'{variables.items_to_check[category_item]["product_name"]}\n'
                                    print(
                                        f'Tracking stock for "{category_item}": '
                                        f'{variables.items_to_check[category_item]["product_name"]}')
                                    item_number += 1
                    elif formatted_item not in variables.items_to_check:
                        variables.items_to_check[formatted_item] = search_urls[formatted_item]
                        embed_description += f'{item_number}: ' \
                                             f'{variables.items_to_check[formatted_item]["product_name"]}\n'
                        print(f'Tracking stock for "{formatted_item}": '
                              f'{variables.items_to_check[formatted_item]["product_name"]}')
                        item_number += 1
                    else:
                        print(f'Found "{formatted_item}" which has already been added.')
                except KeyError as e:
                    print(f'Found "{e}" which is not a valid product item. Skipping this item.')

            await items_response.delete()

            # Send message if no items are found. Otherwise, start tracking Rogue
            if len(variables.items_to_check) <= 0:
                await ctx.send('No valid items found.')
                await rogue_items_to_track_message.delete()
                variables.is_tracking_rogue = False
            else:
                embed_msg.title = f'Starting Rogue Stock Tracking ({len(variables.items_to_check)} items)'
                start_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                embed_msg.description = f'**Start Time:** {start_time}\n\n{embed_description}'
                if len(embed_msg.description) >= 2048:
                    embed_msg.description = f'{embed_msg.description[0:2036]}\n**more...**'
                embed_msg.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
                await rogue_items_to_track_message.edit(embed=embed_msg)
                reset_rogue_variables()
                start_tracking_rogue()

    # Stop tracking Rogue
    @commands.command(aliases=['stop', 'stoprogue'], brief='Stop tracking Rogue items. (ADMIN)')
    async def roguestop(self, ctx):
        await ctx.message.delete()

        # Check if Rogue is being tracked
        # If so, send stop confirmation and stop Rogue tracking. Otherwise, indicate Rogue is not being tracked.
        if variables.is_tracking_rogue:
            stop_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

            embed_description = f'**Stop Time:** {stop_time}\n\n**Stopped Tracking:**\n'

            item_number = 1
            for item in variables.items_to_check:
                embed_description += f'{item_number}: {variables.items_to_check[item]["product_name"]}\n'
                item_number += 1

            embed_msg = discord.Embed(title=f'Stopping Rogue Stock Tracking ({len(variables.items_to_check)} items)',
                                      color=16711680, description=embed_description)
            if len(embed_msg.description) >= 2048:
                embed_msg.description = f'{embed_msg.description[0:2036]}\n**more...**'
            embed_msg.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
            # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
            embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
            stop_tracking_message = await ctx.send(embed=embed_msg)
            stop_tracking_rogue()
        else:
            await ctx.send('Rogue stock is not currently being tracked.')

    # Test all webhooks set to various categories
    @commands.command(aliases=['test', 'testrogue'], brief='Send a test Rogue stock webhook. (ADMIN)')
    async def roguetest(self, ctx):
        await ctx.message.delete()
        send_test_rogue_webhook()

    # Enable notifying roles on item restock webhook
    @commands.command(aliases=['notify', 'notifyrogue'], brief='Toggles Rogue Notify mode. (ADMIN)')
    async def roguenotify(self, ctx):
        await ctx.message.delete()
        if variables.rogue_notify:
            variables.rogue_notify = False
            await ctx.send('Rogue will no longer tag everyone when item stock notification is sent.')
        else:
            variables.rogue_notify = True
            await ctx.send('Rogue will tag everyone when item stock notification is sent.')

    # Enable debug print out in console
    @commands.command(aliases=['debug', 'debugrogue'], brief='Toggles Rogue debug mode. (ADMIN)')
    async def roguedebug(self, ctx):
        await ctx.message.delete()
        if variables.rogue_debug_mode:
            variables.rogue_debug_mode = False
            await ctx.send('Rogue Debug Mode turned off.')
        else:
            variables.rogue_debug_mode = True
            await ctx.send('Rogue Debug Mode turned on. Enabling additional console output.')

    # Enable persistent data whenever restarting Rogue tracking
    @commands.command(aliases=['persist', 'persistrogue'], brief='Toggle Rogue persist logging. (ADMIN)')
    async def roguepersist(self, ctx):
        await ctx.message.delete()
        if variables.rogue_persist:
            variables.rogue_persist = False
            await ctx.send('Rogue Persist Mode turned off. Bot will notify any in stock items at every startup.')
        else:
            variables.rogue_persist = True
            await ctx.send('Rogue Persist Mode turned on. Bot will not notify items that were previously '
                           'notified if they are still in stock upon next startup.')

    # Get status of Rogue tracker
    @commands.command(aliases=['status', 'statusrogue'], brief='View current Rogue bot status.')
    async def roguestatus(self, ctx):
        await ctx.message.delete()

        current_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

        embed_description = f'''
**Current Time:** {current_time}

**Rogue Status:**
- Max Threads for checking: {variables.max_threads}
- Play sound on stock notification? {variables.play_notification_sound}
- Send text on stock notification? {variables.send_text_notification}
- Currently tracking Rogue? {variables.is_tracking_rogue} - {len(variables.items_to_check)} item(s)
- Tagging everyone on stock notifications? {variables.rogue_notify}
- Rogue Debug Mode enabled? {variables.rogue_debug_mode}
- Rogue Persist Mode enabled? {variables.rogue_persist}

- Rogue Check Counter: {variables.check_counter}
- Last Successful Check: {variables.last_successful_check} with runtime of {variables.last_successful_check_runtime}
- Longest Run Time: {variables.longest_run_time}
- Average Run Time: {variables.average_run_time}
'''
        category_tracking_description = ''
        for category in variables.rogue_category_data:
            category_data = variables.rogue_category_data[category]
            if category_data['notify_role'] is not None or category_data['webhook_url'] is not None:
                category_tracking_description += f'{category}:\n- Role: {category_data["notify_role"]}\n'
                if category_data['webhook_url'] is not None:
                    category_tracking_description += f'- Webhook Set: ✅\n\n'

        if len(category_tracking_description) > 0:
            embed_description += f'\n**Category Specific Tracking (ENABLED):**\n{category_tracking_description}'
        else:
            embed_description += f'\n**Category Specific Tracking (DISABLED)**'

        embed_msg = discord.Embed(title='Rogue Bot Status', color=16711680,
                                  description=embed_description)
        if len(embed_msg.description) >= 2048:
            embed_msg.description = f'{embed_msg.description[0:2036]}\n**more...**'
        embed_msg.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
        embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
        # embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
        status_message = await ctx.send(embed=embed_msg)


def setup(client):
    client.add_cog(Rogue(client))
