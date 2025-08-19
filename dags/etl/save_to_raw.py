import json

import psycopg2

from dags.etl.config import get_postgres_config
from dags.etl.loaders_utils.load_sql import load_sql

_sql_cache = {}
_sql_map = {
    "user": "insert_raw_user.sql",
    "post": "insert_raw_post.sql",
    "comment": "insert_raw_comment.sql",
    "like": "insert_raw_like.sql",
    "reaction": "insert_raw_reaction.sql",
    "community": "insert_raw_community.sql",
    "media": "insert_raw_media.sql",
    "pinned_post": "insert_raw_pinned_post.sql",
    "friend": "insert_raw_friend.sql",
    "group_member": "insert_raw_group_member.sql",
}

def _get_sql(event_type):
    fname = _sql_map[event_type]
    if fname not in _sql_cache:
        # поправь layer/subdir под свою структуру, если нужно
        _sql_cache[fname] = load_sql(fname, layer="dml", subdir="raw")
    return _sql_cache[fname]

def save_to_raw(event, event_type):
    cfg = get_postgres_config()
    with psycopg2.connect(**cfg) as conn, conn.cursor() as cur:
        if event_type not in _sql_map:
            print(f"[WARN] Unknown event type for RAW: {event_type}")
            return
        sql = _get_sql(event_type)
        cur.execute(sql, {"event_json": json.dumps(event)})

def save_to_raw_bulk(event_type, events, cur):
    """
    Быстрый путь: одна подготовленная вставка + executemany.
    SQL из твоих файлов остаётся прежним, параметр один: event_json.
    """
    if not events:
        return
    if event_type not in _sql_map:
        print(f"[WARN] Unknown event type for RAW: {event_type}")
        return
    sql = _get_sql(event_type)
    params = [{"event_json": json.dumps(e)} for e in events]
    cur.executemany(sql, params)
