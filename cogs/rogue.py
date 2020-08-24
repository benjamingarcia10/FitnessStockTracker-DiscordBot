import os
from items import search_urls
import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from threadedChecker import start_tracking_rogue, stop_tracking_rogue, reset_rogue_variables

is_tracking_rogue = False
items_to_check = {}


class Rogue(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['startrogue'])
    @commands.has_permissions(administrator=True)
    async def rogue(self, ctx):
        await ctx.message.delete()
        global is_tracking_rogue, items_to_check

        items_to_check = {}
        timeout_time = 30
        timeout_msg = 'Timed Out or Invalid Input.'

        embed_description = f'Please enter all Rogue items you want tracked separated by line breaks. ' \
                            f'Find all available items here (use the name in the command column): ' \
                            f'https://roguestockbot.com/current-items. {timeout_time} second timeout.'
        embed_msg = discord.Embed(title='Rogue Stock Tracker', color=5111552, description=embed_description)
        # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
        embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
        rogue_items_to_track_message = await ctx.send(embed=embed_msg)

        try:
            items_response = await self.client.wait_for('message', timeout=timeout_time)
        except:
            await ctx.send(timeout_msg)
            await rogue_items_to_track_message.delete()
            is_tracking_rogue = False
        else:
            embed_description = ''
            item_number = 1
            for item in items_response.content.lower().strip().split('\n'):
                formatted_item = item.lower().strip()
                try:
                    if len(formatted_item) <= 0 or formatted_item[0] == '#' or formatted_item[0:2] == '//':
                        continue
                    elif formatted_item not in items_to_check:
                        items_to_check[formatted_item] = search_urls[formatted_item]
                        embed_description += f'{item_number}: {items_to_check[formatted_item]["product_name"]}\n'
                        print(f'Tracking stock for "{formatted_item}": {items_to_check[formatted_item]["product_name"]}')
                        item_number += 1
                    else:
                        print(f'Found "{formatted_item}" which has already been added.')
                except KeyError:
                    print(f'Found "{formatted_item}" which is not a valid product item. Skipping this item.')

            await items_response.delete()

            if len(items_to_check) <= 0:
                await ctx.send('No valid items found.')
                await rogue_items_to_track_message.delete()
                is_tracking_rogue = False
            else:
                embed_msg.title = 'Starting Rogue Stock Tracking'
                start_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                embed_msg.description = f'**Start Time:** {start_time}\n\n{embed_description}'
                embed_msg.set_footer(text=f'Started: {start_time}', icon_url='https://i.imgur.com/LbZlRjA.png')
                await rogue_items_to_track_message.edit(embed=embed_msg)
                is_tracking_rogue = True
                reset_rogue_variables()
                start_tracking_rogue(items_to_check)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stoprogue(self, ctx):
        await ctx.message.delete()
        global is_tracking_rogue, items_to_check

        if is_tracking_rogue:
            stop_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

            embed_description = f'**Stop Time:** {stop_time}\n\n**Stopped Tracking:**\n'

            item_number = 1
            for item in items_to_check:
                embed_description += f'{item_number}: {items_to_check[item]["product_name"]}\n'
                item_number += 1

            embed_msg = discord.Embed(title='Stopping Rogue Stock Tracking', color=5111552, description=embed_description)
            embed_msg.set_footer(text=f'Stopped: {stop_time}', icon_url='https://i.imgur.com/LbZlRjA.png')
            # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
            embed_msg.set_image(url='https://i.imgur.com/LbZlRjA.png')
            stop_tracking_message = await ctx.send(embed=embed_msg)

            items_to_check = {}
            is_tracking_rogue = False
            stop_tracking_rogue()
        else:
            await ctx.send('Rogue Stock is not currently being tracked.')


def setup(client):
    client.add_cog(Rogue(client))
