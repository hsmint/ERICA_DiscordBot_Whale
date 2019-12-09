import discord
import os, random
from discord.ext import commands

token = os.environ["discord_auth"]

bot = commands.Bot(command_prefix="!",help_command=None, activity=discord.Activity(name="Whale | !help", type=1))

footer = "Made by hsmint"

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
        e = discord.Embed(title="Help",  description="!whale - Show random picture of whale emoticon.")
        e.set_footer(text=footer)
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
        e = discord.Embed(title="Showing Game available", description=text)
        e.set_footer(text=footer)
        await ctx.send(embed=e)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            e = discord.Embed(description="You are not in voice channel")
            e.set_footer(text=footer)
            await ctx.send(embed=e)
            return
        
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
            e = discord.Embed(description="Connected to voice channel: "+ str(channel))
            e.set_footer(text=footer)
            await ctx.send(embed=e)
        
        except discord.ClientException:
            e = discord.Embed(description="I'm already in voice channel.")
            e.set_footer(text=footer)
            await ctx.send(embed=e)
    
    @commands.command()
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
        
        except AttributeError:
            e= discord.Embed(description="I'm not in voice channel.")
            e.set_footer(text=footer)
            await ctx.send(embed=e)
            

#bot Catergory
bot.add_cog(Whale(bot))
bot.add_cog(Game(bot))
bot.add_cog(Music(bot))

bot.run(token)