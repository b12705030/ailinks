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
        # 1. 先搜索相關連結
        search_query = request.message
        links = await db.get_links(
            limit=20,
            offset=0,
            search=search_query
        )
        
        # 2. 構建上下文信息
        links_context = ""
        if links:
            links_context = "\n相關連結：\n"
            for i, link in enumerate(links[:5], 1):  # 只取前5個
                links_context += f"{i}. {link.get('title', link.get('url', ''))}\n"
                if link.get('summary'):
                    links_context += f"   摘要：{link.get('summary')}\n"
                links_context += f"   分類：{link.get('ai_category', '未知')}\n"
                links_context += f"   URL：{link.get('url')}\n\n"
        
        # 3. 構建對話歷史
        messages = [
            {
                "role": "system",
                "content": """你是一個智能連結管理助手。你的職責是幫助用戶：
1. 搜索和查找他們保存的歷史連結
2. 回答關於連結的問題
3. 提供連結相關的建議和分析

請用友好、簡潔的中文回答。如果找到相關連結，請在回答中提及並總結。"""
            }
        ]
        
        # 添加對話歷史（最近3輪）
        for msg in request.conversation_history[-6:]:  # 最近3輪（每輪2條消息）
            if msg.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # 4. 添加當前問題和上下文
        user_message = f"""用戶問題：{request.message}

{links_context if links_context else "未找到相關連結。"}

請根據以上信息回答用戶的問題。如果找到了相關連結，請簡要介紹它們。"""
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # 5. 調用 OpenAI API
        response = openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        
        # 6. 返回結果
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

