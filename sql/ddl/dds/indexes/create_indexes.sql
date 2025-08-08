-- Для фильтров по времени
CREATE INDEX IF NOT EXISTS idx_posts_created_at              ON dds.posts (created_at);
CREATE INDEX IF NOT EXISTS idx_comments_created_at           ON dds.comments (created_at);
CREATE INDEX IF NOT EXISTS idx_reactions_created_at          ON dds.reactions (created_at);

-- Для DAU/WAU с distinct по user_id
CREATE INDEX IF NOT EXISTS idx_posts_created_at_user_id      ON dds.posts (created_at, user_id);
CREATE INDEX IF NOT EXISTS idx_comments_created_at_user_id   ON dds.comments (created_at, user_id);
CREATE INDEX IF NOT EXISTS idx_reactions_created_at_user_id  ON dds.reactions (created_at, user_id);
