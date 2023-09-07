from datetime import datetime

from airflow import DAG
from airflow.decorators import dag, task

from newsfeed.create_table import create_table
from newsfeed.download_blogs_from_rss import main as main_rss
from newsfeed.extract_articles import main as main_extract


@task(task_id="start")
def start_task() -> None:
    print("Starting pipeline...")


@task(task_id="join")
def join_task() -> None:
    print("Joining tasks...")


@task(task_id="end")
def end_task() -> None:
    print("Ending pipeline...")


@task(task_id="create_table")
def create_table_task() -> None:
    print("Running create_table...")
    create_table()


@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    print("Running download_blogs_from_rss...")
    main_rss("mit")
    main_rss("ts")


@task(task_id="extract_articles")
def extract_articles_task() -> None:
    print("Running extract_articles...")
    main_extract("mit")
    main_extract("ts")


@dag(
    dag_id="test_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def test_pipeline() -> None:
    start_task() >> create_table_task() >> download_blogs_from_rss_task() >> extract_articles_task()


test_pipeline()
