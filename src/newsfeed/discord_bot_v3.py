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
        "[+] Bot running   ",
    ]

    try:
        while True:
            for message in messages:
                print(f"\r{message}", end="", flush=True)
                await asyncio.sleep(0.2)
    except asyncio.CancelledError:
        pass


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


def add_line_breaks(text, line_length):
    line = ""
    lines = []
    sentences = text.split(". ")

    for sentence in sentences:
        line += " " + sentence

        # check if it should add line break.
        if len(line.split(" ")) >= line_length or sentence == sentences[-1]:
            lines.append(line)
            line = ""

    # returns new text with line breakes.
    return ". \n \n".join(lines)


# Check for new articles and send summaries
async def check_and_send(blog_name="mit"):
    # Call get_latest_article from his script
    title, summary, link, date = get_latest_article(blog_name, summary_type="non_technical")

    send_discord_message(
        DISCORD_WEBHOOK_URL,
        "alexnet",
        title,
        add_line_breaks(summary, 20),
        date.strftime("%Y-%m-%d"),
        link,
    )

    await asyncio.sleep(5)


# asyncio loop and scheduling
async def main():
    dot_animation_task = asyncio.create_task(animate_dots())

    try:
        await asyncio.gather(check_and_send(), asyncio.sleep(10))  # Sleep for 10 seconds
    except KeyboardInterrupt:
        print("\r[+] Bot interrupted  ", flush=True)
        for task in asyncio.all_tasks():
            task.cancel()
        await asyncio.gather(*asyncio.all_tasks())
    finally:
        dot_animation_task.cancel()  # Cancel the animation task
        print("\r[-] Bot finished ", end="", flush=True)
        await dot_animation_task  # Wait for animation to finish
        print(" ", flush=True)  # Clear the line


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
