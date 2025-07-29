CREATE TABLE IF NOT EXISTS raw.posts (
    post_id UUID PRIMARY KEY,
    user_id UUID,
    text TEXT,
    created_at TIMESTAMP
);
