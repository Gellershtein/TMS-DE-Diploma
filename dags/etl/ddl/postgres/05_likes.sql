CREATE TABLE IF NOT EXISTS raw.likes (
    like_id UUID PRIMARY KEY,
    user_id UUID,
    target_type TEXT,
    target_id UUID,
    created_at TIMESTAMP
);
