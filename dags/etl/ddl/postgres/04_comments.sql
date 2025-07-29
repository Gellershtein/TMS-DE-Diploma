CREATE TABLE IF NOT EXISTS raw.comments (
    comment_id UUID PRIMARY KEY,
    post_id UUID,
    user_id UUID,
    text TEXT,
    created_at TIMESTAMP
);
