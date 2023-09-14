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

import json
import logging
import os
import time
import xml.etree.ElementTree as ElementTree
from datetime import datetime

import requests
import schedule
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from newsfeed.db_engine import connect_to_db
from newsfeed.misc import add_line_breaks, animate_dots

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load key from api-key.json
with open("api-key.json") as f:
    keys = json.load(f)

# Get the Discord webhook URL from api-key.json
DISCORD_WEBHOOK_URL = keys["DISCORD_WEBHOOK_URL"]


def get_article(type: str = "normal", get_latest: bool = 1, table_name: str = None):
    engine, Base = connect_to_db()
    # Call this with "locally" to run locally.
    # TODO: Implement it as arg somwehere

    print("")

    Blog_summaries = Base.classes.blog_summaries
    Blog_info = Base.classes.bloginfo
    Bot_history = Base.classes.bot_history

    Session = sessionmaker(bind=engine)
    session = Session()

    if get_latest:
        article = (
            session.query(Blog_info, Blog_summaries)
            .join(Blog_summaries, Blog_info.unique_id == Blog_summaries.unique_id)
            .filter(Blog_summaries.type_of_summary == type)
            .order_by(Blog_info.published.desc())
            .limit(1)
            .first()
        )

    else:  # duplicate, use for secondary queries
        article = (
            session.query(Blog_info, Blog_summaries)
            .join(Blog_summaries, Blog_info.unique_id == Blog_summaries.unique_id)
            .filter(Blog_summaries.type_of_summary == type)
            .order_by(Blog_info.published.desc())
            .limit(1)
            .first()
        )

    bloginfo, blog_summary = article

    # set flag and log if article has been published
    published = (
        session.query(Bot_history)
        .filter_by(unique_id=bloginfo.unique_id, type_of_summary=blog_summary.type_of_summary)
        .first()
    )

    if published is None:
        logger.info(f"{bloginfo.unique_id}' has not been published.")

        new_record = Bot_history(
            unique_id=bloginfo.unique_id,
            type_of_summary=blog_summary.type_of_summary,
            publish_stamp=datetime.now(),
        )
        session.add(new_record)
        session.commit()

    title = (
        blog_summary.translated_title if blog_summary.translated_title != None else bloginfo.title
    )

    return title, blog_summary.summary, bloginfo.link, bloginfo.published, published  # is not None


# Send message to Discord with Markdown formatting
def send_discord_message(webhook_url, sender_name, title, summary, published_date, article_link):
    message = (
        f"**Breaking News from** {sender_name}\n# {title}\n"
        f"\n\n{summary}\n\n🌐 [Full Article]({article_link})\n\n"
        f"**Published:** {published_date}\n\n"
    )

    embed = {"description": message, "color": 0x00FF00}
    payload = {"embeds": [embed]}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()


# This function will always send latest article
def send_latest_article(summary_type="normal"):
    try:
        title, summary, link, date, _ = get_article(summary_type, get_latest=True)
        send_discord_message(
            DISCORD_WEBHOOK_URL,
            "Alexnet",
            title,
            add_line_breaks(summary, 20),
            date.strftime("%Y-%m-%d"),
            link,
        )
        logger.info("Latest article sent.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


# Check for new articles and send summaries
def check_and_send(summary_type="normal"):
    try:
        title, summary, link, date, published = get_article(summary_type)
    except TypeError as e:
        print(f"An error occurred: {e}")
        return

    if published == False:
        send_discord_message(
            DISCORD_WEBHOOK_URL,
            "Alexnet",
            title,
            add_line_breaks(summary, 20),
            date.strftime("%Y-%m-%d"),
            link,
        )

        logger.info("Article sent.")
        print("Article sent.")
    else:
        print("Debug: latest article has already been published!")
        send_text(f"Debug: Latest article {link}, has already been sent: {published.publish_stamp}")

    return


def main(debug: bool = False):
    if debug:
        if __name__ == "__main__":
            send_text("Debug: Running from script")
        else:
            send_text("Debug: Running from DAG")

        logger.info("Discord bot is fetching articles.")

    try:
        check_and_send()
        logger.info("Discord bot is sending article.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        print("\r[-] Bot finished ", end="", flush=True)
        print(" ", flush=True)  # Clear the line


def send_text(text: str):
    embed = {"description": text, "color": 0x00FF00}
    payload = {"embeds": [embed]}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    response.raise_for_status()


if __name__ == "__main__":
    locally = 1
    main(debug=0)

    # Input SQL-query with data here:
    # send_discord_message(webhook_url=DISCORD_WEBHOOK_URL, sender_name="Alexnet", title="test", published_date="2023-12-12", summary='normal', article_link='none')
