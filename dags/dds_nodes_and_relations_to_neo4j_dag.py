from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from dags.etl.loaders.dds_to_neo4j_relations import copy_all_relations
from etl.loaders.dds_to_neo4j_nodes import copy_nodes_to_neo4j
from dags.etl.utils.telegram_notifier import telegram_notifier

default_args = {
    "owner": "airflow",
    "retries": 3,
    "on_failure_callback": telegram_notifier
}

with DAG(
    dag_id="4_DDS_to_NEO4J_dag",
    default_args=default_args,
    schedule_interval="*/5 * * * *",
    start_date=datetime(2024, 7, 30),
    catchup=False,
    max_active_runs=1,
    tags=["dds", "neo4j"],
) as dag:
    create_nodes = PythonOperator(
        task_id="copy_nodes_to_neo4j",
        python_callable=copy_nodes_to_neo4j,
        pool="postgres_dwh"
    )

    create_relations = PythonOperator(
        task_id="copy_relations_to_neo4j",
        python_callable=copy_all_relations,
        pool="postgres_dwh"
    )

    create_nodes >> create_relations

