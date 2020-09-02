import discord
from discord.ext import commands
from discord import utils
from discord import Embed

class Acciones(commands.Cog):
    def __init__(self, user):
        self.user = user
    
    @commands.command(name="saludo", help='Este comando es para saludar a todos en el chat :D')
    async def hi(self, ctx):
        print("Saludaste a todos :D que buen amigo")
        await ctx.send("{0.author} los saluda :sunglasses:".format(ctx))
        
def setup(bot):
    bot.add_cog(Acciones(bot))