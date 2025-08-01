CREATE TABLE IF NOT EXISTS dds.group_members (
    community_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    PRIMARY KEY (community_id, user_id)
);
