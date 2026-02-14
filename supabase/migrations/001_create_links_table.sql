-- 創建 links 表
CREATE TABLE IF NOT EXISTS links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT NOT NULL,
    title TEXT,
    description TEXT,
    summary TEXT, -- AI 生成的摘要
    image_url TEXT, -- og:image
    domain TEXT NOT NULL,
    source_app TEXT, -- instagram, facebook, messenger, threads, manual
    content_type TEXT, -- video, article, post, shopping, other
    ai_category TEXT, -- 娛樂, 學習, 工作, 購物, 食譜, 健身, 旅遊, 靈感, 其他
    ai_tags JSONB DEFAULT '[]'::jsonb, -- AI 生成的標籤數組
    importance_score INTEGER DEFAULT 0, -- 0-100, AI 判斷的重要性分數
    reviewed BOOLEAN DEFAULT FALSE, -- 是否已查看
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 創建索引
CREATE INDEX idx_links_created_at ON links(created_at DESC);
CREATE INDEX idx_links_ai_category ON links(ai_category);
CREATE INDEX idx_links_domain ON links(domain);
CREATE INDEX idx_links_reviewed ON links(reviewed);
CREATE INDEX idx_links_importance_score ON links(importance_score DESC);

-- 創建全文搜索索引
CREATE INDEX idx_links_search ON links USING gin(
    to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, '') || ' ' || coalesce(summary, ''))
);

-- 更新時間觸發器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_links_updated_at BEFORE UPDATE ON links
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 創建週報統計視圖
CREATE OR REPLACE VIEW weekly_stats AS
SELECT 
    DATE_TRUNC('week', created_at) as week_start,
    COUNT(*) as total_links,
    COUNT(DISTINCT domain) as unique_domains,
    COUNT(DISTINCT source_app) as unique_sources,
    jsonb_object_agg(
        ai_category, 
        category_count
    ) FILTER (WHERE ai_category IS NOT NULL) as category_distribution
FROM (
    SELECT 
        created_at,
        domain,
        source_app,
        ai_category,
        COUNT(*) OVER (PARTITION BY DATE_TRUNC('week', created_at), ai_category) as category_count
    FROM links
) sub
GROUP BY DATE_TRUNC('week', created_at);

