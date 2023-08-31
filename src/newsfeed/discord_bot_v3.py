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
import xml.etree.ElementTree as ElementTree

import requests
import schedule

# Import functions from his script
from newsfeed.summarize import get_latest_article, summarize_text

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

# Animation function for the running dots
async def animate_dots():
    messages = [
        "[+] Bot running   ",
        "[+] Bot running.  ",
        "[+] Bot running.. ",
        "[+] Bot running...",
        "[+] Bot running.. ",
        "[+] Bot running.  ",
        "[+] Bot running   "
    ]

    while True:
        for message in messages:
            print(f"\r{message}", end="", flush=True)
            await asyncio.sleep(0.3)
        
        await asyncio.sleep(0.3)

# Send message to Discord with Markdown formatting
def send_discord_message(webhook_url, group_name, title, summary, published_date, article_link):
    message = (
        f"**Group-name:** {group_name}\n# {title}\n"
        f"\n\n{summary}\n\n🌐 [Full Article]({article_link})\n\n"
        f"**Published:** {published_date}\n\n"
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
    dot_animation_task = asyncio.create_task(animate_dots())
    await asyncio.gather(check_and_send(), asyncio.sleep(10))  # Sleep for 10 seconds
    dot_animation_task.cancel()  # Cancel the animation task

    print("\r[-] Bot shutting down   ", flush=True)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\r[+] Bot interrupted     ", flush=True)
        for task in asyncio.all_tasks():
            task.cancel()
        loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
    finally:
        print("\r[-] Bot shutting down   ", flush=True)
        loop.close()
