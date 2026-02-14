# 🚀 快速啟動指南

## ✅ 項目狀態

**項目已經可以執行了！** 但需要先完成以下配置步驟。

## 📋 執行前檢查清單

### 1. 環境準備 ✅
- [x] Python 3.8+ 已安裝
- [x] Node.js 16+ 已安裝
- [x] Supabase 帳號（免費版即可）

### 2. 數據庫設置

1. 前往 [Supabase](https://supabase.com) 創建新項目
2. 進入 **SQL Editor**
3. 複製並執行 `supabase/migrations/001_create_links_table.sql` 的全部內容
4. 在 **Settings > API** 獲取：
   - Project URL
   - anon/public key

### 3. OpenAI API Key

1. 前往 [OpenAI Platform](https://platform.openai.com)
2. 創建 API Key
3. 確保帳戶有餘額（至少 $5）

### 4. 環境變量配置

在 `backend` 目錄下創建 `.env` 文件：

```bash
cd backend
# Windows (PowerShell)
New-Item .env
# Mac/Linux
touch .env
```

編輯 `.env`，填入以下內容：

```env
# Supabase 配置（必填）
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# OpenAI 配置（必填）
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4o-mini

# 應用配置（可選，有默認值）
APP_ENV=development
APP_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# 週報配置（可選）
WEEKLY_REPORT_ENABLED=true
WEEKLY_REPORT_DAY=sunday
WEEKLY_REPORT_TIME=20:00
```

## 🎯 啟動步驟

### 步驟 1：安裝後端依賴

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 步驟 2：啟動後端

```bash
# 在 backend 目錄下
python run.py
```

後端會在 `http://localhost:8000` 運行

**測試後端**：打開瀏覽器訪問 `http://localhost:8000/docs` 查看 API 文檔

### 步驟 3：安裝前端依賴

```bash
# 新開一個終端
cd frontend
npm install
```

### 步驟 4：啟動前端

```bash
npm run dev
```

前端會在 `http://localhost:3000` 運行

## 🧪 測試

1. 打開 `http://localhost:3000`
2. 點擊「添加連結」
3. 輸入一個測試 URL，例如：
   - `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - `https://medium.com/@example/article`
4. 等待 AI 自動分類（可能需要幾秒鐘）
5. 查看連結列表，應該能看到分類結果

## ❌ 常見問題

### 問題 1：後端啟動失敗

**錯誤**：`ModuleNotFoundError: No module named 'app'`

**解決**：確保在 `backend` 目錄下運行，並且已激活虛擬環境

### 問題 2：Supabase 連接失敗

**錯誤**：`Invalid API key` 或連接超時

**解決**：
- 檢查 `.env` 中的 URL 和 Key 是否正確
- 確認 Supabase 項目沒有暫停（免費版會自動暫停）

### 問題 3：OpenAI API 調用失敗

**錯誤**：`Invalid API key` 或 `Insufficient quota`

**解決**：
- 檢查 API Key 是否正確
- 確認帳戶有餘額
- 檢查 API Key 是否有使用限制

### 問題 4：前端無法連接後端

**錯誤**：`Network Error` 或 `CORS error`

**解決**：
- 確認後端正在運行（訪問 `http://localhost:8000/docs`）
- 檢查 `backend/app/config.py` 中的 `frontend_url` 是否正確

## 📝 下一步

項目運行後，你可以：

1. **測試功能**：添加幾個連結，測試分類功能
2. **查看週報**：等待一週後查看自動生成的週報
3. **配置通知**：設置 Telegram 或 Email 接收週報（可選）
4. **部署上線**：參考 `SETUP.md` 部署到 Railway/Vercel

## 🎉 完成！

如果所有步驟都完成，項目應該可以正常運行了！

如有問題，請檢查：
- 後端日誌（終端輸出）
- 瀏覽器控制台（F12）
- Supabase Dashboard 的日誌

