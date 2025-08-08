-- :as_of_date приходит из Python как date (psycopg2: %(as_of_date)s)
WITH
bounds AS (
    SELECT
        %(as_of_date)s::date                             AS d0,               -- начало дня
        (%(as_of_date)s::date + INTERVAL '1 day')        AS d1,               -- конец дня (не включая)
        (%(as_of_date)s::date - INTERVAL '6 days')       AS w0                -- начало окна 7 дней
),
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
    -- DAU: уникальные юзеры, у кого есть действие за день [d0, d1)
    SELECT DISTINCT p.user_id
    FROM dds.posts p, bounds b
    WHERE p.created_at >= b.d0 AND p.created_at < b.d1
    UNION ALL
    SELECT DISTINCT c.user_id
    FROM dds.comments c, bounds b
    WHERE c.created_at >= b.d0 AND c.created_at < b.d1
    UNION ALL
    SELECT DISTINCT r.user_id
    FROM dds.reactions r, bounds b
    WHERE r.created_at >= b.d0 AND r.created_at < b.d1
),
active_w AS (
    -- WAU: уникальные юзеры, у кого есть действие за 7 дней [w0, d1)
    SELECT DISTINCT p.user_id
    FROM dds.posts p, bounds b
    WHERE p.created_at >= b.w0 AND p.created_at < b.d1
    UNION ALL
    SELECT DISTINCT c.user_id
    FROM dds.comments c, bounds b
    WHERE c.created_at >= b.w0 AND c.created_at < b.d1
    UNION ALL
    SELECT DISTINCT r.user_id
    FROM dds.reactions r, bounds b
    WHERE r.created_at >= b.w0 AND r.created_at < b.d1
)
SELECT
    (SELECT d0 FROM bounds)::date                                      AS dt,
    (SELECT c FROM posts_cnt)                                          AS total_posts,
    (SELECT c FROM comments_cnt)                                       AS total_comments,
    (SELECT c FROM reactions_cnt)                                      AS total_reactions,
    ((SELECT c FROM comments_cnt) + (SELECT c FROM reactions_cnt))::float
        / NULLIF((SELECT c FROM posts_cnt), 0)                         AS interactions_per_post,
    (SELECT COUNT(*) FROM active_d)                                    AS dau,
    (SELECT COUNT(*) FROM active_w)                                    AS wau,
    (SELECT COUNT(*) FROM active_d)::float
        / NULLIF((SELECT COUNT(*) FROM active_w), 0)                   AS dau_wau_ratio;
