"""
Automated Article Summary Discord Bot

This script automates the process of fetching article summaries and broadcasting them to a Discord channel via a webhook. It constantly monitors for new articles, generates concise summaries, and transmits the summaries along with relevant details to the specified channel.

Imports:
- Standard Python Libraries: asyncio, json, os, requests, xml.etree.ElementTree as ElementTree
- Required External Package: schedule
- External Function: get_latest_article (imported from a friend's script)

Global Variables:
- DISCORD_WEBHOOK_URL: URL of the Discord webhook for message delivery.
- METADATA_FILE_PATH: Path to the XML metadata file.

Functions:
- send_discord_message: Formats and sends messages to the designated Discord channel.
- check_and_send: Scans for recent articles, summarizes them, and forwards to Discord.
- main: Asynchronous loop for scheduling periodic article checks.

Usage:
Execute this script to automatically collect article summaries and broadcast them on Discord.

"""

# Native to Python
import asyncio
import json
import os
import requests
import schedule
import xml.etree.ElementTree as ElementTree

# Import functions from his script
from summarize import get_latest_article, summarize_text

# Load key from api-key.json
with open("api-key.json") as f:
    keys = json.load(f)

# Get the Discord webhook URL from api-key.json
DISCORD_WEBHOOK_URL = keys["DISCORD_WEBHOOK_URL"]

# Configuration and Global Variables
METADATA_FILE_PATH = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "Github",
    "iths-data-engineering-group-alexnet",
    "data",
    "data_lake",
    "mit",
    "metadata.xml",
)

# Send message to Discord with Markdown formatting
def send_discord_message(webhook_url, group_name, title, summary, published_date, article_link):
    message = (
        f"**Group-name:** {group_name}\n# {title}\n"
        f"\n\n{summary}\n\n[Article Link]({article_link})\n\n"
        f"**Published Date:** {published_date}"
    )
    embed = {"description": message, "color": 0x00FF00}
    payload = {"embeds": [embed]}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

# Check for new articles and send summaries
async def check_and_send():
    # Call get_latest_article from his script
    title, summary, link, date = get_latest_article(summary_type="non_technical")

    send_discord_message(
        DISCORD_WEBHOOK_URL,
        "alexnet",
        title,
        summary,
        date.strftime("%Y-%m-%d"),
        link,
    )

    await asyncio.sleep(5)

# asyncio loop and scheduling
async def main():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(check_and_send(), main()))
