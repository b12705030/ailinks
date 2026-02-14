import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional, Dict
import re
import json


class MetadataExtractor:
    """提取網頁的 metadata"""
    
    @staticmethod
    async def extract(url: str) -> Dict[str, Optional[str]]:
        """
        提取 URL 的 metadata
        返回: title, description, image_url, domain, content_type
        """
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'lxml')
                
                # 提取 domain
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.replace('www.', '')
                
                # 提取 title
                title = None
                
                # 特殊處理 YouTube
                if 'youtube.com' in domain or 'youtu.be' in domain:
                    # 嘗試從 JSON-LD 提取
                    json_ld = soup.find('script', type='application/ld+json')
                    if json_ld:
                        try:
                            data = json.loads(json_ld.string)
                            if isinstance(data, dict):
                                if 'name' in data:
                                    title = data['name']
                                elif '@graph' in data:
                                    for item in data['@graph']:
                                        if item.get('@type') == 'VideoObject' and 'name' in item:
                                            title = item['name']
                                            break
                        except:
                            pass
                    
                    # 如果還是沒有，嘗試 og:title
                    if not title and soup.find('meta', property='og:title'):
                        title = soup.find('meta', property='og:title').get('content')
                    
                    # 如果還是沒有，嘗試 title 標籤
                    if not title and soup.find('title'):
                        title = soup.find('title').get_text().strip()
                    
                    # 清理 YouTube 標題（移除 " - YouTube" 等後綴）
                    if title:
                        title = re.sub(r'\s*-\s*YouTube\s*$', '', title, flags=re.IGNORECASE)
                        title = re.sub(r'\s*-\s*YouTube\s*-\s*.*$', '', title, flags=re.IGNORECASE)
                        title = title.strip()
                else:
                    # 一般網站的處理
                    if soup.find('meta', property='og:title'):
                        title = soup.find('meta', property='og:title').get('content')
                    elif soup.find('title'):
                        title = soup.find('title').get_text().strip()
                
                # 提取 description
                description = None
                if soup.find('meta', property='og:description'):
                    description = soup.find('meta', property='og:description').get('content')
                elif soup.find('meta', attrs={'name': 'description'}):
                    description = soup.find('meta', attrs={'name': 'description'}).get('content')
                
                # 提取 image
                image_url = None
                if soup.find('meta', property='og:image'):
                    image_url = soup.find('meta', property='og:image').get('content')
                elif soup.find('meta', property='twitter:image'):
                    image_url = soup.find('meta', property='twitter:image').get('content')
                
                # 判斷 content_type
                content_type = MetadataExtractor._detect_content_type(url, domain, soup)
                
                return {
                    'title': title,
                    'description': description,
                    'image_url': image_url,
                    'domain': domain,
                    'content_type': content_type
                }
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            # 即使失敗也返回基本信息
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('www.', '')
            return {
                'title': None,
                'description': None,
                'image_url': None,
                'domain': domain,
                'content_type': MetadataExtractor._detect_content_type(url, domain, None)
            }
    
    @staticmethod
    def _detect_content_type(url: str, domain: str, soup: Optional[BeautifulSoup]) -> str:
        """根據 URL 和 domain 判斷內容類型"""
        url_lower = url.lower()
        domain_lower = domain.lower()
        
        # 視頻平台
        if any(platform in domain_lower for platform in ['youtube.com', 'youtu.be', 'vimeo.com', 'bilibili.com', 'tiktok.com']):
            return 'video'
        
        # 購物平台
        if any(platform in domain_lower for platform in ['shopee', 'amazon', 'momo', 'pchome', 'rakuten']):
            return 'shopping'
        
        # 社交媒體
        if any(platform in domain_lower for platform in ['instagram.com', 'facebook.com', 'twitter.com', 'threads.net', 'linkedin.com']):
            return 'post'
        
        # 文章平台
        if any(platform in domain_lower for platform in ['medium.com', 'substack.com', 'notion.so', 'blog']):
            return 'article'
        
        # 如果有 video 標籤
        if soup and soup.find('video'):
            return 'video'
        
        # 默認
        return 'other'

