# 🔧 Railway "railpack process exited" 錯誤修復

## ❌ 錯誤原因

`railpack process exited with an error` 通常表示：
- Railway 無法自動檢測項目類型
- 缺少必要的配置文件
- 構建命令不正確

## ✅ 解決方案

### 步驟 1：創建 Procfile

在 `backend` 目錄創建 `Procfile` 文件（沒有擴展名）：

**文件位置**：`backend/Procfile`

**內容**：
```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

這個文件告訴 Railway 如何啟動你的應用。

### 步驟 2：創建 runtime.txt（可選但推薦）

在 `backend` 目錄創建 `runtime.txt`：

**文件位置**：`backend/runtime.txt`

**內容**：
```
python-3.11.0
```

這指定了 Python 版本。

### 步驟 3：確認文件結構

確保 `backend` 目錄下有這些文件：

```
backend/
├── Procfile          ← 新建
├── runtime.txt       ← 新建
├── requirements.txt  ← 已有
├── run.py           ← 已有
└── app/
    ├── main.py
    └── ...
```

### 步驟 4：上傳到 GitHub

如果還沒上傳這些新文件：

```bash
cd C:\Users\tinti\Desktop\ailinks
git add backend/Procfile backend/runtime.txt
git commit -m "Add Railway deployment files"
git push
```

### 步驟 5：在 Railway 設置

1. **進入服務的 Settings**
2. **確認 Root Directory** 設置為：`backend`
3. **Start Command**（如果有的話）可以留空，因為 Procfile 會處理

### 步驟 6：重新部署

1. Railway 會自動檢測到新的提交
2. 或者手動點擊 **Redeploy**
3. 等待構建完成

## 🔍 如果還是不行

### 檢查 1：確認 Root Directory

在 Railway 服務的 Settings 中：
- **Root Directory** 必須是：`backend`
- 不是 `backend/` 或 `/backend`

### 檢查 2：查看詳細日誌

1. 進入 **Deployments** 標籤
2. 點擊失敗的部署
3. 查看 **Build Logs**
4. 找到具體的錯誤信息

### 檢查 3：手動設置啟動命令

如果 Procfile 不工作，在 Settings 中手動設置：

**Start Command**：
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 📝 完整檢查清單

- [ ] `backend/Procfile` 已創建
- [ ] `backend/runtime.txt` 已創建
- [ ] 文件已提交到 GitHub
- [ ] Railway Root Directory 設置為 `backend`
- [ ] 環境變量已設置（至少 SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY）
- [ ] 重新部署

## 🚀 快速修復命令

在項目根目錄運行：

```bash
# 創建 Procfile
echo web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT > backend/Procfile

# 創建 runtime.txt
echo python-3.11.0 > backend/runtime.txt

# 提交到 GitHub
git add backend/Procfile backend/runtime.txt
git commit -m "Add Railway deployment configuration"
git push
```

## 💡 提示

- **Procfile** 必須在 `backend` 目錄，不是項目根目錄
- **Procfile** 沒有文件擴展名
- 使用 `$PORT` 環境變量，不要用固定端口

完成這些步驟後，Railway 應該能正確構建了！

