CREATE TABLE IF NOT EXISTS dds.posts (
    post_id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);
