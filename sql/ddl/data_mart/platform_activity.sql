CREATE TABLE IF NOT EXISTS data_mart.platform_activity
(
    date          Date,
    posts_cnt     UInt64,
    comments_cnt  UInt64,
    reactions_cnt UInt64,
    interactions_per_post Float64
)
ENGINE = MergeTree
ORDER BY date;
