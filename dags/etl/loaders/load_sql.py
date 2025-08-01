import os
import psycopg2
from etl.config import get_postgres_config

def load_sql(query_file, subdir="raw"):
    base_sql_dir = os.environ.get("SQL_DIR", "/opt/airflow/sql")
    sql_dir = os.path.join(base_sql_dir, "dml", subdir)
    path = os.path.join(sql_dir, query_file)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"SQL-файл не найден: {path}")
    with open(path, encoding='utf-8') as f:
        return f.read()
