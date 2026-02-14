from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config import settings
from app.services.database import DatabaseService
from app.services.ai_classifier import AIClassifier
from app.services.notifier import Notifier
from datetime import datetime, timedelta
import asyncio


scheduler = AsyncIOScheduler()
db = DatabaseService()
ai_classifier = AIClassifier()
notifier = Notifier()


async def generate_and_send_weekly_report():
    """生成並發送週報"""
    try:
        # 獲取上週的統計數據
        today = datetime.now()
        last_week_start = today - timedelta(days=today.weekday() + 7)
        
        stats = await db.get_weekly_stats(last_week_start)
        
        # AI 生成分析
        ai_analysis = await ai_classifier.generate_weekly_report(
            stats=stats,
            top_links=stats.get('top_links', [])
        )
        
        # 發送通知
        await notifier.send_weekly_report(stats, ai_analysis)
        
        print(f"Weekly report generated and sent at {datetime.now()}")
        
    except Exception as e:
        print(f"Error generating weekly report: {e}")


def setup_scheduler():
    """設置定時任務"""
    # 解析週報時間
    day_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }
    
    day = day_map.get(settings.weekly_report_day.lower(), 6)
    time_parts = settings.weekly_report_time.split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
    
    # 添加每週任務
    scheduler.add_job(
        generate_and_send_weekly_report,
        trigger=CronTrigger(day_of_week=day, hour=hour, minute=minute),
        id='weekly_report',
        replace_existing=True
    )
    
    scheduler.start()
    print(f"Scheduler started. Weekly report will run every {settings.weekly_report_day} at {settings.weekly_report_time}")

