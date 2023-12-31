import asyncio
import logging
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

logger = logging.getLogger(__name__)


@task(task_id="start")
def start_task() -> None:
    logger.info("Starting pipeline...")


@task(task_id="end")
def end_task() -> None:
    logger.info("Ending pipeline...")


@task(task_id="create_table")
def create_table_task() -> None:
    logger.info("Running create_table from DAG")
    newsfeed.create_table.main()


@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    logger.info("Running download_blogs_from_rss from DAG")
    newsfeed.download_blogs_from_rss.main("mit")
    newsfeed.download_blogs_from_rss.main("ts")
    newsfeed.blog_scraper.main()  # OpenAI Blog


@task(task_id="extract_articles")
def extract_articles_task() -> None:
    logger.info("Running extract_articles from DAG")
    newsfeed.extract_articles.main("mit")
    newsfeed.extract_articles.main("ts")


@task(task_id="discord_bot_summary")
def run_discord_summary_task() -> None:
    logger.info("Running discord_bot_summary from DAG")
    asyncio.run(newsfeed.discord_bot_summary.main())


@dag(
    dag_id="article_summary_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def article_summary_pipeline() -> None:
    (
        start_task()
        >> create_table_task()
        >> download_blogs_from_rss_task()
        >> extract_articles_task()
        >> run_discord_summary_task()
        >> end_task()
    )


article_summary_pipeline()
