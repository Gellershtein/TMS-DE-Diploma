CREATE TABLE IF NOT EXISTS dds.media (
    media_id VARCHAR PRIMARY KEY,
    media_type VARCHAR NOT NULL,
    url TEXT NOT NULL,
    attached_to_post VARCHAR,
    created_at TIMESTAMP NOT NULL
);
