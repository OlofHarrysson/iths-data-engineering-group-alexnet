import asyncio
import logging
import time
from datetime import datetime

from airflow import DAG
from airflow.decorators import dag, task

import newsfeed
from newsfeed import (
    blog_scraper,
    create_table,
    discord_bot_summary,
    download_blogs_from_rss,
    extract_articles,
)
from newsfeed.discord_bot_summary import (
    send_discord_message,
    send_latest_article,
    send_text,
)

logger = logging.getLogger(__name__)

debug = 0


@task(task_id="start_bot_cycle")
def start_task() -> None:
    if debug:
        discord_bot_summary.send_text("run_bot triggered in Airflow, skipping scraping")

    logger.info("run_bot triggered in Airflow, skipping scraping")


@task(task_id="end")
def end_task() -> None:
    logger.info("Ending pipeline...")


@task(task_id="discord_bot_summary")
def run_discord_summary_task() -> None:
    logger.info("Running discord_bot_summary from DAG")
    # newsfeed.discord_bot_summary.main(debug)
    # newsfeed.discord_bot_summary.check_and_send()
    newsfeed.discord_bot_summary.send_latest_article()


@dag(
    dag_id="run_bot",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def article_summary_pipeline() -> None:
    (start_task() >> run_discord_summary_task() >> end_task())


article_summary_pipeline()
