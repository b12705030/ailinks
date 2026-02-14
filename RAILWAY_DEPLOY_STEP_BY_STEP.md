# 🚂 Railway 部署詳細步驟

## 📋 前置準備

### 1. 確保代碼已上傳到 GitHub

如果還沒上傳，需要先：

```bash
# 在項目根目錄
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/ailinks.git
git push -u origin main
```

### 2. 準備環境變量

確保你的 `backend/.env` 文件中有這些值：
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OPENAI_API_KEY`

---

## 🚀 Railway 部署步驟

### 步驟 1：註冊 Railway

1. 前往 [Railway](https://railway.app)
2. 點擊 **Start a New Project**
3. 選擇 **Login with GitHub**（推薦）或使用 Email 註冊
4. 授權 Railway 訪問你的 GitHub

### 步驟 2：創建新項目

1. 登錄後，點擊 **New Project**
2. 選擇 **Deploy from GitHub repo**
3. 如果第一次使用，需要授權 Railway 訪問 GitHub
4. 選擇你的 `ailinks` 倉庫
5. 點擊 **Deploy Now**

### 步驟 3：配置服務

Railway 會自動檢測到你的項目，但需要指定後端目錄：

1. 點擊創建的服務
2. 進入 **Settings** 標籤
3. 找到 **Root Directory**
4. 設置為：`backend`
5. 保存

### 步驟 4：設置啟動命令

1. 在 **Settings** 中找到 **Start Command**
2. 設置為：
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   或者 Railway 可能會自動檢測，如果自動檢測到了就不需要手動設置

### 步驟 5：設置環境變量

1. 在服務頁面，點擊 **Variables** 標籤
2. 點擊 **+ New Variable** 添加以下變量：

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4o-mini
APP_ENV=production
WEEKLY_REPORT_ENABLED=true
WEEKLY_REPORT_DAY=sunday
WEEKLY_REPORT_TIME=20:00
```

**重要**：
- 將 `your-project.supabase.co` 替換為你的實際 Supabase URL
- 將 `your-anon-key` 替換為你的實際 Supabase Key
- 將 `sk-your-openai-key` 替換為你的實際 OpenAI API Key

### 步驟 6：生成域名

1. 在 **Settings** 標籤中
2. 找到 **Generate Domain** 按鈕
3. 點擊生成一個域名
4. Railway 會給你一個地址，例如：`ailinks-production.up.railway.app`
5. **記下這個地址**，這就是你的後端 API 地址

### 步驟 7：等待部署

1. Railway 會自動：
   - 檢測到 `requirements.txt`
   - 安裝 Python 依賴
   - 運行你的應用
2. 等待部署完成（約 2-5 分鐘）
3. 查看 **Deployments** 標籤，確認部署成功（綠色 ✅）

### 步驟 8：測試部署

1. 訪問 `https://your-app.up.railway.app/docs`
2. 應該能看到 FastAPI 文檔頁面
3. 如果能看到，說明部署成功！

---

## 🔧 常見問題

### Q: Railway 找不到後端？

**解決**：
1. 確認 **Root Directory** 設置為 `backend`
2. 確認 `backend` 目錄下有 `requirements.txt` 和 `app` 目錄

### Q: 部署失敗？

**檢查**：
1. 查看 **Deployments** 標籤中的日誌
2. 確認環境變量是否正確
3. 確認 `requirements.txt` 中的依賴是否正確

### Q: API 無法訪問？

**檢查**：
1. 確認域名已生成
2. 確認服務正在運行（Deployments 顯示成功）
3. 嘗試訪問 `/docs` 端點

### Q: CORS 錯誤？

**解決**：
需要更新後端的 CORS 配置，允許你的前端域名。但現在先測試後端是否正常。

---

## 📝 部署後的重要信息

### 獲取你的 API 地址

部署完成後，你的 API 地址格式為：
```
https://your-app-name.up.railway.app
```

完整的 API 端點：
```
https://your-app-name.up.railway.app/api/links
```

### 更新 Android App

部署完成後，在 `ShareActivity.kt` 中更新：

```kotlin
private val API_URL = "https://your-app-name.up.railway.app/api/links"
```

然後重新編譯 APK。

---

## 🎯 下一步

部署完成後：

1. ✅ 測試 API 是否正常（訪問 `/docs`）
2. ✅ 更新 Android App 中的 API_URL
3. ✅ 重新編譯並安裝 APK
4. ✅ 測試分享功能

---

## 💡 提示

- Railway 免費版有 $5/月額度，個人使用完全夠用
- 如果服務暫停，可能是額度用完了，可以升級或等待下個月
- 建議設置環境變量後再部署，避免部署失敗

---

## 🎉 完成！

部署完成後，你就可以隨時隨地使用你的 API 了！

需要幫助？查看 Railway 的 **Deployments** 日誌，那裡會有詳細的錯誤信息。

