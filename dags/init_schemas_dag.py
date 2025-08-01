from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
from dags.etl.init_schemas_postgres import run_sql_files
from dags.etl.init_schemas_neo4j import run_cypher_files
from dags.etl.create_database import create_database

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

default_args = {
    'start_date': datetime(2024, 7, 29)
}

with DAG(
    dag_id='INIT_RAW_and_DDS_schemas',
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["ddl", "init", "raw", "dds", "postgres", "neo4j"],
) as dag:

    # 0. Postgres: Создание базы DWH
    create_dwh_database = PythonOperator(
        task_id='create_dwh_database',
        python_callable=create_database
    )

    # 1. Postgres: Инициализация RAW и DDS схем
    init_pg_schemas = PythonOperator(
        task_id='init_postgres_schemas',
        python_callable=run_sql_files,
        op_args=[os.path.join(BASE, "sql", "ddl", "init_schemas.sql")]
    )

    # 2. Postgres: Создание таблиц в RAW схеме
    create_raw_tables = PythonOperator(
        task_id='create_raw_tables',
        python_callable=run_sql_files,
        op_args=[os.path.join(BASE, "sql", "ddl", "raw")]
    )

    # 3. Postgres: Создание таблиц в DDS схеме
    create_dds_tables = PythonOperator(
        task_id='create_dds_tables',
        python_callable=run_sql_files,
        op_args=[os.path.join(BASE, "sql", "ddl", "dds")]
    )

    # 4. Neo4j: создание констрейнтов
    create_neo4j_constraints = PythonOperator(
        task_id='create_neo4j_constraints',
        python_callable=run_cypher_files,
        op_args=[os.path.join(BASE, "cypher", "ddl")]
    )

    # Граф выполнения
    create_dwh_database >> init_pg_schemas >> create_raw_tables >> create_dds_tables
    [create_raw_tables, create_dds_tables] >> create_neo4j_constraints
