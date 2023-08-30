import asyncio
import datetime
import json
import os
import xml.etree.ElementTree as ET

import openai
import requests
import schedule

# Import the summarize_text function from the summarize.py file
# from summarize import summarize_text
from newsfeed.get_summary import get_summary

# Get key
with open("api-key.json") as f:
    OPENAI_API_KEY = json.load(f)

openai.api_key = OPENAI_API_KEY["OPENAI_API_KEY"]

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1131522847509069874/Lwk1yVc4w623xpRPkKYu9faFdMNvV5HTZ3TCcL5DgsIgeqhEvo9tBookvuh2S4IWysTt"

# Global variables to track the number of messages sent and the current date
messages_sent_today = 0
current_date = datetime.date.today()

# Construct the path to the XML metadata file dynamically
metadata_file_path = os.path.join(
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
def send_discord_message(webhook_url, title, summary, link):
    global messages_sent_today  # Use the global variable
    message = f"**Group-name:** alexnet\n# {title}\n### Summary:\n\n{summary} \n\n link:{link}"
    embed = {"description": message, "color": 0x00FF00}
    payload = {"embeds": [embed]}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()
    messages_sent_today += 1  # Increment the count


# Check for new articles and send summaries
async def check_and_send():
    global messages_sent_today, current_date  # Use the global variables
    today = datetime.date.today()

    # If it's a new day, reset the messages_sent_today count
    if today != current_date:
        current_date = today
        messages_sent_today = 0

    # Parse XML metadata
    tree = ET.parse(metadata_file_path)
    root = tree.getroot()
    articles = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        description = item.find("description").text
        articles.append({"title": title, "description": description})

    # Limit to sending 2 messages per day
    if messages_sent_today < 3:
        for article in articles:
            if messages_sent_today >= 3:
                break
            # summary = summarize_text(article)
            summary, title, link = get_summary("French")
            send_discord_message(DISCORD_WEBHOOK_URL, title, summary, link)
            messages_sent_today += 1
            await asyncio.sleep(5)  # Add a 5-second delay between messages


# asyncio loop
async def main():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(check_and_send(), main()))
