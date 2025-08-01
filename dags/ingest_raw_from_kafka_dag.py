from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl.ingestion import ingest_from_kafka

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ingest_raw_from_kafka_dag",
    default_args=default_args,
    start_date=datetime(2024, 7, 29),
    schedule_interval="*/2 * * * *",  # каждые 2 минуты
    catchup=False,
    tags=["diploma", "raw", "ingest", "kafka"],
) as dag:

    ingest_kafka = PythonOperator(
        task_id="ingest_from_kafka",
        python_callable=ingest_from_kafka,
        dag=dag,
    )

