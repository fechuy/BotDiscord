import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

yukiBot = commands.Bot(command_prefix='!Y')

@yukiBot.event
async def on_ready():
    print('{0.user} online :D!'.format(yukiBot))
    yukiBot.load_extension('cogs.music')
    yukiBot.load_extension('actions.actions')
    yukiBot.load_extension('reddit.reddit')

@yukiBot.command(name='99', help='Responds with a random quote from Brooklyn 99')
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

yukiBot.run(TOKEN)