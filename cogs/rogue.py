import os
import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

start_rogue_tracking = None


class Rogue(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def startrogue(self, ctx):
        global start_rogue_tracking
        start_rogue_tracking = True
        await ctx.send(f'Starting Rogue Tracking?: {start_rogue_tracking}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stoprogue(self, ctx):
        global start_rogue_tracking
        start_rogue_tracking = False
        await ctx.send(f'Starting Rogue Tracking?: {start_rogue_tracking}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def statusrogue(self, ctx):
        await ctx.send(f'Starting Rogue Tracking?: {start_rogue_tracking}')


def setup(client):
    client.add_cog(Rogue(client))
