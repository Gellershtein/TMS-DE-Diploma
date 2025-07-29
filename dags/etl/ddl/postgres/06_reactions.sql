CREATE TABLE IF NOT EXISTS raw.reactions (
    reaction_id UUID PRIMARY KEY,
    user_id UUID,
    target_type TEXT,
    target_id UUID,
    reaction TEXT,
    created_at TIMESTAMP
);
