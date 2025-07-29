
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "data_generator"))
from generate_events import generate_to_kafka, generate_to_minio

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=30)
}

with DAG(
    dag_id="DATA_GENERATOR_to_kafka_and_minio",
    default_args=default_args,
    schedule_interval="* * * * *", #генерируем данные каждую минуту
    start_date=datetime(2024, 7, 28),
    catchup=False
) as dag:

    kafka_task = PythonOperator(
        task_id="generate_kafka_events",
        python_callable=generate_to_kafka,
    )

    minio_task = PythonOperator(
        task_id="generate_minio_batch",
        python_callable=generate_to_minio,
    )

    kafka_task >> minio_task