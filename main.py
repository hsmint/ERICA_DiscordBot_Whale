import discord
from discord.ext import commands
import os
import random

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

bot.run(token)


