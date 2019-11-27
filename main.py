import discord
from discord.ext import commands
import os

token = os.environ["discord_auth"]

app = commands.Bot(command_prefix='$')

@app.event
async def on_ready():
    print("Log in as :", app.user.name)
    await app.change_presence(activity=discord.Activity(name="Currently Not Available", type=1))

app.run(token)


