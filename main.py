import discord
import os, random, asyncio, time
import youtube_dl
import urllib.request, urllib.parse, re
from discord.ext import commands
from bs4 import BeautifulSoup

token = os.environ["discord_auth"]

bot = commands.Bot(command_prefix="!",help_command=None, activity=discord.Activity(name="Whale | !help", type=1))

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
        pick = random.randrange(1, 30)
        await ctx.send(file=discord.File('image/'+str(pick)+'.png'))

    @commands.command()
    async def help(self, ctx):
        e = message("Help", "!whale - Show random picture of whale emoticon.")
        await ctx.send(embed=e)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong! `{0}ms`".format(round(bot.latency, 6)))
    
class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def game(self, ctx):
        text = "What game do you want to play!"
        e = message("<Showing Game available>", text)
        await ctx.send(embed=e)
    
    @commands.command()
    async def blackjack(self, ctx):
        return

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            e = message("", "You are not in voice channel.")
            await ctx.send(embed=e)
            return
        
        channel = ctx.author.voice.channel

        try:
            await channel.connect()
            e = message("", "Connected to voice channel to "+ str(channel))
            await ctx.send(embed=e)
        
        except discord.ClientException:
            if channel == ctx.voice_client.channel:
                e = message("", "I'm already in voice channel.")
                await ctx.send(embed=e)

            else:
                await ctx.send(embed=message("","Moving voice channel to " + str(channel)))
                await ctx.voice_client.disconnect()
                await channel.connect()

    @commands.command()
    async def play(self, ctx, search):
        if ctx.voice_client is None:
            return await ctx.send("I'm not connected to voice channel.")

        if ctx.voice_client.is_playing():
            await ctx.send("Music is still playing.\nDo you want to stop this music?(y/n)")
            try:
                chk = await self.bot.wait_for('message', timeout=10.0)
                while not (chk.content == 'y' or chk.content == 'n'):
                    chk = await self.bot.wait_for('message', timeout=5.0)
                if chk.content == 'y' : ctx.voice_client.stop()
                else : return
            
            except asyncio.TimeoutError:
                await ctx.send("Timeout.")
                return

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
        
        await ctx.send('Now playing: {}'.format(player.title))
    
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I'm not in voice channel.")
        
        if ctx.voice_client.is_playing:
            ctx.voice_client.stop()
            return await ctx.send("Stopped music.")
        
        else:
            return await ctx.send("There is no music playing.")

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def leave(self, ctx):
        try:
            channel = ctx.voice_client.channel
            await ctx.send(embed=message("", "Leaving voice channel " + str(channel)))
            await ctx.voice_client.disconnect()
        
        except AttributeError:
            e= message("", "I'm not in voice channel.")
            await ctx.send(embed=e)
            
#bot Catergory
bot.add_cog(Whale(bot))
bot.add_cog(Game(bot))
bot.add_cog(Music(bot))

bot.run(token)