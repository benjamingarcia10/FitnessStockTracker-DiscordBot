import os
import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

is_tracking_rogue = None
items_to_check = []


class Rogue(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def startrogue(self, ctx):
        await ctx.message.delete()
        global is_tracking_rogue, items_to_check

        is_tracking_rogue = True

        start_msg = await ctx.send(f'Starting Rogue Tracking?: {is_tracking_rogue}')

        embed_description = 'Please enter all Rogue items you want tracked separated by line breaks.'
        embed_msg = discord.Embed(title='Rogue Tracking', color=5111552, description=embed_description)
        rogue_items_to_track = await ctx.send(embed=embed_msg)
        timeout_time = 30
        timeout_msg = 'Timed Out or Invalid Input.'

        try:
            items_response = await self.client.wait_for('message', timeout=timeout_time)
        except:
            await ctx.send(timeout_msg)
            await items_response.delete()
            await start_msg.delete()
            is_tracking_rogue = False
            stop_msg = await ctx.send(f'Starting Rogue Tracking?: {is_tracking_rogue}')
        else:
            for item in items_response.content.split('\n'):
                if len(item) <= 0 or item[0] == '#' or item[0:2] == '//':
                    continue
                elif item not in items_to_check:
                    items_to_check.append(item)

            # await items_response.delete()
            # await rogue_items_to_track.edit(embed=embed_msg)
            await ctx.send(items_to_check)





    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stoprogue(self, ctx):
        global is_tracking_rogue
        is_tracking_rogue = False
        await ctx.send(f'Starting Rogue Tracking?: {is_tracking_rogue}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def statusrogue(self, ctx):
        await ctx.send(f'Starting Rogue Tracking?: {is_tracking_rogue}')


def setup(client):
    client.add_cog(Rogue(client))
