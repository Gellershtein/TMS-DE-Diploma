from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl.loaders.raw_to_dds import process_raw_entity

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=30)
}

with DAG(
    dag_id="RAW_to_DDS_dag",
    default_args=default_args,
    schedule_interval="*/10 * * * *", # запуск каждые 10 минут
    start_date=datetime(2024, 7, 31),
    catchup=False,
    tags=["ddl", "dds", "postgres"]
) as dag:

    for entity_type in [
        "user",
        "friend",
        "post",
        "comment",
        "like",
        "reaction",
        "community",
        "group_member",
        "media",
        "pinned_post"
    ]:
        PythonOperator(
            task_id=f"raw_to_dds_{entity_type}",
            python_callable=process_raw_entity,
            op_args=[entity_type],
        )
