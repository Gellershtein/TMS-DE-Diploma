from generators import (
    generate_user, generate_friend, generate_post, generate_comment,
    generate_like, generate_reactions, generate_community, generate_group_member,
    generate_media, generate_pinned_post
)
from writer import write_to_kafka, write_to_minio
import random
from datetime import datetime

def parametrised_all_data(
    num_users=10,
    num_communities=2,
    posts_per_user=2,
    comments_per_post=2,
    likes_per_post=2,
    group_memberships=10,
    media_per_post=1,
    pinned_per_community=1,
    num_reactions=40
):
    # Users
    users = [generate_user() for _ in range(num_users)]
    user_ids = [u.user_id for u in users]

    # Communities
    communities = [generate_community() for _ in range(num_communities)]
    community_ids = [c.community_id for c in communities]

    # Friends
    friends = [generate_friend(user_ids) for _ in range(num_users)]

    # Posts
    posts = [generate_post(user_id) for user_id in user_ids for _ in range(posts_per_user)]
    post_ids = [p.post_id for p in posts]

    # Comments
    comments = [generate_comment(random.choice(user_ids), post.post_id) for post in posts for _ in range(comments_per_post)]
    comment_ids = [c.comment_id for c in comments]

    # Likes
    likes = [generate_like(random.choice(user_ids), "post", post.post_id) for post in posts for _ in range(likes_per_post)]

    # Reactions
    reactions = generate_reactions(users, posts, comments, n=num_reactions)

    # Group members
    group_members = [
        generate_group_member(random.choice(community_ids), random.choice(user_ids))
        for _ in range(group_memberships)
    ]

    # Media
    media = [generate_media(random.choice(post_ids)) for _ in range(media_per_post * len(posts))]

    # Pinned posts
    pinned_posts = [generate_pinned_post(random.choice(community_ids), random.choice(post_ids)) for _ in range(pinned_per_community * num_communities)]

    return {
        "users": [u.dict() for u in users],
        "friends": [f.dict() for f in friends],
        "posts": [p.dict() for p in posts],
        "comments": [c.dict() for c in comments],
        "likes": [l.dict() for l in likes],
        "reactions": [r.dict() for r in reactions],
        "communities": [c.dict() for c in communities],
        "group_members": [g.dict() for g in group_members],
        "media": [m.dict() for m in media],
        "pinned_posts": [p.dict() for p in pinned_posts],
    }

def generate_all_data_and_return():
    return parametrised_all_data()

def generate_to_kafka(ti):
    data = ti.xcom_pull(task_ids="generate_data")
    for entity, events in data.items():
        for event in events:
            write_to_kafka(entity, event)

def generate_to_minio(ti):
    data = ti.xcom_pull(task_ids="generate_data")
    events = (
        data["communities"] +
        data["group_members"] +
        data["media"] +
        data["pinned_posts"]
    )
    filename = f"batch_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
    write_to_minio(filename, events)