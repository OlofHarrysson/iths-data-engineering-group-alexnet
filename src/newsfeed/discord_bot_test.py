# for testing new stuff before implenting into the main bot, right now it attempts to solve the storage of previous articles and giving the user ability to retreive them.

import asyncio
import json

import discord
from discord.ext import commands

# Define the bot's intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  # Enable message content intent

from newsfeed.summarize import get_latest_article, summary_types


# Define a custom help command class
class CustomHelpCommand(commands.HelpCommand):
    # This method sends a list of available commands and their short descriptions when users run !help

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Bot Commands",
            description="Here's a list of available commands and their short descriptions:",
            color=discord.Color.blue(),
        )

        # Create a list of commands and their short descriptions
        command_list = [
            f"`{command.name}`: {command.short_doc}"
            for command in self.context.bot.commands
            if command.short_doc
        ]

        # Add the list to the embed
        embed.add_field(name="Commands", value="\n".join(command_list), inline=False)

        await self.get_destination().send(embed=embed)

        # You can also add additional information here if needed
        await self.get_destination().send(
            "For more details on a specific command, use `!help [command]`."
        )

    async def send_cog_help(self, cog):
        pass

    # This method sends a detailed explanation of a specific command when users run !help [command]
    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Command: {command.name}", description=command.help, color=discord.Color.green()
        )
        await self.get_destination().send(embed=embed)


# Define the bot with the specified intents and custom help command
bot = commands.Bot(command_prefix="!", intents=intents, help_command=CustomHelpCommand())

# Global variables for storing the latest articles
latest_articles = []


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("------")


# Command to send a private message to the bot
@bot.command()
async def send_dm(ctx, *, message):
    # Get the author of the message (the user who sent the command)
    user = ctx.author

    # Send a DM to the user with the provided message
    await user.send(f"You sent the following message to the bot: {message}")


# Command to send a message
@bot.command()
async def send_message(ctx):
    """
    Sends a hello message to a channel.
    """
    # Replace 'your_channel_id' with the actual channel ID where you want to send the message
    channel = bot.get_channel(1148542025491288095)

    # Send a message to the specified channel
    await channel.send("Hello World")
    print("Command executed: !send_message")


# Command to provide a more detailed explanation for the send_message command
@bot.command()
async def send_message_description(ctx):
    """
    Provides a more detailed explanation for the send_message command.
    """
    await ctx.send("This command sends a hello message to a channel.")


@bot.command()
async def summary(ctx, summary_type: str, language: str = "english"):
    """
    Sends a summary of the latest article via DM.
    Usage: !summary [summary_type] [language]
    Example: !summary non_technical swedish
    """
    if summary_type in summary_types:
        latest_title, summary, latest_link, latest_date = get_latest_article(
            blog_identifier="mit", summary_type=summary_type
        )
        await ctx.author.send(
            f"Summary Type: {summary_type}\nTitle: {latest_title}\nSummary: {summary}\nLink: {latest_link}\nDate: {latest_date}"
        )

        # Store the latest article
        latest_articles.append((latest_title, summary, latest_link, latest_date))

        await ctx.send(f"Summary sent via DM! Check your messages.")
    else:
        await ctx.send(
            "Invalid summary type. Supported types: normal, non_technical, swedish, french"
        )


@bot.command()
async def get_latest(ctx):
    """
    Get the latest article summary.
    Usage: !get_latest
    """
    if latest_articles:
        latest_title, latest_summary, latest_link, latest_date = latest_articles[-1]
        await ctx.send(
            f"Latest Article:\nTitle: {latest_title}\nSummary: {latest_summary}\nLink: {latest_link}\nDate: {latest_date}"
        )
    else:
        await ctx.send("No latest articles available.")


@bot.command()
async def get_previous(ctx, index: int = 1):
    """
    Get a previous article summary by index.
    Usage: !get_previous [index]
    Example: !get_previous 2
    """
    if index > 0 and index <= len(latest_articles):
        previous_title, previous_summary, previous_link, previous_date = latest_articles[-index]
        await ctx.send(
            f"Previous Article {index}:\nTitle: {previous_title}\nSummary: {previous_summary}\nLink: {previous_link}\nDate: {previous_date}"
        )
    else:
        await ctx.send("Invalid index or no previous articles available.")


# Load key from api-key.json
with open("api-key.json") as f:
    keys = json.load(f)

# Run the bot with your bot token
bot.run(keys["DISCORD_TOKEN"])  # Use the token loaded from the JSON file
