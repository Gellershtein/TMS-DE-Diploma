CREATE TABLE IF NOT EXISTS raw.users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP
);
