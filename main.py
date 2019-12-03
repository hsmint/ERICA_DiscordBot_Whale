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
        self.bot = bot;

    @commands.command()
    async def whale(self, ctx):
        pick = random.randrange(1, 30)
        await ctx.send(file=discord.File('image/'+str(pick)+'.png'))

    @commands.command()
    async def help(self, ctx):
        e = discord.Embed(title="Help",  description="!whale - Show random picture of whale emoticon.")
        e.set_footer(text=footer)
        await ctx.send(embed=e)

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def game(self, ctx):
        text = "What game do you want to play!"
        e = discord.Embed(title="Play Game!", description=text)
        e.set_footer(text=footer)
        await ctx.send(embed=e)

bot.add_cog(Whale(bot))
bot.add_cog(Game(bot))
bot.run(token)


