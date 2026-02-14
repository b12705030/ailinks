from fastapi import APIRouter, HTTPException
from app.models.link import WeeklyReport, LinkResponse
from app.services.database import DatabaseService
from app.services.ai_classifier import AIClassifier
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api/reports", tags=["reports"])

db = DatabaseService()
ai_classifier = AIClassifier()


@router.get("/weekly", response_model=WeeklyReport)
async def get_weekly_report(week_start: Optional[str] = None):
    """獲取週報"""
    try:
        # 解析 week_start 或使用本週
        if week_start:
            week_start_dt = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
        else:
            today = datetime.now()
            week_start_dt = today - timedelta(days=today.weekday())
        
        # 獲取統計數據
        stats = await db.get_weekly_stats(week_start_dt)
        
        # AI 生成分析
        ai_analysis = await ai_classifier.generate_weekly_report(
            stats=stats,
            top_links=stats.get('top_links', [])
        )
        
        return WeeklyReport(
            week_start=stats['week_start'],
            total_links=stats['total_links'],
            unique_domains=stats['unique_domains'],
            unique_sources=stats['unique_sources'],
            category_distribution=stats['category_distribution'],
            top_links=[LinkResponse(**link) for link in stats['top_links']],
            ai_analysis=ai_analysis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

