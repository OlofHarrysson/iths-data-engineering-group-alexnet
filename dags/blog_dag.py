from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator


## ↓↓☻ PLACEHOLDER FUNCTIONS ↓↓☻ ##
def get_blog_type(**kwargs):
    pass


def download_blogs_from_rss(**kwargs):
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
choose_branch_task >> download_blogs_from_rss_task
choose_branch_task >> blog_scraper_task
download_blogs_from_rss_task >> join
blog_scraper_task >> join
join >> data_parser_task >> summary_parser_task
summary_parser_task >> discord_task >> end
summary_parser_task >> app_task >> end
