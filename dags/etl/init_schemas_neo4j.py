import os
from neo4j import GraphDatabase
from dags.etl.config import get_neo4j_config

def run_cypher_files(folder):
    cfg = get_neo4j_config()
    driver = GraphDatabase.driver(cfg["uri"], auth=(cfg["user"], cfg["password"]))
    files = sorted(os.listdir(folder))
    with driver.session() as session:
        for file in files:
            if not file.endswith(".cypher"):
                continue
            with open(os.path.join(folder, file), encoding='utf-8') as f:
                cypher = f.read()
                print(f"Running {file}...")
                session.run(cypher)
    driver.close()

if __name__ == "__main__":
    run_cypher_files(os.path.join(os.path.dirname(__file__), "ddl", "neo4j"))
