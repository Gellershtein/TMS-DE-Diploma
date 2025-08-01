CREATE TABLE IF NOT EXISTS dds.likes (
    like_id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    target_type VARCHAR NOT NULL,
    target_id VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL
);
