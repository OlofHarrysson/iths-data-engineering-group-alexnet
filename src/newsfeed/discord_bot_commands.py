"""
Automated Discord Bot for Article Summaries

This script sets up a Discord bot that can perform various actions, including sending messages,
providing article summaries, and shutting down the bot. It uses the Discord.py library for
interacting with Discord and integrates with the Newsfeed module for fetching and summarizing
the latest articles.

Commands:
- !send_dm [message]: Send a direct message to the bot.
- !send_message: Send a hello message to a specific channel.
- !send_message_description: Get a detailed explanation of the send_message command.
- !summary [summary_type]: Get a summary of the latest article via DM.
- !shutdown: Shut down the bot (Admins only).

Custom Help Command:
- The bot features a custom help command that provides a list of available commands and
  their descriptions. Use !help to access it.

Dependencies:
- Discord.py: For Discord bot functionality.
- Newsfeed module: For fetching and summarizing articles.
- JSON file: Contains the Discord bot token and other configuration.

To use this script, run it with your bot's token provided in the 'api-key.json' file.

Author: Hannes
"""

import asyncio
import json

import discord
from discord.ext import commands

# Load key from api-key.json
with open("api-key.json") as f:
    keys = json.load(f)

# Define the bot's intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  # Enable message content intent

from newsfeed.summarize import get_latest_article, summarize_text, summary_types


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

        # For additional information about the different commands
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


# Command to select a summary type for the DM
@bot.command()
async def summary(ctx, summary_type: str):
    """
    Sends a summary of the latest article via DM.
    Usage: !summary [summary_type]
    Example: !summary non_technical
    """
    if summary_type in summary_types:
        latest_title, summary, latest_link, latest_date = get_latest_article(
            blog_identifier="mit", summary_type=summary_type
        )
        await ctx.author.send(
            f"Summary Type: {summary_type}\nTitle: {latest_title}\nSummary: {summary}\nLink: {latest_link}\nDate: {latest_date}"
        )
        await ctx.send(f"Summary sent via DM! Check your messages.")
    else:
        await ctx.send(
            "Invalid summary type. Supported types: normal, non_technical, swedish, french"
        )


# Command to shut down the bot
@bot.command()
async def shutdown(ctx):
    """
    Shuts down the bot after a 10-second delay.
    """
    if ctx.author.id == keys["DISCORD_ADMIN"]:  # Replace YOUR_USER_ID with Discord user Admins ID
        await ctx.send("Shutting down the bot in 10 seconds. Goodbye!")

        # Delay the shutdown for 10 seconds
        await asyncio.sleep(10)

        # Close the bot
        await bot.close()


# Error handler for CommandNotFound
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Type !help to see a list of available commands.")


# Run the bot with your bot token
bot.run(keys["DISCORD_TOKEN"])  # Use the token loaded from the JSON file
