from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl.ingestion import ingest_from_minio

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ingest_raw_from_minio_dag",
    default_args=default_args,
    start_date=datetime(2024, 7, 29),
    schedule_interval="*/5 * * * *",  # каждые 5 минут
    catchup=False,
    tags=["diploma", "raw", "ingest", "minio"],
) as dag:

    ingest_minio = PythonOperator(
        task_id="ingest_from_minio",
        python_callable=ingest_from_minio
    )
