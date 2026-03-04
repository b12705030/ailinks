from openai import OpenAI
from typing import Dict, List, Optional
from app.config import settings
import json


class AIClassifier:
    """AI 分類服務"""
    
    CATEGORIES = [
        "娛樂", "學習", "工作", "購物", "食譜", "健身", "旅遊", "靈感", "其他"
    ]
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def classify(self, url: str, title: Optional[str], description: Optional[str], domain: str) -> Dict:
        """
        對連結進行 AI 分類
        返回: category, tags, summary, importance_score, short_name
        """
        # 第一層：規則分類（快速）
        rule_category = self._rule_based_classify(domain, url, title)
        
        # 第二層：LLM 語義分類（精準）
        llm_result = await self._llm_classify(url, title, description, domain, rule_category)
        
        # 第三層：生成簡短易識別的名稱
        short_name = await self._generate_short_name(
            url=url,
            title=title,
            description=description,
            domain=domain,
            category=llm_result.get('category', rule_category),
            tags=llm_result.get('tags', [])
        )
        
        return {
            'ai_category': llm_result.get('category', rule_category),
            'ai_tags': llm_result.get('tags', []),
            'summary': llm_result.get('summary', ''),
            'importance_score': llm_result.get('importance_score', 50),
            'short_name': short_name
        }
    
    def _rule_based_classify(self, domain: str, url: str, title: Optional[str]) -> str:
        """基於規則的快速分類"""
        domain_lower = domain.lower()
        url_lower = url.lower()
        title_lower = (title or '').lower()
        
        # YouTube / 視頻 → 娛樂
        if any(x in domain_lower for x in ['youtube', 'youtu.be', 'bilibili', 'tiktok']):
            return "娛樂"
        
        # 購物平台 → 購物
        if any(x in domain_lower for x in ['shopee', 'amazon', 'momo', 'pchome']):
            return "購物"
        
        # 學習平台
        if any(x in domain_lower for x in ['coursera', 'udemy', 'khan', 'medium', 'substack']):
            return "學習"
        
        # 食譜相關
        if any(x in title_lower + url_lower for x in ['recipe', '食譜', '料理', 'cooking', 'food']):
            return "食譜"
        
        # 健身相關
        if any(x in title_lower + url_lower for x in ['fitness', 'workout', '健身', '運動', 'exercise']):
            return "健身"
        
        # 旅遊相關
        if any(x in title_lower + url_lower for x in ['travel', 'trip', '旅遊', '旅行', 'hotel', 'airbnb']):
            return "旅遊"
        
        return "其他"
    
    async def _llm_classify(self, url: str, title: Optional[str], description: Optional[str], domain: str, rule_category: str) -> Dict:
        """使用 LLM 進行語義分類"""
        try:
            content = f"""
請分析以下連結並分類：

URL: {url}
標題: {title or '無'}
描述: {description or '無'}
域名: {domain}
初步分類: {rule_category}

請以 JSON 格式返回：
{{
    "category": "分類（從以下選擇：娛樂、學習、工作、購物、食譜、健身、旅遊、靈感、其他）",
    "tags": ["標籤1", "標籤2", "標籤3"],
    "summary": "1-2句簡短摘要",
    "importance_score": 0-100的整數（判斷這個連結是否值得稍後閱讀，100=非常重要，0=純娛樂）
}}

只返回 JSON，不要其他文字。
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一個專業的連結分類助手。請根據連結內容進行準確分類。"},
                    {"role": "user", "content": content}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # 驗證 category
            if result.get('category') not in self.CATEGORIES:
                result['category'] = rule_category
            
            # 確保 tags 是列表
            if not isinstance(result.get('tags'), list):
                result['tags'] = []
            
            # 確保 importance_score 在 0-100
            importance = result.get('importance_score', 50)
            if not isinstance(importance, int):
                importance = 50
            result['importance_score'] = max(0, min(100, importance))
            
            return result
            
        except Exception as e:
            print(f"LLM classification error: {e}")
            # 失敗時返回規則分類結果
            return {
                'category': rule_category,
                'tags': [],
                'summary': '',
                'importance_score': 50
            }
    
    async def _generate_short_name(
        self, 
        url: str, 
        title: Optional[str], 
        description: Optional[str], 
        domain: str,
        category: str,
        tags: List[str]
    ) -> str:
        """
        生成簡短易識別的名稱（4-8個字）
        例如："暖心小說"、"Python教學"、"美食料理"
        """
        try:
            # 如果有 tags，優先使用 tags 組合
            if tags and len(tags) > 0:
                # 選擇最相關的1-2個標籤
                relevant_tags = tags[:2]
                combined = ''.join(relevant_tags)
                if len(combined) <= 8:
                    return combined
            
            # 使用 LLM 生成簡短名稱
            content = f"""
