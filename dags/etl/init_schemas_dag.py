from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dags.etl.init_schemas_postgres import run_sql_files
from dags.etl.init_schemas_neo4j import run_cypher_files
import os

default_args = {
    'start_date': datetime(2024, 7, 29)
}

with DAG(
    dag_id='INIT_schemas',
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["ddl", "raw", "init", "postgres", "neo4j"],
) as dag:

    init_pg = PythonOperator(
        task_id='init_postgres',
        python_callable=run_sql_files,
        op_args=[os.path.join(os.path.dirname(__file__), "ddl", "postgres")]
    )
    init_neo4j = PythonOperator(
        task_id='init_neo4j',
        python_callable=run_cypher_files,
        op_args=[os.path.join(os.path.dirname(__file__), "ddl", "neo4j")]
    )

    init_pg >> init_neo4j
