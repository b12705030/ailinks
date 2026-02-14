# ☁️ 雲端部署指南

## 🎯 為什麼要部署到雲端？

### 本地部署的限制
- ❌ 手機和電腦必須在同一 Wi-Fi
- ❌ 電腦關機就無法使用
- ❌ IP 地址可能會變化

### 雲端部署的優勢
- ✅ **隨時隨地訪問**，不需要在同一網絡
- ✅ **24/7 運行**，電腦關機也能用
- ✅ **穩定可靠**，不會因為 IP 變化而失效
- ✅ **可以分享給朋友**使用

---

## 🚀 部署步驟

### 第一步：部署後端到 Railway

#### 1. 註冊 Railway

1. 前往 [Railway](https://railway.app)
2. 使用 GitHub 帳號登錄（推薦）或 Email 註冊
3. 免費版有 $5 額度，足夠個人使用

#### 2. 創建項目

1. 點擊 **New Project**
2. 選擇 **Deploy from GitHub repo**
3. 連接你的 GitHub 倉庫（如果還沒上傳，先上傳到 GitHub）
4. 選擇 `ailinks` 倉庫

#### 3. 配置服務

1. Railway 會自動檢測到 `backend` 目錄
2. 點擊服務，進入設置
3. 在 **Settings** → **Generate Domain** 生成一個域名
4. 記下這個域名，例如：`your-app.up.railway.app`

#### 4. 設置環境變量

在 **Variables** 標籤中添加所有環境變量：

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4o-mini
APP_ENV=production
APP_URL=https://your-app.up.railway.app
FRONTEND_URL=https://your-frontend.vercel.app
WEEKLY_REPORT_ENABLED=true
WEEKLY_REPORT_DAY=sunday
WEEKLY_REPORT_TIME=20:00
```

#### 5. 部署

Railway 會自動：
- 檢測到 `requirements.txt`
- 安裝依賴
- 運行 `python run.py` 或自動檢測啟動命令

等待部署完成（約 2-5 分鐘）

#### 6. 測試後端

訪問 `https://your-app.up.railway.app/docs`，應該能看到 API 文檔。

---

### 第二步：部署前端到 Vercel

#### 1. 註冊 Vercel

1. 前往 [Vercel](https://vercel.com)
2. 使用 GitHub 帳號登錄
3. 免費版完全夠用

#### 2. 導入項目

1. 點擊 **Add New** → **Project**
2. 選擇你的 GitHub 倉庫
3. 選擇 `ailinks` 倉庫

#### 3. 配置項目

1. **Framework Preset**: Vite
2. **Root Directory**: `frontend`
3. **Build Command**: `npm run build`
4. **Output Directory**: `dist`

#### 4. 設置環境變量

在 **Environment Variables** 中添加：

```env
VITE_API_URL=https://your-app.up.railway.app
```

（替換為你的 Railway 後端地址）

#### 5. 部署

點擊 **Deploy**，等待完成（約 1-2 分鐘）

#### 6. 獲取前端地址

部署完成後，Vercel 會給你一個地址，例如：
`https://ailinks.vercel.app`

---

## 📱 更新手機配置

### 方式一：更新 Tasker 配置

1. 打開 Tasker
2. 找到你的「保存連結到 Link Collector」Task
3. 編輯 **HTTP Request** 動作
4. 將 URL 改為：
   ```
   https://your-app.up.railway.app/api/links
   ```
5. 保存

### 方式二：更新 Android App

如果你開發了 Android App，修改 `ShareActivity.kt` 中的 URL：

```kotlin
val request = Request.Builder()
    .url("https://your-app.up.railway.app/api/links") // 改為雲端地址
    .post(requestBody)
    .build()
```

重新編譯並安裝。

### 方式三：更新前端 API 地址

如果前端也部署了，手機瀏覽器訪問：
```
https://your-frontend.vercel.app
```

---

## ✅ 部署後的好處

### 1. 隨時隨地使用

- 不需要手機和電腦在同一 Wi-Fi
- 可以在任何地方使用
- 電腦關機也能用

### 2. 分享功能更穩定

- Facebook 分享 → Tasker/App → 雲端 API
- 完全自動化，無需手動操作
- 不會因為網絡問題失敗

### 3. 可以分享給朋友

- 給朋友你的前端地址
- 他們也可以使用（需要你提供 API 訪問權限，或設置用戶系統）

---

## 🔧 更新 CORS 配置

部署到雲端後，記得更新後端的 CORS 設置：

編輯 `backend/app/main.py`：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",  # 你的前端地址
        "http://localhost:3000",  # 本地開發
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

然後重新部署到 Railway。

---

## 🎯 完整流程示例

### 部署前（本地）
```
Facebook → 分享 → Tasker → http://192.168.1.105:8000/api/links
（需要同一 Wi-Fi）
```

### 部署後（雲端）
```
Facebook → 分享 → Tasker → https://your-app.up.railway.app/api/links
（隨時隨地可用！）
```

---

## 💰 費用

### Railway（後端）
- **免費版**：$5 額度/月
- 個人使用完全夠用
- 如果超過，可以升級到 Hobby 計劃（$5/月）

### Vercel（前端）
- **免費版**：完全免費
- 無限部署
- 足夠個人使用

### 總計
- **完全免費**（如果用量不大）
- 或 **$5/月**（如果 Railway 用量較大）

---

## 🚨 注意事項

### 1. 環境變量安全

- ✅ 不要在代碼中硬編碼 API Key
- ✅ 使用環境變量存儲敏感信息
- ✅ Railway 和 Vercel 都支持環境變量加密

### 2. API 限流

考慮添加 API 限流，防止濫用：

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@router.post("")
@limiter.limit("10/minute")  # 每分鐘最多 10 次
async def create_link(...):
    ...
```

### 3. 數據庫備份

定期備份 Supabase 數據：
- Supabase Dashboard → Database → Backups
- 可以設置自動備份

---

## 🎉 完成！

部署完成後，你就可以：

1. ✅ **隨時隨地**從 Facebook 分享連結
2. ✅ **自動保存**到你的系統
3. ✅ **AI 自動分類**和整理
4. ✅ **查看週報**分析

享受雲端部署帶來的便利吧！🚀

---

## 📝 快速檢查清單

- [ ] Railway 後端部署完成
- [ ] Vercel 前端部署完成
- [ ] 環境變量設置正確
- [ ] CORS 配置更新
- [ ] Tasker/App 中的 API URL 更新為雲端地址
- [ ] 測試分享功能
- [ ] 測試手機瀏覽器訪問

---

## ❓ 常見問題

### Q: Railway 部署失敗？
A: 檢查環境變量是否正確，查看 Railway 日誌

### Q: Vercel 無法連接後端？
A: 檢查 `VITE_API_URL` 環境變量是否正確設置

### Q: 分享功能不工作？
A: 確認 Tasker/App 中的 API URL 已更新為雲端地址

