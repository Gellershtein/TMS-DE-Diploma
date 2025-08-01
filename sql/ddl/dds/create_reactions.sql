CREATE TABLE IF NOT EXISTS dds.reactions (
    reaction_id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    target_type VARCHAR NOT NULL,
    target_id VARCHAR NOT NULL,
    reaction VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL
);
