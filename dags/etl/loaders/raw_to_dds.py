import psycopg2
from data_generator.models import User, Friend, Post, Comment, Like, Reaction, Community, GroupMember, Media, PinnedPost
from etl.loaders.save_to_dds import save_to_dds
from etl.config import get_postgres_config

# Маппинг: сущность → Pydantic модель → таблица

ENTITY_META = {
    "user":      {"model": User,      "table": "users"},
    "friend":    {"model": Friend,    "table": "friends"},
    "post":      {"model": Post,      "table": "posts"},
    "comment":   {"model": Comment,   "table": "comments"},
    "like":      {"model": Like,      "table": "likes"},
    "reaction":  {"model": Reaction,  "table": "reactions"},
    "community": {"model": Community, "table": "communities"},
    "group_member": {"model": GroupMember, "table": "group_members"},
    "media":     {"model": Media,     "table": "media"},
    "pinned_post": {"model": PinnedPost, "table": "pinned_posts"},
}


def process_raw_entity(entity_type):
    config = get_postgres_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    meta = ENTITY_META[entity_type]
    table = meta["table"]
    Model = meta["model"]
    cur.execute(f"SELECT event_json FROM raw.{table}")
    rows = cur.fetchall()
    valid = 0
    errors = 0
    for row in rows:
        try:
            raw = row[0]
            # Если jsonb → dict, если text → str
            if isinstance(raw, dict):
                data = Model.parse_obj(raw)
            else:
                data = Model.parse_raw(raw)
            save_to_dds(data.dict(), entity_type)
            valid += 1
        except Exception as e:
            errors += 1
            print(f"[ERROR] Invalid {entity_type}: {e}")
    print(f"{entity_type}: OK {valid}, ERRORS {errors}")
    cur.close()
    conn.close()


def process_all_entities():
    for entity_type in ENTITY_META:
        process_raw_entity(entity_type)

