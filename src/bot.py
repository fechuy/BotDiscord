import os

#import discord
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

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
    
@bot.command(name='saludo', help='Comando para saludar :D')
async def hi(ctx):
    saludo = 'Hola a todos :D!!!'
    await ctx.send(saludo)

#Apartado para poner musica
  

bot.run(TOKEN)