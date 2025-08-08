from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, date
from etl.loaders.dds_to_clickhouse_metrics import upsert_daily_platform_stats

default_args = {"owner": "airflow", "retries": 0}

with DAG(
    dag_id="MART_daily_platform_stats",
    start_date=datetime(2024, 7, 30),
    schedule_interval="0 0 * * *",  # раз в сутки
    catchup=False,
    tags=["marts","clickhouse"],
) as dag:

    load_daily_stats = PythonOperator(
        task_id="upsert_daily_platform_stats",
        python_callable=lambda: upsert_daily_platform_stats(date.today())
    )
