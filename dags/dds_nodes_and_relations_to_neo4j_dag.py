from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from dags.etl.loaders.dds_to_neo4j_relations import copy_all_relations
from etl.loaders.dds_to_neo4j_nodes import copy_nodes_to_neo4j
from etl.loaders.dds_to_neo4j_relations import copy_relation_to_neo4j

default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="DDS_to_NEO4J_dag",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=datetime(2024, 7, 30),
    catchup=False,
    tags=["dds", "neo4j"]
) as dag:
    create_nodes = PythonOperator(
        task_id="copy_nodes_to_neo4j",
        python_callable=copy_nodes_to_neo4j
    )

    create_relations = PythonOperator(
        task_id="copy_relations_to_neo4j",
        python_callable=copy_all_relations
    )

    create_nodes >> create_relations

