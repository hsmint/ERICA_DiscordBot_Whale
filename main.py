import discord
from discord.ext import commands
import os
import random

token = os.environ["discord_auth"]

app = discord.Client()

@app.event
async def on_ready():
    print("Log in as :", app.user.name)
    await app.change_presence(activity=discord.Activity(name="Currently Not Available", type=1))

@app.event
async def on_message(ctx):
    if ctx.author == app.user:
        return
    
    if ctx.content.startswith("!whale"):
        pick = random.randrange(1, 30)
        await ctx.channel.send(file=discord.File('image/'+str(pick)+'.png'))

app.run(token)


