# In your single DAG file

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


# Function1
def function1():
    print("Function 1 executed")


# Function2
def function2():
    print("Function 2 executed")


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

# DAG definition
dag = DAG(
    "my_single_dag",
    default_args=default_args,
    description="My single DAG with multiple tasks",
    schedule_interval=timedelta(days=1),
)

# Task1 for function1
task1 = PythonOperator(
    task_id="function1_task",
    python_callable=function1,
    dag=dag,
)

# Task2 for function2
task2 = PythonOperator(
    task_id="function2_task",
    python_callable=function2,
    dag=dag,
)

# Setting task sequence
task1 >> task2
