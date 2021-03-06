import discord
import re
import math
from discord.ext import commands
from discord import utils
from discord import Embed
import lavalink

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 7000, 'test', 'na', 'music-node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)
        
    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        
    """@commands.command(name='join')
    async def join(self, ctx):
        print('Join commnad ;D')
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))"""
    
    @commands.command(name='play')
    async def play(self, ctx, *, query):
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            query = f'ytsearch:{query}'
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:10]
            i = 0
            query_result = ''
            
            for track in tracks:
                i = i + 1
                query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
                
            embed = Embed()
            embed.description = query_result
            await ctx.channel.send(embed=embed)

            def check(m):
                return m.author.id == ctx.author.id
            
            response = await self.bot.wait_for('message', check=check)
            track = tracks[int(response.content)-1]

            player.add(requester=ctx.author.id, track=track)
            if not player.is_playing:
                await player.play()
        
        except ValueError as value:
            print(value)
        
        except Exception as error:
            print(error)
            await ctx.send("Error al reproducir tu musica D:")    
            
    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guil_id)
            await self.connect_to(guild_id, None)
            
    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.
        
    @commands.command(name='skip')
    async def skip(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)        
        await player.skip()
        print("Saltaste una cancion D:")
        await ctx.send("{0.author} Saltaste una cancion D:".format(ctx))
    
    @commands.command(name='queue')
    async def queue(self, ctx, page: int = 1):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        
        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = Embed(colour=discord.Color.blurple(), description=f'**{len(player.queue)} tracks**\n\n{queue_list} :D')
        embed.set_footer(text=f'Pagina {page}/{pages}')
        await ctx.send(embed=embed)
        
    @commands.command(name='pausa')
    async def pause(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        await player.stop()
        #await player.set_pause(True)
        
    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.music.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | Disconnected.')

def setup(bot):
    bot.add_cog(Musica(bot))