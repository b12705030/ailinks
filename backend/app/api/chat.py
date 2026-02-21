from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.database import DatabaseService
from app.services.ai_classifier import AIClassifier
from openai import OpenAI
from app.config import settings
import json

router = APIRouter(prefix="/api/chat", tags=["chat"])

db = DatabaseService()
ai_classifier = AIClassifier()
openai_client = OpenAI(api_key=settings.openai_api_key)


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    response: str
    links: List[dict] = []


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """AI 智能助手對話"""
    try:
        # 1. 先讓 AI 理解問題並提取搜索關鍵詞
        extract_messages = [
            {
                "role": "system",
                "content": """你是一個搜索關鍵詞提取助手。用戶會問關於他們保存的連結的問題。
請分析問題並提取1-3個最重要的搜索關鍵詞（用逗號分隔）。
如果問題是關於分類的（如「健身」、「學習」），直接返回分類名稱。
如果問題是關於時間的（如「這週」、「最近」），返回「recent」。
如果問題是統計類的（如「有多少」、「總共」），返回「stats」。
只返回關鍵詞，不要其他文字。"""
            },
            {
                "role": "user",
                "content": f"用戶問題：{request.message}\n\n請提取搜索關鍵詞："
            }
        ]
        
        extract_response = openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=extract_messages,
            temperature=0.3,
            max_tokens=50
        )
        
        extracted_keywords = extract_response.choices[0].message.content.strip()
        
        # 2. 獲取數據庫統計信息（給 AI 更多上下文）
        all_links = await db.get_links(limit=1000, offset=0)  # 獲取更多連結用於統計
        total_count = len(all_links)
        
        # 統計分類
        categories = {}
        for link in all_links:
            cat = link.get('ai_category', '其他')
            categories[cat] = categories.get(cat, 0) + 1
        
        # 統計來源
        sources = {}
        for link in all_links:
            src = link.get('source_app', 'unknown')
            if src:
                sources[src] = sources.get(src, 0) + 1
        
        # 3. 根據關鍵詞搜索連結
        links = []
        if extracted_keywords.lower() == "stats":
            # 統計類問題，返回所有連結用於統計
            links = all_links[:20]
        elif extracted_keywords.lower() == "recent":
            # 最近的問題，獲取最近的連結
            links = all_links[:20]
        else:
            # 正常搜索
            keywords = [k.strip() for k in extracted_keywords.split(',') if k.strip()]
            for keyword in keywords[:3]:  # 最多嘗試3個關鍵詞
                found = await db.get_links(
                    limit=20,
                    offset=0,
                    search=keyword
                )
                links.extend(found)
                if len(links) >= 20:
                    break
            
            # 去重
            seen_ids = set()
            unique_links = []
            for link in links:
                link_id = link.get('id')
                if link_id and link_id not in seen_ids:
                    seen_ids.add(link_id)
                    unique_links.append(link)
            links = unique_links[:20]
        
        # 4. 構建上下文信息
        stats_context = f"""
數據庫統計信息：
- 總連結數：{total_count}
- 分類分布：{', '.join([f'{k}({v})' for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]])}
- 來源分布：{', '.join([f'{k}({v})' for k, v in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3]])}
"""
        
        links_context = ""
        if links:
            links_context = "\n找到的相關連結：\n"
            for i, link in enumerate(links[:10], 1):  # 顯示前10個
                links_context += f"{i}. 【{link.get('ai_category', '未知')}】{link.get('title', link.get('url', ''))}\n"
                if link.get('summary'):
                    links_context += f"   摘要：{link.get('summary')}\n"
                if link.get('ai_tags'):
                    tags = link.get('ai_tags', [])
                    if isinstance(tags, list) and tags:
                        links_context += f"   標籤：{', '.join(tags[:3])}\n"
                links_context += f"   來源：{link.get('source_app', '未知')}\n"
                links_context += f"   時間：{link.get('created_at', '')[:10]}\n\n"
        else:
            links_context = "\n未找到相關連結。"
        
        # 5. 構建對話歷史
        messages = [
            {
                "role": "system",
                "content": f"""你是一個智能連結管理助手。你的職責是幫助用戶：
1. 搜索和查找他們保存的歷史連結
2. 回答關於連結的問題（如「有多少連結」、「有哪些分類」等）
3. 提供連結相關的建議和分析
4. 根據統計信息回答問題

用戶的數據庫信息：
{stats_context}

回答格式要求：
- 使用 **粗體** 來強調重要信息（如分類名稱、數字等）
- **重要**：下方會顯示連結卡片，卡片已包含標題、分類、標籤、來源等詳細信息
- 因此文字回覆應該**簡短**，不需要重複列出每個連結的詳細信息
- 只提供簡短的總結和洞察，例如：「我找到了 **3** 個關於 **健身** 的連結，請查看下方卡片。」
- 對於統計問題，用簡潔的方式回答，例如：「你總共有 **50** 個連結，其中 **健身** 類有 **5** 個，**學習** 類有 **10** 個。」
- 避免冗長的列表，讓用戶直接查看卡片獲取詳細信息

請用友好、簡潔的中文回答。保持簡短，讓卡片來展示詳細信息。"""
            }
        ]
        
        # 添加對話歷史（最近3輪）
        for msg in request.conversation_history[-6:]:  # 最近3輪（每輪2條消息）
            if msg.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # 6. 添加當前問題和上下文
        user_message = f"""用戶問題：{request.message}

{links_context}

請根據以上信息回答用戶的問題。要求：
1. 使用 **粗體** 強調重要信息（分類、數字、關鍵詞）
2. **保持簡短**：下方會顯示連結卡片，卡片已包含所有詳細信息（標題、分類、標籤、來源等）
3. 不需要重複列出每個連結的詳細信息，只提供簡短總結
4. 如果用戶問統計問題，用簡潔方式回答，用 **粗體** 標出數字和分類
5. 可以添加一些洞察或建議，但保持簡短

例如格式（簡短版）：
「我找到了 **3** 個關於 **健身** 的連結，請查看下方卡片。」

或者（統計問題）：
「你總共有 **50** 個連結，其中 **健身** 類有 **5** 個，**學習** 類有 **10** 個。請查看下方卡片了解更多。」"""
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # 7. 調用 OpenAI API
        response = openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content
        
        # 8. 返回結果
        return ChatResponse(
            response=ai_response,
            links=[{
                "id": link.get("id"),
                "url": link.get("url"),
                "title": link.get("title"),
                "description": link.get("description"),
                "summary": link.get("summary"),
                "image_url": link.get("image_url"),
                "domain": link.get("domain"),
                "source_app": link.get("source_app"),
                "ai_category": link.get("ai_category"),
                "ai_tags": link.get("ai_tags", []),
                "reviewed": link.get("reviewed", False),
                "created_at": link.get("created_at")
            } for link in links[:10]]  # 返回前10個連結
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 對話錯誤: {str(e)}")

