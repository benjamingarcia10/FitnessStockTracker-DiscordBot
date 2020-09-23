from discord.ext import commands
import discord
import asyncio
from helpers.auth import developer_id, developer_tag


class Tools(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Clear last messages (default is 100 messages unless otherwise set)
    @commands.command(aliases=['purge', 'clear'], brief='Clear previous amount of messages. (ADMIN)')
    async def clean(self, ctx, limit: int = 100):
        await ctx.channel.purge(limit=limit + 1)
        clear_message = await ctx.send(f'Cleared by {ctx.author.mention}')
        await asyncio.sleep(3)
        await clear_message.delete()

    # Send bot donation link
    @commands.command(aliases=['support'], brief='Send donation info to support the Rogue bot.')
    async def donate(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if user is not None:
            await ctx.send(user.mention)
        donation_url = 'https://www.buymeacoffee.com/benjamingarcia'
        donation_info = f"If the bot helped you get your items, consider supporting the project "\
                        f"to keep the bot updated and pay for monthly server costs to host the bot 24/7/365. :pray:"
        developer_mention = f'<@{developer_id}>'
        feature_info = f'If you have any feature requests or suggestions, please DM me {developer_mention}'
        embed_msg = discord.Embed(title='Support Rogue Bot Here!', color=5111552,
                                  url=donation_url)
        embed_msg.add_field(name='Donation Info', value=donation_info, inline=True)
        embed_msg.add_field(name='Donation Link', value=donation_url, inline=True)
        embed_msg.add_field(name='Bot Suggestions', value=feature_info, inline=False)

        # embed_msg.set_thumbnail(url='https://i.imgur.com/LbZlRjA.png')
        embed_msg.set_footer(text=f'Developer: {developer_tag}', icon_url='https://i.imgur.com/1lNJjf3.png')
        embed_msg.set_image(url='https://i.imgur.com/o0IXrJO.jpg')
        donation_message = await ctx.send(embed=embed_msg)

    @donate.error
    async def role_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await self.donate(ctx)


def setup(client):
    client.add_cog(Tools(client))
