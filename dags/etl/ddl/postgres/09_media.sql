CREATE TABLE IF NOT EXISTS raw.media (
    media_id UUID PRIMARY KEY,
    media_type TEXT,
    url TEXT,
    attached_to_post UUID,
    created_at TIMESTAMP
);