請為以下連結生成一個簡短易識別的名稱（4-8個字），讓人一眼就能看出這是什麼內容：

URL: {url}
標題: {title or '無'}
描述: {description or '無'}
分類: {category}
標籤: {', '.join(tags) if tags else '無'}

要求：
1. 名稱要簡短（4-8個字）
2. 要能一眼看出內容類型（例如：溫馨故事、小說、學習網站、教學影片等）
3. 不要使用分類名稱（如"學習"、"娛樂"），要用更具體的描述
4. 只返回名稱，不要其他文字

範例：
- "YouTube 美食料理頻道" → "美食料理"
- "Python 程式設計教學" → "Python教學"
- "溫馨的愛情小說推薦" → "暖心小說"
- "健身運動教學網站" → "健身教學"
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一個專業的內容命名助手。請根據連結內容生成簡短易識別的名稱。"},
                    {"role": "user", "content": content}
                ],
                temperature=0.5,
                max_tokens=20
            )
            
            short_name = response.choices[0].message.content.strip()
            # 移除可能的引號或標點
            short_name = short_name.strip('"\'「」『』【】')
            # 限制長度
            if len(short_name) > 8:
                short_name = short_name[:8]
            
            return short_name if len(short_name) >= 2 else self._fallback_short_name(title, domain, category)
            
        except Exception as e:
            print(f"Short name generation error: {e}")
            return self._fallback_short_name(title, domain, category)
    
    def _fallback_short_name(self, title: Optional[str], domain: str, category: str) -> str:
        """後備方案：從標題或域名生成簡短名稱"""
        if title:
            # 移除常見的無意義詞
            clean_title = title.replace('【', '').replace('】', '').replace('《', '').replace('》', '')
            clean_title = clean_title.replace('「', '').replace('」', '').replace('(', '').replace(')', '')
            # 取前6個字
            if len(clean_title) >= 2:
                return clean_title[:6]
        
        # 使用域名
        clean_domain = domain.replace('www.', '').replace('m.', '').split('.')[0]
        if len(clean_domain) >= 2:
            return clean_domain[:6]
        
        # 最後使用分類
        return category[:4] if category else "連結"
    
    async def generate_weekly_report(self, stats: Dict, top_links: List[Dict]) -> str:
        """生成週報的 AI 分析"""
        try:
            content = f"""
請分析以下一週的連結收集數據：

總連結數: {stats.get('total_links', 0)}
分類分布: {json.dumps(stats.get('category_distribution', {}), ensure_ascii=False)}
來源分布: {json.dumps(stats.get('source_distribution', {}), ensure_ascii=False)}
最常訪問的域名: {', '.join(stats.get('top_domains', [])[:5])}

請用 2-3 句話分析用戶的興趣趨勢，並給出建議。
語氣要輕鬆友好，像朋友聊天一樣。
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一個貼心的個人助手，幫助用戶分析他們的連結收集習慣。"},
                    {"role": "user", "content": content}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Weekly report generation error: {e}")
            return "本週收集了一些有趣的連結，記得找時間回看哦！"

