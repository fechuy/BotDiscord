import discord
from discord.ext import commands
from discord import utils
from discord import Embed

class Reddit(commands.Cog):
    def __init__(self, user):
        self.user = user
    
    @commands.command(name="reddit", help='Este comando es para traer cosas de reddit')
    async def hi(self, ctx):
        await ctx.send("{0.author} los saluda :sunglasses:".format(ctx))
        
def setup(bot):
    bot.add_cog(Reddit(bot))