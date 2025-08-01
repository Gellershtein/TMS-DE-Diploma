import os
import psycopg2
from etl.config import get_postgres_config

def create_database(db_name=os.environ.get("POSTGRES_DB")):
    config = get_postgres_config()
    config["dbname"] = "postgres"   # <-- меняем значение, только для создания БД!
    conn = psycopg2.connect(**config)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {db_name};")
    cur.close()
    conn.close()
