import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def joke(ctx):
    response = fetch_chuck_norris_joke()
    await ctx.send(response)


def fetch_chuck_norris_joke():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    joke_data = response.json()
    return joke_data.get("value", "No joke available")


bot.run("YOUR_BOT_TOKEN_HERE")
