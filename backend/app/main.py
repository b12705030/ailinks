from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import links, reports, chat
from app.services.scheduler import setup_scheduler

app = FastAPI(
    title="Link Collector API",
    description="AI 智能連結收集系統",
    version="1.0.0"
)

# CORS 配置（開發環境允許所有來源，生產環境請限制）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發環境允許所有來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(links.router)
app.include_router(reports.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {
        "message": "Link Collector API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# 啟動時設置定時任務
@app.on_event("startup")
async def startup_event():
    if settings.weekly_report_enabled:
        setup_scheduler()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

