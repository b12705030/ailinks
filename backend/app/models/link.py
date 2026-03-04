from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class LinkCreate(BaseModel):
    url: str
    source_app: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class LinkResponse(BaseModel):
    id: UUID
    url: str
    title: Optional[str]
    description: Optional[str]
    summary: Optional[str]
    image_url: Optional[str]
    domain: str
    source_app: Optional[str]
    content_type: Optional[str]
    ai_category: Optional[str]
    ai_tags: List[str] = []
    short_name: Optional[str] = None  # AI 生成的簡短易識別名稱
    importance_score: int = 0
    reviewed: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LinkUpdate(BaseModel):
    reviewed: Optional[bool] = None
    ai_category: Optional[str] = None


class WeeklyReport(BaseModel):
    week_start: str
    total_links: int
    unique_domains: int
    unique_sources: int
    category_distribution: dict
    top_links: List[LinkResponse]
    ai_analysis: str

