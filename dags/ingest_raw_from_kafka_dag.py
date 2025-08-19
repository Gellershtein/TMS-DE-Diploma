from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.etl.ingestion import ingest_from_kafka_topics
from dags.etl.utils.telegram_notifier import telegram_notifier

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": telegram_notifier,
}

HEAVY = ["likes", "comments", "reactions", "posts"]
LIGHT = ["users", "friends", "communities", "group_members", "media", "pinned_posts"]

with DAG(
    dag_id="2_INGEST_RAW_FROM_KAFKA",
    default_args=default_args,
    start_date=datetime(2024, 7, 29),
    schedule_interval="*/5 * * * *",  # каждые 5 минуты (чтобы дать времени на догон)
    catchup=False,
    max_active_runs=2,                 # один запуск DAG одновременно
    tags=["diploma", "raw", "ingest", "kafka"],
) as dag:

    # тяжёлые топики — отдельные воркеры (делят партиции)
    heavy_tasks = []
    for topic in HEAVY:
        heavy_tasks.append(
            PythonOperator(
                task_id=f"consume_{topic}",
                python_callable=ingest_from_kafka_topics,
                op_kwargs={"topics": [topic], "batch_size": 2000, "group_id": "raw-loader"},
            )
        )

    # лёгкие — одним воркером
    light_task = PythonOperator(
        task_id="consume_light",
        python_callable=ingest_from_kafka_topics,
        op_kwargs={"topics": LIGHT, "batch_size": 1000, "group_id": "raw-loader"},
    )

    heavy_tasks >> light_task

