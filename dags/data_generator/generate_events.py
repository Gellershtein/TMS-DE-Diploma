
from generators import (
    generate_user, generate_friend, generate_post, generate_comment,
    generate_like, generate_reactions, generate_community, generate_group_member,
    generate_media, generate_pinned_post
)
from writer import write_to_kafka, write_to_minio
import random
from datetime import datetime

def generate_to_kafka():
    users = [generate_user() for _ in range(5)]
    user_ids = [u.user_id for u in users]
    friends = [generate_friend(user_ids) for _ in range(5)]
    posts = [generate_post(user_id) for user_id in user_ids for _ in range(2)]
    comments = [generate_comment(random.choice(user_ids), post.post_id) for post in posts for _ in range(2)]
    likes = [generate_like(random.choice(user_ids), "post", post.post_id) for post in posts for _ in range(2)]

    # Генерируем реакции на посты и на комментарии (70% посты, 30% комментарии)
    reactions = generate_reactions(users, posts, comments, n=40)

    for user in users:
        write_to_kafka("users", user)
    for friend in friends:
        write_to_kafka("friends", friend)
    for post in posts:
        write_to_kafka("posts", post)
    for comment in comments:
        write_to_kafka("comments", comment)
    for like in likes:
        write_to_kafka("likes", like)
    for reaction in reactions:
        write_to_kafka("reactions", reaction)


def generate_to_minio():
    communities = [generate_community() for _ in range(2)]
    community_ids = [c.community_id for c in communities]
    users = [generate_user() for _ in range(10)]
    user_ids = [u.user_id for u in users]
    group_members = [generate_group_member(random.choice(community_ids), random.choice(user_ids)) for _ in range(10)]
    posts = [generate_post(random.choice(user_ids)) for _ in range(5)]
    post_ids = [p.post_id for p in posts]
    media = [generate_media(random.choice(post_ids)) for _ in range(5)]
    pinned_posts = [generate_pinned_post(random.choice(community_ids), random.choice(post_ids)) for _ in range(2)]

    events = communities + group_members + media + pinned_posts
    filename = f"batch_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
    write_to_minio(filename, events)
