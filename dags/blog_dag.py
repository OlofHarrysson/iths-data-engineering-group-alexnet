from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import (
    blog_scraper,
    create_table,
    download_blogs_from_rss,
    extract_articles,
)


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
    create_table.main()


@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main(blog_name="mit")
    download_blogs_from_rss.main(blog_name="ts")


@task(task_id="extract_articles")
def extract_articles_task() -> None:
    extract_articles.main(blog_name="mit")
    extract_articles.main(blog_name="ts")


@task(task_id="blog_scraper")
def blog_scraper_task() -> None:
    blog_scraper.main(blog_name="openai")


@dag(
    dag_id="test_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def test_pipeline() -> None:
    start_task() >> create_table()
    create_table() >> download_blogs_from_rss_task() >> extract_articles_task() >> join_task()
    create_table() >> blog_scraper_task() >> join_task()


# register DAG
test_pipeline()
