import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


class YukiBot(discord.Client):
    @bot.event
    async def on_ready(self):
        print('{0} se ha iniciado :D!'.format(self.user))

    @bot.command(name='hi')
    async def saludo(self, ctx):
        await ctx.send("Hola")

"""
@bot.event
async def on_ready():
    print('Yukibot online :D!')
    bot.load_extension('cogs.music')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the :100: emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
"""
yukiClient = YukiBot()
yukiClient.run(TOKEN)

#bot.run(TOKEN)