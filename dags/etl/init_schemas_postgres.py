import os
import psycopg2
from dags.etl.config import get_postgres_config

def run_sql_files(folder):
    config = get_postgres_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    files = sorted(os.listdir(folder))
    for file in files:
        if not file.endswith('.sql'):
            continue
        with open(os.path.join(folder, file), encoding='utf-8') as f:
            sql = f.read()
            print(f"Running {file}...")
            cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    run_sql_files(os.path.join(os.path.dirname(__file__), "ddl", "postgres"))
