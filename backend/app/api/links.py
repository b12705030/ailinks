from fastapi import APIRouter, HTTPException, Query
from app.models.link import LinkCreate, LinkResponse, LinkUpdate
from app.services.database import DatabaseService
from app.services.metadata_extractor import MetadataExtractor
from app.services.ai_classifier import AIClassifier
from typing import List, Optional

router = APIRouter(prefix="/api/links", tags=["links"])

db = DatabaseService()
metadata_extractor = MetadataExtractor()
ai_classifier = AIClassifier()


@router.post("", response_model=LinkResponse, status_code=201)
async def create_link(link_data: LinkCreate):
    """創建新連結並自動分類"""
    try:
        # 1. 提取 metadata
        metadata = await metadata_extractor.extract(link_data.url)
        
        # 2. AI 分類
        ai_result = await ai_classifier.classify(
            url=link_data.url,
            title=metadata.get('title') or link_data.title,
            description=metadata.get('description') or link_data.description,
            domain=metadata.get('domain', '')
        )
        
        # 3. 保存到數據庫
        link_record = {
            'url': link_data.url,
            'title': metadata.get('title') or link_data.title,
            'description': metadata.get('description') or link_data.description,
            'image_url': metadata.get('image_url'),
            'domain': metadata.get('domain', ''),
            'source_app': link_data.source_app,
            'content_type': metadata.get('content_type', 'other'),
            'ai_category': ai_result.get('ai_category'),
            'ai_tags': ai_result.get('ai_tags', []),
            'summary': ai_result.get('summary'),
            'short_name': ai_result.get('short_name'),
            'importance_score': ai_result.get('importance_score', 50)
        }
        
        result = await db.create_link(link_record)
        return LinkResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating link: {str(e)}")


@router.get("", response_model=List[LinkResponse])
async def get_links(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None,
    reviewed: Optional[bool] = None,
    search: Optional[str] = None
):
    """獲取連結列表"""
    try:
        links = await db.get_links(
            limit=limit,
            offset=offset,
            category=category,
            reviewed=reviewed,
            search=search
        )
        return [LinkResponse(**link) for link in links]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching links: {str(e)}")


@router.get("/{link_id}", response_model=LinkResponse)
async def get_link(link_id: str):
    """獲取單個連結"""
    try:
        link = await db.get_link_by_id(link_id)
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        return LinkResponse(**link)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching link: {str(e)}")


@router.patch("/{link_id}", response_model=LinkResponse)
async def update_link(link_id: str, update_data: LinkUpdate):
    """更新連結"""
    try:
        update_dict = update_data.model_dump(exclude_unset=True)
        result = await db.update_link(link_id, update_dict)
        if not result:
            raise HTTPException(status_code=404, detail="Link not found")
        return LinkResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating link: {str(e)}")


@router.delete("/{link_id}", status_code=204)
async def delete_link(link_id: str):
    """刪除連結"""
    try:
        await db.delete_link(link_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting link: {str(e)}")

