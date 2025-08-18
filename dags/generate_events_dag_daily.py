from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os, sys
from dags.etl.utils.telegram_notifier import telegram_notifier

sys.path.append(os.path.join(os.path.dirname(__file__), "data_generator"))
from generate_events import generate_to_kafka, generate_to_minio, generate_all_data_and_return

default_args = {"owner": "airflow", "retries": 3, "retry_delay": timedelta(seconds=30),"on_failure_callback": telegram_notifier}

with DAG(
    dag_id="1_DATA_GENERATOR_daily",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 7, 1),
    catchup=True,
    max_active_runs=1,
    tags=["generator", "raw", "minio", "kafka"],
) as dag:

    generate_data = PythonOperator(
        task_id="generate_data",
        python_callable=generate_all_data_and_return,
        op_kwargs={"day": "{{ ds }}"}   # <- ключ: передаём дату запуска 'YYYY-MM-DD'
    )

    kafka_task = PythonOperator(
        task_id="generate_kafka_events",
        python_callable=generate_to_kafka,
    )

    minio_task = PythonOperator(
        task_id="generate_minio_batch",
        python_callable=generate_to_minio,
        op_kwargs={"day": "{{ ds }}"}
    )

    # «Слип» на 2 минуты
    throttle_2m = BashOperator(
        task_id="throttle_2m",
        bash_command="sleep 120"
    )

    generate_data >> [kafka_task, minio_task]
    [kafka_task, minio_task] >> throttle_2m
