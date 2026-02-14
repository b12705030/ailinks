# 🔗 Link Collector - AI 智能連結收集系統

一個可以自動收集、分類和整理你發送到 Messenger 或其他應用的連結的智能系統。

## ✨ 功能特性

- 📱 **多平台支持**：從 Messenger、Instagram、Facebook、Threads 等應用收集連結
- 🤖 **AI 自動分類**：使用規則 + LLM 語義分析自動分類連結
- 📊 **智能週報**：每週自動生成分析報告
- 🏷️ **自動標籤**：AI 自動生成相關標籤
- 📈 **趨勢分析**：追蹤你的興趣變化

## 🏗️ 技术栈

- **後端**：FastAPI + Python
- **數據庫**：Supabase (PostgreSQL)
- **AI**：OpenAI API / Anthropic Claude
- **前端**：React + TypeScript
- **部署**：Vercel (前端) + Railway/Render (後端)

## 📁 项目结构

```
ailinks/
├── backend/          # FastAPI 後端
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── requirements.txt
├── frontend/         # React 前端
├── supabase/         # 數據庫遷移文件
└── android/          # Android Share Target (可选)
```

## 🚀 快速开始

### 1. 環境變量設置

複製 `.env.example` 為 `.env` 並填入：

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_key
```

### 2. 數據庫初始化

運行 Supabase migration 文件創建表結構。

### 3. 啟動後端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. 啟動前端

```bash
cd frontend
npm install
npm run dev
```

## 📱 使用方式

### 方式 1：Android Share Target（推荐）

1. 在任何應用中看到喜歡的連結
2. 點擊「分享」
3. 選擇「Link Collector」
4. 自動保存並分類

### 方式 2：API 直接调用

```bash
curl -X POST http://localhost:8000/api/links \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

## 🎯 分类系统

AI 會自動將連結分類為：
- 娱乐
- 学习
- 工作
- 购物
- 食谱
- 健身
- 旅游
- 灵感
- 其他

## 📊 周报功能

每週日晚上自動生成週報，包含：
- 本週收集的連結數量
- 分類統計
- 來源分析
- 推薦回看的連結
- AI 生成的趨勢分析

