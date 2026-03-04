-- 添加 short_name 字段到 links 表
ALTER TABLE links ADD COLUMN IF NOT EXISTS short_name TEXT;

-- 添加索引以便搜索
CREATE INDEX IF NOT EXISTS idx_links_short_name ON links(short_name);

