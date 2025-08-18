from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl.ingestion import ingest_from_minio
from dags.etl.utils.telegram_notifier import telegram_notifier

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": telegram_notifier
}

with DAG(
    dag_id="2_INGEST_RAW_FROM_MINIO",
    default_args=default_args,
    start_date=datetime(2024, 7, 29),
    schedule_interval="*/2 * * * *",  # каждые 5 минут
    catchup=False,
    max_active_runs=1,
    tags=["diploma", "raw", "ingest", "minio"],
) as dag:

    ingest_minio = PythonOperator(
        task_id="ingest_from_minio",
        python_callable=ingest_from_minio
    )
