import asyncio
import datetime
import json
import os
import xml.etree.ElementTree as ET
import requests
import schedule

#imported libraries 


# Built in packages

# Import the get_summary function
from newsfeed import get_summary
from newsfeed.get_summary import get_summary

summary = get_summary("Explain like i'm five")  # Replace with correct summary type


# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1144176316535541773/xbf8ien_4kcghHum5NpqH1gGWuuOJeSxfLWRAzCiMuSRIE-jI0EENx95EgMcT875LUdO"

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
    tree = ET.parse(metadata_file_path)
    root = tree.getroot()
    articles = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        description = item.find("description").text
        link = item.find("link").text  # Assuming link is available in metadata
        published = item.find("pubDate").text  # Assuming published date is available
        articles.append(
            {
                "title": title,
                "description": description,
                "link": link,
                "published": published,
            }
        )

    if messages_sent_today < 3:
        for article in articles:
            if messages_sent_today >= 3:
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
