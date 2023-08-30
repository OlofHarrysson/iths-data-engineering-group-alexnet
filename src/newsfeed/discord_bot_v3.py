"""
Discord Bot for Article Summaries

This script fetches article summaries and sends them to a Discord channel using a webhook. It checks for new articles, summarizes them, and sends the summaries along with relevant information to the designated channel.

Imports:
- Native to Python: asyncio, datetime, json, os, xml.etree.ElementTree as ElementTree
- Requires Installation: requests, schedule
- External Function: get_summary (from newsfeed.get_summary)

Global Variables:
- DISCORD_WEBHOOK_URL: Discord webhook URL for sending messages.
- MESSAGES_LIMIT: Limit for messages sent per day.
- METADATA_FILE_PATH: Path to the XML metadata file.

Functions:
- send_discord_message: Sends formatted messages to the Discord channel.
- check_and_send: Checks for new articles, summarizes, and sends them to Discord.
- main: Asynchronous loop for scheduling article checks.

Usage:
Run this script to periodically fetch article summaries and send them to Discord.
"""

# Native to Python
import asyncio
import datetime
import json
import os
import xml.etree.ElementTree as ElementTree

# Requires installation
import requests
import schedule

# Import the get_summary function
from newsfeed.get_summary import get_summary

# Load key from api-key.json
with open("api-key.json") as f:
    keys = json.load(f)

# Get the Discord webhook URL from api-key.json
DISCORD_WEBHOOK_URL = keys["DISCORD_WEBHOOK_URL"]

# Configuration and Global Variables
DISCORD_WEBHOOK_URL = keys["DISCORD_WEBHOOK_URL"]
MESSAGES_LIMIT = 3
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

# Global variables to track the number of messages sent and the current date
messages_sent_today = 0
current_date = datetime.date.today()



# Send message to Discord with Markdown formatting
def send_discord_message(webhook_url, group_name, title, summary, published_date, article_link):
    global messages_sent_today
    message = (
        f"**Group-name:** {group_name}\n# {title}\n"
        f"\n\n{summary}\n\n[Article Link]({article_link})\n\n"
        f"**Published Date:** {published_date}"
    )
    embed = {"description": message, "color": 0x00FF00}
    payload = {"embeds": [embed]}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()
    messages_sent_today += 1

# Check for new articles and send summaries
async def check_and_send():
    global messages_sent_today, current_date
    today = datetime.date.today()

    # If it's a new day, reset the messages_sent_today count
    if today != current_date:
        current_date = today
        messages_sent_today = 0

    # Parse XML metadata
    tree = ElementTree.parse(METADATA_FILE_PATH)
    root = tree.getroot()
    articles = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        description = item.find("description").text
        link = item.find("link").text
        published = item.find("pubDate").text
        articles.append(
            {
                "title": title,
                "description": description,
                "link": link,
                "published": published,
            }
        )

    if messages_sent_today < MESSAGES_LIMIT:
        for article in articles:
            if messages_sent_today >= MESSAGES_LIMIT:
                break

            summary = get_summary("Explain like i'm five")  # Replace with correct summary type
            send_discord_message(
                DISCORD_WEBHOOK_URL,
                "alexnet",
                article["title"],
                summary,
                article["published"],
                article["link"],
            )
            messages_sent_today += 1
            await asyncio.sleep(5)

# asyncio loop and scheduling
async def main():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(check_and_send(), main()))
