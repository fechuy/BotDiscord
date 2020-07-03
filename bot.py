# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:12:38 2020

@author: FELIPE.SANTANA
"""

import os, discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} se a conectado a discord :3')
    
client.run(TOKEN)