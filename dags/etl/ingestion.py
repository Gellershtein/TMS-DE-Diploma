import json
from minio import Minio
from kafka import KafkaConsumer
from dags.etl import save_to_postgres
from dags.etl import save_to_neo4j
from config import (
    get_kafka_bootstrap_servers,
    get_minio_endpoint, get_minio_access_key, get_minio_secret_key,
    get_minio_bucket, get_minio_use_ssl
)

def ingest_from_kafka():
    consumer = KafkaConsumer(
        "users", "friends", "posts", "comments", "likes", "reactions",
        "communities", "group_members", "media", "pinned_posts",
        bootstrap_servers=get_kafka_bootstrap_servers(),
        auto_offset_reset='earliest',
        group_id="airflow-group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=10000,
    )
    for msg in consumer:
        event = msg.value
        event_type = event.get("type")
        # Распределение по типам
        if event_type in {"user", "post", "comment", "like", "reaction", "community", "media", "pinned_post"}:
            save_to_postgres(event, event_type)
        elif event_type in {"friend", "group_member"}:
            save_to_neo4j(event, event_type)

def ingest_from_minio():
    minio_client = Minio(
        get_minio_endpoint(),
        access_key=get_minio_access_key(),
        secret_key=get_minio_secret_key(),
        secure=get_minio_use_ssl(),
    )
    bucket = get_minio_bucket()
    for obj in minio_client.list_objects(bucket, recursive=True):
        data = minio_client.get_object(bucket, obj.object_name).read()
        try:
            events = json.loads(data)
            # Для файла, который содержит список событий, а не одно событие
            if isinstance(events, dict):  # если вдруг объект — одно событие
                events = [events]
        except Exception as e:
            print(f"Ошибка при парсинге файла {obj.object_name}: {e}")
            continue
        for event in events:
            event_type = event.get("type")
            if event_type in {"user", "post", "comment", "like", "reaction", "community", "media", "pinned_post"}:
                save_to_postgres(event, event_type)
            elif event_type in {"friend", "group_member"}:
                save_to_neo4j(event, event_type)
        # (опционально) удалять объект после обработки:
        # minio_client.remove_object(bucket, obj.object_name)
