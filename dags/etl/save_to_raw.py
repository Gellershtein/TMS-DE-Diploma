import psycopg2
import json
from etl.config import get_postgres_config
from etl.loaders.load_sql import load_sql

def save_to_raw(event, event_type):
    config = get_postgres_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    sql_map = {
        "user": "insert_raw_user.sql",
        "post": "insert_raw_post.sql",
        "comment": "insert_raw_comment.sql",
        "like": "insert_raw_like.sql",
        "reaction": "insert_raw_reaction.sql",
        "community": "insert_raw_community.sql",
        "media": "insert_raw_media.sql",
        "pinned_post": "insert_raw_pinned_post.sql",
        "friend": "insert_raw_friend.sql",
        "group_member": "insert_raw_group_member.sql"
    }
    if event_type not in sql_map:
        print(f"[WARN] Unknown event type for RAW: {event_type}")
        cur.close()
        conn.close()
        return
    sql = load_sql(sql_map[event_type])
    cur.execute(sql, {"event_json": json.dumps(event)})
    conn.commit()
    cur.close()
    conn.close()
