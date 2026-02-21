from supabase import create_client, Client
from app.config import settings
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json


class DatabaseService:
    """Supabase 數據庫服務"""
    
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
    
    async def create_link(self, link_data: Dict) -> Dict:
        """創建新連結"""
        result = self.client.table('links').insert(link_data).execute()
        return result.data[0] if result.data else None
    
    async def get_links(
        self,
        limit: int = 50,
        offset: int = 0,
        category: Optional[str] = None,
        reviewed: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Dict]:
        """获取链接列表"""
        query = self.client.table('links').select('*')
        
        if category:
            query = query.eq('ai_category', category)
        
        if reviewed is not None:
            query = query.eq('reviewed', reviewed)
        
        if search:
            # 多字段搜索：先獲取數據，然後在 Python 中過濾
            # 這樣可以搜索 title, description, summary, domain, ai_category, ai_tags
            search_lower = search.lower()
            all_results = query.execute()
            filtered_results = []
            
            for link in (all_results.data if all_results.data else []):
                # 檢查多個字段
                title = (link.get('title') or '').lower()
                description = (link.get('description') or '').lower()
                summary = (link.get('summary') or '')
                summary = summary.lower() if summary else ''
                domain = (link.get('domain') or '').lower()
                category = (link.get('ai_category') or '').lower()
                tags = link.get('ai_tags', [])
                tags_str = ' '.join([str(t).lower() for t in tags if t]).lower()
                
                # 如果任何字段包含搜索關鍵詞
                if (search_lower in title or 
                    search_lower in description or 
                    search_lower in summary or
                    search_lower in domain or 
                    search_lower in category or
                    search_lower in tags_str):
                    filtered_results.append(link)
            
            # 按創建時間排序並限制數量
            filtered_results.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            result_data = filtered_results[:limit]
            
            # 創建一個模擬的結果對象
            class MockResult:
                def __init__(self, data):
                    self.data = data
            
            return MockResult(result_data).data
        
        query = query.order('created_at', desc=True).limit(limit).offset(offset)
        
        result = query.execute()
        return result.data if result.data else []
    
    async def get_link_by_id(self, link_id: str) -> Optional[Dict]:
        """根據 ID 獲取連結"""
        result = self.client.table('links').select('*').eq('id', link_id).execute()
        return result.data[0] if result.data else None
    
    async def update_link(self, link_id: str, update_data: Dict) -> Dict:
        """更新連結"""
        result = self.client.table('links').update(update_data).eq('id', link_id).execute()
        return result.data[0] if result.data else None
    
    async def delete_link(self, link_id: str) -> bool:
        """刪除連結"""
        result = self.client.table('links').delete().eq('id', link_id).execute()
        return True
    
    async def get_weekly_stats(self, week_start: Optional[datetime] = None) -> Dict:
        """獲取週統計"""
        if not week_start:
            # 獲取本週的開始（週一）
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
        
        week_end = week_start + timedelta(days=7)
        
        # 獲取本週的連結
        result = self.client.table('links')\
            .select('*')\
            .gte('created_at', week_start.isoformat())\
            .lt('created_at', week_end.isoformat())\
            .execute()
        
        links = result.data if result.data else []
        
        # 統計
        total_links = len(links)
        unique_domains = len(set(link.get('domain') for link in links))
        unique_sources = len(set(link.get('source_app') for link in links if link.get('source_app')))
        
        # 分類分布
        category_distribution = {}
        for link in links:
            category = link.get('ai_category', '其他')
            category_distribution[category] = category_distribution.get(category, 0) + 1
        
        # 來源分布
        source_distribution = {}
        for link in links:
            source = link.get('source_app', 'unknown')
            source_distribution[source] = source_distribution.get(source, 0) + 1
        
        # 域名統計
        domain_count = {}
        for link in links:
            domain = link.get('domain', '')
            domain_count[domain] = domain_count.get(domain, 0) + 1
        top_domains = sorted(domain_count.items(), key=lambda x: x[1], reverse=True)[:10]
        top_domains = [domain for domain, _ in top_domains]
        
        # 最重要的連結（按 importance_score）
        top_links = sorted(
            links,
            key=lambda x: x.get('importance_score', 0),
            reverse=True
        )[:5]
        
        return {
            'week_start': week_start.isoformat(),
            'total_links': total_links,
            'unique_domains': unique_domains,
            'unique_sources': unique_sources,
            'category_distribution': category_distribution,
            'source_distribution': source_distribution,
            'top_domains': top_domains,
            'top_links': top_links
        }

