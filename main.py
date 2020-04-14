import discord
import os, random, asyncio, time
import youtube_dl
import urllib.request, urllib.parse, re
from discord.ext import commands
from bs4 import BeautifulSoup

token = 'NTQzNzY3NTA1MTAyMDQ1MTk0.XpWt3A.Nwf6JrcIdCFqqXm7S8ULXw4CQGE'

bot = commands.Bot(command_prefix="!", activity=discord.Activity(name="Whale | !help", type=1))

footer = "Made by hsmint"

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def message(head, msg):
    e = discord.Embed(title=head, description=msg)
    e.set_footer(text=footer)
    return e

@bot.event
async def on_ready():
    print("Logged in as: "+ bot.user.name)

class Whale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whale(self, ctx):
        """Show random pictures of whale emoticon"""
        pick = random.randrange(1, 30)
        await ctx.send(file=discord.File('image/'+str(pick)+'.png'))
    
    @commands.command()
    async def ping(self, ctx):
        """Show bot's internet connection"""
        await ctx.send("Pong! `{0}ms`".format(round(bot.latency, 6)))
    
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.volume = 100
    
    @commands.command()
    async def join(self, ctx):
        """Join voice channel"""
        if ctx.author.voice is None:
            return await ctx.send("You are not in voice channel.")
        
        channel = ctx.author.voice.channel

        try:
            await channel.connect()
            await ctx.send("Connected to voice channel to "+ str(channel))
        
        except discord.ClientException:
            if channel == ctx.voice_client.channel:
                await ctx.send("I'm already in voice channel.")

            else:
                await ctx.send("Moving voice channel to " + str(channel))
                await ctx.voice_client.disconnect()
                await channel.connect()

    @commands.command()
    async def play(self, ctx):
        """Play music(need url or word. Using youtube!)"""
        search = ctx.message.content[6:]
        if ctx.voice_client is None: return await ctx.send("I'm not connected to voice channel.")
        elif ctx.author.voice is None: return await ctx.send("You are not in voice channel.")
        if ctx.voice_client.is_playing():
            await ctx.send("Music is still playing.\nDo you want to stop this music?(y/n)")
            try:
                chk = await self.bot.wait_for('message', timeout=20.0)
                while not (chk.content.lower() == 'y' or chk.content.lower() == 'n'):
                    chk = await self.bot.wait_for('message', timeout=10.0)
                if chk.content.lower() == 'y' : ctx.voice_client.stop()
                else : return
            
            except asyncio.TimeoutError:
                await ctx.send("Timeout.")
                return
        if (search.startswith("https:")): url = search
        else:
            query = urllib.parse.urlencode({"search_query" : search})
            search_url = "https://www.youtube.com/results?search_query=" + query
            response = urllib.request.urlopen(search_url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            result = []
            result_url = []
            for music in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
                if (music['href'].find('watch') == 1 and music['href'].find('list') != 21):
                    result.append(music['title'])
                    result_url.append(music['href'])
            music_list = "0. " + result[0] + "\n1. " + result[1] + "\n2. " + result[3] + "\n3. " + result[4] + "\n4. " + result[5]
            await ctx.send(embed=message("Search result", music_list+"\nc. cancel"))
            try:
                cmd = await self.bot.wait_for('message', timeout=10.0)
                while not (cmd.content.isdigit() or cmd.content == 'c'):
                    cmd = await self.bot.wait_for('message', timeout=2.0)
                if cmd.content == 'c': return await ctx.send("Canceled.")
                elif (cmd.content.isdigit()) : url = "https://www.youtube.com" + result_url[int(cmd.content)]
        
            except asyncio.TimeoutError:
                await ctx.send("Timeout.")
                return
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            ctx.voice_client.source.volume = self.volume / 100
        
        await ctx.send('Now playing: {}'.format(player.title))
    
    @commands.command()
    async def stop(self, ctx):
        """Stop playing music"""
        if ctx.voice_client is None:
            return await ctx.send("I'm not in voice channel.")
        
        if ctx.voice_client.is_playing() == True:
            ctx.voice_client.stop()
            return await ctx.send("Stopped music.")
        
        else: return await ctx.send("There is no music playing.")

    @commands.command()
    async def volume(self, ctx, volume):
        """Change volume"""
        if ctx.voice_client is None: return await ctx.send("I'm not connected to a voice channel.")
        elif ctx.author.voice is None: return await ctx.send("You are not in voice channel.")
        if(volume != int and (volume <= 0 or volume >= 11)): return await ctx.send("Please give input 1 to 10")
        self.volume = volume
        ctx.voice_client.source.volume = int(volume / 1000)
        await ctx.send("Changed volume to {}".format(volume))

    @commands.command()
    async def leave(self, ctx):
        """Leave voice channel"""
        if ctx.author.voice is None: return await ctx.send("You are not in voice channel.")
        try:
            channel = ctx.voice_client.channel
            await ctx.send("Leaving voice channel " + str(channel))
            await ctx.voice_client.disconnect()
        
        except AttributeError:
            await ctx.send("I'm not in voice channel.")
            
#bot Catergory
bot.add_cog(Whale(bot))
bot.add_cog(Music(bot))

bot.run(token)
