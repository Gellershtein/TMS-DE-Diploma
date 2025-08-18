from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl.loaders.raw_to_dds import process_raw_entity
from dags.etl.utils.telegram_notifier import telegram_notifier

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(seconds=30),
    "on_failure_callback": telegram_notifier
}

with DAG(
    dag_id="3_RAW_to_DDS_dag",
    default_args=default_args,
    schedule_interval="*/5 * * * *", # запуск каждые 5 минут
    start_date=datetime(2024, 7, 31),
    catchup=False,
    max_active_runs=1,
    tags=["ddl", "dds", "postgres"]
) as dag:
    entity_type = [
        "user", "community",
        "post", "comment", "media",
        "pinned_post", "group_member", "friend",
        "like", "reaction",
    ]

    tasks = {
        entity: PythonOperator(task_id=f"raw_to_dds_{entity}", python_callable=process_raw_entity, op_args=[entity],pool="postgres_dwh")
        for entity in entity_type
    }

    # База
    tasks["user"] >> [tasks["post"], tasks["friend"], tasks["group_member"]]
    tasks["community"] >> [tasks["group_member"], tasks["pinned_post"]]

    # Контент и зависящие
    tasks["post"] >> [tasks["comment"], tasks["media"], tasks["pinned_post"], tasks["like"], tasks["reaction"]]
    tasks["comment"] >> [tasks["like"], tasks["reaction"]]