CREATE TABLE IF NOT EXISTS dds.comments (
    comment_id VARCHAR PRIMARY KEY,
    post_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);
