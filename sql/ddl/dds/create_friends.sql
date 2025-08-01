CREATE TABLE IF NOT EXISTS dds.friends (
    user_id VARCHAR NOT NULL,
    friend_id VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, friend_id)
);
