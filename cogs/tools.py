from discord.ext import commands
import asyncio


class Tools(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['purge', 'clear'], brief='Clear previous amount of messages. (ADMIN)')
    async def clean(self, ctx, limit: int = 100):
        await ctx.channel.purge(limit=limit + 1)
        clear_message = await ctx.send(f'Cleared by {ctx.author.mention}')
        await asyncio.sleep(3)
        await clear_message.delete()


def setup(client):
    client.add_cog(Tools(client))
