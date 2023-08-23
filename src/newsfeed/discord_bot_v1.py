import asyncio
import datetime
import xml.etree.ElementTree as ET

import openai
import requests
import schedule

# OpenAI API key
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1131522847509069874/Lwk1yVc4w623xpRPkKYu9faFdMNvV5HTZ3TCcL5DgsIgeqhEvo9tBookvuh2S4IWysTt"

# Global variables to track the number of messages sent and the current date
messages_sent_today = 0
current_date = datetime.date.today()


# Parse XML metadata
def parse_xml_metadata(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    articles = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        description = item.find("description").text
        articles.append({"title": title, "description": description})

    return articles


# Summarize text using OpenAI API
def summarize_text(article):
    prompt = f"Summarize the following text:\n{article['description']}\nSummary:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
    )
    summary = response.choices[0].text.strip()
    return summary


# Send message to Discord with Markdown formatting
def send_discord_message(webhook_url, title, summary):
    global messages_sent_today  # Use the global variable
    message = f"**Group-name:** alexnet\n# {title}\n### Summary:\n\n{summary}"
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

    articles = parse_xml_metadata(
        "C:/Users/user/Desktop/Github/iths-data-engineering-group-alexnet/data/data_lake/mit/metadata.xml"
    )

    # Limit to sending 2 messages per day
    if messages_sent_today < 3:
        for article in articles:
            if messages_sent_today >= 3:
                break
            summary = summarize_text(article)
            send_discord_message(DISCORD_WEBHOOK_URL, article["title"], summary)
            messages_sent_today += 1
            await asyncio.sleep(5)  # Add a 5-second delay between messages


# asyncio loop
async def main():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(check_and_send(), main()))
