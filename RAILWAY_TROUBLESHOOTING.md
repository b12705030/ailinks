# 🔧 Railway 部署故障排除

## ❌ Build Failed 常見原因

### 1. Root Directory 設置錯誤

**問題**：Railway 找不到 `requirements.txt` 或 `app` 目錄

**解決**：
1. 進入服務的 **Settings**
2. 找到 **Root Directory**
3. 設置為：`backend`
4. 保存並重新部署

### 2. 啟動命令錯誤

**問題**：Railway 不知道如何啟動應用

**解決**：
1. 進入 **Settings** → **Start Command**
2. 設置為：
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. 或者 Railway 可能會自動檢測，如果自動檢測到了就不需要設置

### 3. Python 版本問題

**問題**：Railway 使用的 Python 版本不兼容

**解決**：
在 `backend` 目錄創建 `runtime.txt`：

```txt
python-3.11.0
```

或者使用其他版本：
- `python-3.10.0`
- `python-3.9.0`

### 4. 依賴安裝失敗

**問題**：`requirements.txt` 中的某些依賴無法安裝

**檢查**：
1. 查看 Railway 的 **Deployments** 標籤
2. 點擊失敗的部署
3. 查看 **Build Logs**，找到具體錯誤

**常見錯誤**：
- 依賴版本衝突
- 缺少系統依賴
- 網絡問題

---

## 🔍 如何查看詳細錯誤

### 步驟：

1. 在 Railway 項目頁面
2. 點擊你的服務
3. 進入 **Deployments** 標籤
4. 點擊失敗的部署（紅色 ❌）
5. 查看 **Build Logs** 或 **Deploy Logs**
6. 找到錯誤信息（通常是紅色的）

---

## 🛠️ 常見錯誤和解決方案

### 錯誤 1：`ModuleNotFoundError: No module named 'app'`

**原因**：Root Directory 設置錯誤

**解決**：
- 設置 Root Directory 為 `backend`

### 錯誤 2：`Could not find a version that satisfies the requirement`

**原因**：依賴版本不兼容或不存在

**解決**：
- 檢查 `requirements.txt` 中的版本號
- 嘗試移除版本號，讓 pip 自動選擇：
  ```txt
  fastapi
  uvicorn[standard]
  supabase
  ```

### 錯誤 3：`ERROR: Failed building wheel for ...`

**原因**：需要編譯的包缺少系統依賴

**解決**：
- 檢查是否有 `lxml`、`psycopg2` 等需要編譯的包
- 可能需要添加 `buildpack` 或使用預編譯的版本

### 錯誤 4：`Port already in use` 或 `Address already in use`

**原因**：啟動命令使用了固定端口

**解決**：
- 使用 `$PORT` 環境變量：
  ```bash
  python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

---

## ✅ 檢查清單

部署前確認：

- [ ] Root Directory 設置為 `backend`
- [ ] `requirements.txt` 存在於 `backend` 目錄
- [ ] `app/main.py` 存在
- [ ] 環境變量已設置（至少 SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY）
- [ ] 啟動命令使用 `$PORT` 而不是固定端口

---

## 🔄 重新部署

如果修改了配置：

1. 進入服務的 **Settings**
2. 修改配置
3. 保存
4. Railway 會自動重新部署
5. 或者手動點擊 **Redeploy**

---

## 📝 推薦配置

### Settings 配置：

- **Root Directory**: `backend`
- **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Healthcheck Path**: `/health`（可選）

### 環境變量（必須）：

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
OPENAI_API_KEY=sk-your-openai-key
```

### 環境變量（可選）：

```env
OPENAI_MODEL=gpt-4o-mini
APP_ENV=production
WEEKLY_REPORT_ENABLED=true
```

---

## 🚨 如果還是不行

1. **複製完整的錯誤日誌**（從 Build Logs）
2. **檢查**：
   - Root Directory 是否正確
   - requirements.txt 是否在正確位置
   - 環境變量是否設置
3. **嘗試**：
   - 刪除服務，重新創建
   - 檢查 GitHub 倉庫是否正確上傳

---

## 💡 調試技巧

### 查看實時日誌：

1. 進入服務頁面
2. 點擊 **View Logs**
3. 可以看到實時輸出

### 本地測試：

在本地測試 Railway 的構建：

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

如果本地可以運行，Railway 應該也可以。

---

需要幫助？把 Build Logs 的錯誤信息發給我，我可以幫你具體分析！

