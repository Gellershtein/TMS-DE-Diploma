CREATE TABLE IF NOT EXISTS dds.pinned_posts (
    community_id VARCHAR NOT NULL,
    post_id VARCHAR NOT NULL,
    PRIMARY KEY (community_id, post_id)
);
