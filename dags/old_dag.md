```py
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator

from newsfeed import *


## ↓↓☻ PLACEHOLDER FUNCTIONS ↓↓☻ ##
def get_blog_type(**kwargs):
    pass


def download_blogs_from_rss(**kwargs):
    pass


def extract_articles(**kwargs):
    pass


def blog_scraper(**kwargs):
    pass


def create_table(**kwargs):
    pass


def data_parser(**kwargs):
    pass


def summary_parser(**kwargs):
    pass


def discord(**kwargs):
    pass


def app(**kwargs):
    pass


## ↑↑☻ PLACEHOLDER FUNCTIONS ↑↑☻ ##


# Function to choose the branch
def choose_branch(**kwargs):
    # Implement your logic here
    blog_type = get_blog_type()  # your function to determine blog type
    if blog_type == "XML blogs":
        return "download_blogs_from_rss"
    if blog_type == "web_scrape blogs":
        return "blog_scraper"


# Default Args
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 8, 29),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "my_complex_dag",
    default_args=default_args,
    description="A complex DAG with conditional tasks",
    schedule_interval=timedelta(days=1),
)

start = EmptyOperator(
    task_id="start",
    dag=dag,
)

create_table = PythonOperator(
    task_id="create_table",
    python_callable=create_table,
    dag=dag,
)

choose_branch_task = BranchPythonOperator(
    task_id="choose_branch",
    python_callable=choose_branch,
    provide_context=True,
    dag=dag,
)

download_blogs_from_rss_task = PythonOperator(
    task_id="download_blogs_from_rss",
    python_callable=download_blogs_from_rss,
    dag=dag,
)

extract_articles_task = PythonOperator(
    task_id="extract_articles",
    python_callable=extract_articles,
    dag=dag,
)

blog_scraper_task = PythonOperator(
    task_id="blog_scraper",
    python_callable=blog_scraper,
    dag=dag,
)

data_parser_task = PythonOperator(
    task_id="data_parser",
    python_callable=data_parser,
    dag=dag,
)

summary_parser_task = PythonOperator(
    task_id="summary_parser",
    python_callable=summary_parser,
    dag=dag,
)

discord_task = PythonOperator(
    task_id="discord",
    python_callable=discord,
    dag=dag,
)

app_task = PythonOperator(
    task_id="app",
    python_callable=app,
    dag=dag,
)


join = EmptyOperator(
    task_id="join",
    dag=dag,
)

end = EmptyOperator(
    task_id="end",
    dag=dag,
)

start >> create_table >> choose_branch_task
choose_branch_task >> download_blogs_from_rss_task >> extract_articles_task
choose_branch_task >> blog_scraper_task
extract_articles_task >> join
blog_scraper_task >> join
join >> data_parser_task
data_parser_task >> discord_task >> end
data_parser_task >> app_task >> end




from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator

from newsfeed import download_blogs_from_rss, extract_articles, blog_scraper, create_table
from datetime import datetime


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
```




```py

## WORKS

from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import download_blogs_from_rss, create_table, data_parser


@task(task_id="hello")
def hello_task() -> None:
    print("HELLO suuup")


@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main(blog_name="mit")


@dag(
    dag_id="test_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def test_pipeline() -> None:
    # hello_task() >> download_blogs_from_rss_task()
    hello_task()
    download_blogs_from_rss_task()


# register DAG
test_pipeline()
```