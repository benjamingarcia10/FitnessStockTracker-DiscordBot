from discord.ext import commands


class Tools(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=['purge', 'clear'], brief='Clear previous amount of messages.')
    @commands.has_permissions(administrator=True)
    async def clean(self, ctx, limit: int = 100):
        await ctx.channel.purge(limit=limit + 1)
        clear_message = await ctx.send(f'Cleared by {ctx.author.mention}')
        await clear_message.delete()


def setup(client):
    client.add_cog(Tools(client))
