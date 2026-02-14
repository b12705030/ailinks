# 🚀 快速設置指南

## 1. 環境準備

### 後端

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 前端

```bash
cd frontend
npm install
```

## 2. 配置 Supabase

1. 在 [Supabase](https://supabase.com) 創建新項目
2. 進入 SQL Editor
3. 運行 `supabase/migrations/001_create_links_table.sql`
4. 獲取你的 Supabase URL 和 API Key

## 3. 配置環境變量

在項目根目錄創建 `.env` 文件：

```bash
# 複製示例文件
cp .env.example .env
```

編輯 `.env`，填入：

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4o-mini
```

## 4. 啟動服務

### 啟動後端

```bash
cd backend
python run.py
```

後端會在 `http://localhost:8000` 運行

### 啟動前端

```bash
cd frontend
npm run dev
```

前端會在 `http://localhost:3000` 運行

## 5. 測試

1. 打開 `http://localhost:3000`
2. 點擊「添加連結」
3. 輸入一個 URL，例如：`https://www.youtube.com/watch?v=dQw4w9WgXcQ`
4. 等待 AI 自動分類
5. 查看連結列表和週報

## 6. 配置週報（可選）

### Telegram Bot

1. 在 Telegram 找 [@BotFather](https://t.me/botfather)
2. 創建新 bot，獲取 token
3. 獲取你的 chat_id（發送消息給 bot，訪問 `https://api.telegram.org/bot<token>/getUpdates`）
4. 在 `.env` 中添加：

```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

### Email

在 `.env` 中添加：

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
```

## 7. 部署（可選）

### 後端部署到 Railway

1. 在 Railway 創建新項目
2. 連接 GitHub 倉庫
3. 設置環境變量
4. Railway 會自動部署

### 前端部署到 Vercel

1. 在 Vercel 創建新項目
2. 連接 GitHub 倉庫
3. 設置環境變量 `VITE_API_URL` 為你的後端 URL
4. Vercel 會自動部署

## 常見問題

### Q: OpenAI API 調用失敗？

A: 檢查你的 API Key 是否正確，賬戶是否有餘額。

### Q: Supabase 連接失敗？

A: 檢查 URL 和 Key 是否正確，確保網絡可以訪問 Supabase。

### Q: 週報沒有發送？

A: 檢查定時任務是否啟動，查看後端日誌。

