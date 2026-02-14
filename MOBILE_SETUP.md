# 📱 手機使用指南

## 🎯 方式一：通過瀏覽器訪問（最簡單）

### 前提條件
- 手機和電腦連接到**同一個 Wi-Fi 網絡**
- 後端和前端都在運行

### 步驟 1：獲取電腦的 IP 地址

#### Windows
```powershell
# 在 PowerShell 中運行
ipconfig

# 找到 "IPv4 地址"，例如：192.168.1.100
```

#### Mac/Linux
```bash
ifconfig | grep "inet "
# 或
ip addr show
```

### 步驟 2：修改後端配置

編輯 `backend/app/config.py`，確保 `frontend_url` 包含你的 IP：

```python
frontend_url: str = "http://192.168.1.100:3000"  # 替換為你的 IP
```

或者更簡單，允許所有來源（僅開發環境）：

```python
# 在 backend/app/main.py 中
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發環境可以這樣，生產環境不建議
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 步驟 3：修改前端配置

編輯 `frontend/src/api/client.ts`，將 API URL 改為你的 IP：

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://192.168.1.100:8000'
```

或者創建 `frontend/.env.local`：

```env
VITE_API_URL=http://192.168.1.100:8000
```

### 步驟 4：重啟服務

1. **重啟後端**（在 backend 目錄）：
   ```bash
   python run.py
   ```
   確保顯示：`Uvicorn running on http://0.0.0.0:8000`

2. **重啟前端**（在 frontend 目錄）：
   ```bash
   npm run dev
   ```
   確保顯示：`Local: http://localhost:3000` 和 `Network: http://192.168.1.100:3000`

### 步驟 5：在手機瀏覽器訪問

在手機瀏覽器中打開：
```
http://192.168.1.100:3000
```
（替換為你的實際 IP 地址）

---

## 🚀 方式二：部署到雲端（推薦，隨時可用）

### 優點
- ✅ 隨時隨地訪問，不需要在同一網絡
- ✅ 可以分享給朋友使用
- ✅ 更穩定

### 部署步驟

#### 1. 後端部署到 Railway

1. 前往 [Railway](https://railway.app)
2. 創建新項目，連接 GitHub 倉庫
3. 設置環境變量（從你的 `.env` 文件）
4. Railway 會自動部署

#### 2. 前端部署到 Vercel

1. 前往 [Vercel](https://vercel.com)
2. 導入項目
3. 設置環境變量：
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```
4. 部署完成後，會獲得一個 URL，例如：`https://your-app.vercel.app`

#### 3. 在手機訪問

直接在手機瀏覽器打開 Vercel 提供的 URL 即可！

---

## 📲 方式三：Android Share Target（最方便）

這是**最方便的方式**，可以直接從任何 App 分享連結到你的系統。

### 選項 A：使用 Tasker（推薦，無需開發）

1. **安裝 Tasker**（需要付費，但功能強大）
2. **創建 Profile**：
   - Event → Intent Received
   - Action: `android.intent.action.SEND`
   - MIME Type: `text/plain`
3. **創建 Task**：
   - HTTP Request
   - Method: POST
   - URL: `http://your-api-url/api/links`
   - Headers: `Content-Type: application/json`
   - Body:
     ```json
     {
       "url": "%text",
       "source_app": "%app_package"
     }
     ```

### 選項 B：開發簡單的 Android App

如果你會 Android 開發，可以創建一個簡單的 Share Target App。參考 `android/README.md` 中的代碼示例。

### 選項 C：使用 Shortcuts App

1. 安裝 [Shortcuts](https://play.google.com/store/apps/details?id=com.rhmsoft.shortcuts)
2. 創建新的 Shortcut
3. 設置 Intent Action 為 `android.intent.action.SEND`
4. 在 Shortcut 中調用你的 API

---

## 🎨 方式四：添加到手機主屏幕（PWA）

讓你的應用像原生 App 一樣使用！

### 步驟

1. 在手機瀏覽器打開你的應用
2. 點擊瀏覽器菜單（三個點）
3. 選擇「添加到主屏幕」或「安裝應用」
4. 現在可以像 App 一樣從主屏幕打開

### 需要添加 PWA 支持（可選）

如果你想讓它更像原生 App，可以添加：

1. **創建 `frontend/public/manifest.json`**：
```json
{
  "name": "Link Collector",
  "short_name": "LinkCollector",
  "description": "AI 智能連結收集系統",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

2. **在 `frontend/index.html` 中添加**：
```html
<link rel="manifest" href="/manifest.json">
```

---

## 🔧 快速測試

### 測試本地網絡訪問

1. 確保手機和電腦在同一 Wi-Fi
2. 在手機瀏覽器輸入：`http://[你的IP]:3000`
3. 如果無法訪問，檢查：
   - Windows 防火牆是否允許端口 3000 和 8000
   - 路由器是否允許設備間通信

### 測試 API 連接

在手機瀏覽器打開：
```
http://[你的IP]:8000/docs
```
應該能看到 API 文檔頁面。

---

## 💡 推薦方案

### 個人使用（快速）
- **方式一**：本地網絡訪問（最簡單，5 分鐘搞定）

### 長期使用（穩定）
- **方式二**：部署到雲端（一次設置，永久使用）

### 最方便（自動化）
- **方式三**：Android Share Target + Tasker（分享即保存）

---

## ❓ 常見問題

### Q: 手機無法訪問？
A: 
1. 檢查 IP 地址是否正確
2. 確保手機和電腦在同一 Wi-Fi
3. 檢查防火牆設置
4. 嘗試關閉 VPN

### Q: API 調用失敗？
A:
1. 檢查後端是否在運行
2. 檢查 CORS 設置
3. 確認 API URL 正確

### Q: 想在外網訪問？
A: 必須部署到雲端（Railway/Vercel），或者使用內網穿透工具（如 ngrok）

---

## 🎉 完成！

選擇最適合你的方式，開始在手機上收集連結吧！

