# ⚡ Railway 快速修復

## 🔧 立即執行這些步驟

### 步驟 1：確認文件已上傳

在 PowerShell 運行：

```bash
cd C:\Users\tinti\Desktop\ailinks

# 檢查文件是否存在
ls backend/Procfile
ls backend/runtime.txt

# 如果存在，上傳到 GitHub
git add backend/Procfile backend/runtime.txt
git commit -m "Fix Railway deployment"
git push
```

### 步驟 2：在 Railway 確認設置

1. **進入服務的 Settings**
2. **Root Directory** 必須是：`backend`（沒有斜杠，沒有引號）
3. **保存**

### 步驟 3：手動設置啟動命令（如果 Procfile 不工作）

在 Railway Settings 中：

1. 找到 **Start Command** 或 **Command**
2. 設置為：
   ```
   python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. 保存

### 步驟 4：重新部署

1. 點擊 **Redeploy** 或等待自動重新部署
2. 查看 Build Logs

---

## 🎯 最關鍵的 3 個檢查

1. ✅ **Root Directory = `backend`**（在 Settings）
2. ✅ **Procfile 在 GitHub 的 backend 目錄**
3. ✅ **環境變量已設置**（至少 SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY）

---

## 📸 如果還是不行

請提供：
1. Railway Settings 頁面的截圖（特別是 Root Directory）
2. Build Logs 的完整錯誤信息
3. GitHub 倉庫中 backend 目錄的文件列表截圖

這樣我可以更精確地幫你解決！

