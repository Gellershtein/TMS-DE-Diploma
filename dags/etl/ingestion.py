import json
import time
from collections import defaultdict

import psycopg2
from kafka import KafkaConsumer
from minio import Minio

from dags.etl.config import (
    get_kafka_bootstrap_servers,
    get_minio_endpoint, get_minio_access_key, get_minio_secret_key,
    get_minio_bucket, get_minio_use_ssl, get_postgres_config
)
from dags.etl.save_to_raw import save_to_raw, save_to_raw_bulk

RAW_ENTITY_TYPES = {
    "user", "post", "comment", "like", "reaction",
    "community", "media", "pinned_post", "friend", "group_member"
}

def ingest_from_kafka_topics(topics, batch_size=2000, flush_sec=5, idle_sec=8, group_id="raw-loader"):
    """
    Читает один или несколько топиков, буферизует события по типу, пишет батчами в RAW
    и коммитит оффсеты после успешной записи.
    Завершается, если нет новых сообщений idle_sec секунд.
    """
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=get_kafka_bootstrap_servers(),
        group_id=group_id,
        enable_auto_commit=False,                 # сами коммитим после записи
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        max_poll_records=batch_size,
        fetch_max_bytes=50 * 1024 * 1024,
        fetch_min_bytes=1 * 1024 * 1024,
        fetch_max_wait_ms=500,
    )

    pg = get_postgres_config()
    conn = psycopg2.connect(**pg)
    cur = conn.cursor()

    buffers = defaultdict(list)
    last_flush = time.time()
    last_seen = time.time()

    def flush():
        # батчевые вставки по типу события
        for etype, rows in list(buffers.items()):
            if not rows:
                continue
            if etype in RAW_ENTITY_TYPES:
                save_to_raw_bulk(etype, rows, cur)   # executemany под капотом
            buffers[etype].clear()
        conn.commit()
        consumer.commit()

    try:
        while True:
            polled = consumer.poll(timeout_ms=1000, max_records=batch_size)
            if not polled:
                # если пусто достаточно долго — выходим; DAG запустит нас снова
                if time.time() - last_seen > idle_sec:
                    break
                continue

            last_seen = time.time()

            for _, msgs in polled.items():
                for m in msgs:
                    v = m.value
                    etype = v.get("type")
                    if etype:
                        buffers[etype].append(v)

            if time.time() - last_flush >= flush_sec:
                flush()
                last_flush = time.time()

        # финальный сброс
        if any(buffers.values()):
            flush()
    finally:
        try:
            cur.close()
            conn.close()
        finally:
            consumer.close()

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
        if event_type in RAW_ENTITY_TYPES:
            save_to_raw(event, event_type)

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
            if event_type in RAW_ENTITY_TYPES:
                save_to_raw(event, event_type)
        # (опционально) удалять объект после обработки:
        minio_client.remove_object(bucket, obj.object_name)
