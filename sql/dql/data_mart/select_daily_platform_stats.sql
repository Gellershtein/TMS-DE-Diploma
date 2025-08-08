-- :as_of_date передаём из Python (date)
WITH
posts_cnt AS (
    SELECT COUNT(*)::bigint AS c FROM dds.posts
),
comments_cnt AS (
    SELECT COUNT(*)::bigint AS c FROM dds.comments
),
reactions_cnt AS (
    SELECT COUNT(*)::bigint AS c FROM dds.reactions
),
active_d AS (
    SELECT DISTINCT user_id
    FROM (
        SELECT user_id FROM dds.posts     WHERE created_at::date = %(as_of_date)s
        UNION ALL
        SELECT user_id FROM dds.comments  WHERE created_at::date = %(as_of_date)s
        UNION ALL
        SELECT user_id FROM dds.reactions WHERE created_at::date = %(as_of_date)s
    ) t
),
active_w AS (
    SELECT DISTINCT user_id
    FROM (
        SELECT user_id FROM dds.posts     WHERE created_at >= (%(as_of_date)s::date - INTERVAL '6 days')
        UNION ALL
        SELECT user_id FROM dds.comments  WHERE created_at >= (%(as_of_date)s::date - INTERVAL '6 days')
        UNION ALL
        SELECT user_id FROM dds.reactions WHERE created_at >= (%(as_of_date)s::date - INTERVAL '6 days')
    ) t
)
SELECT
    %(as_of_date)s::date                                            AS dt,
    (SELECT c FROM posts_cnt)                                       AS total_posts,
    (SELECT c FROM comments_cnt)                                    AS total_comments,
    (SELECT c FROM reactions_cnt)                                   AS total_reactions,
    ((SELECT c FROM comments_cnt) + (SELECT c FROM reactions_cnt))::float
        / NULLIF((SELECT c FROM posts_cnt), 0)                      AS interactions_per_post,
    (SELECT COUNT(*) FROM active_d)                                 AS dau,
    (SELECT COUNT(*) FROM active_w)                                 AS wau,
    (SELECT COUNT(*) FROM active_d)::float / NULLIF((SELECT COUNT(*) FROM active_w), 0) AS dau_wau_ratio;
