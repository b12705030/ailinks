# 🔧 Railway 構建錯誤詳細修復指南

## ❌ 錯誤：railpack process exited with an error

這個錯誤通常有幾個原因，讓我們逐一排查：

---

## 🔍 排查步驟

### 步驟 1：確認文件已上傳到 GitHub

檢查 GitHub 倉庫中是否有這些文件：

1. 打開你的 GitHub 倉庫
2. 進入 `backend` 目錄
3. 確認能看到：
   - ✅ `Procfile`
   - ✅ `runtime.txt`
   - ✅ `requirements.txt`
   - ✅ `app/` 目錄

**如果沒有**，需要上傳：

```bash
cd C:\Users\tinti\Desktop\ailinks
git add backend/Procfile backend/runtime.txt
git commit -m "Add Railway config files"
git push
```

### 步驟 2：確認 Railway Root Directory

在 Railway：

1. 進入服務的 **Settings**
2. 找到 **Root Directory** 或 **Source**
3. **必須設置為**：`backend`（沒有斜杠）
4. 保存

### 步驟 3：檢查 Procfile 格式

確認 `backend/Procfile` 的內容是：

```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**重要**：
- 沒有空行
- 沒有多餘的空格
- `$PORT` 必須大寫

### 步驟 4：手動設置啟動命令

如果 Procfile 不工作，在 Railway Settings 中手動設置：

1. 進入 **Settings**
2. 找到 **Start Command** 或 **Command**
3. 設置為：
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

---

## 🛠️ 替代方案：使用 nixpacks.toml

如果 Procfile 還是不工作，創建 `backend/nixpacks.toml`：

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

然後上傳到 GitHub。

---

## 🔄 重新部署步驟

### 方法 1：自動重新部署

1. 確保所有文件已上傳到 GitHub
2. Railway 會自動檢測到新提交
3. 等待自動重新部署

### 方法 2：手動重新部署

1. 進入 Railway 服務頁面
2. 點擊 **Deployments** 標籤
3. 點擊 **Redeploy** 或 **Deploy**

### 方法 3：觸發新部署

在 GitHub 做一個小改動（比如在 README 加個空格），然後提交：

```bash
git commit --allow-empty -m "Trigger Railway redeploy"
git push
```

---

## 📋 完整檢查清單

在重新部署前，確認：

- [ ] `backend/Procfile` 存在且內容正確
- [ ] `backend/runtime.txt` 存在
- [ ] `backend/requirements.txt` 存在
- [ ] `backend/app/main.py` 存在
- [ ] 所有文件已提交到 GitHub
- [ ] Railway Root Directory = `backend`
- [ ] 環境變量已設置（至少 3 個必須的）

---

## 🚨 如果還是不行

### 查看詳細錯誤

1. 進入 Railway **Deployments**
2. 點擊失敗的部署
3. 查看 **Build Logs**
4. 找到具體的錯誤信息（通常是紅色的）

### 常見錯誤信息

**錯誤 1**：`No such file or directory: Procfile`
- **解決**：確認 Procfile 在 `backend` 目錄，不是根目錄

**錯誤 2**：`ModuleNotFoundError: No module named 'app'`
- **解決**：確認 Root Directory 設置為 `backend`

**錯誤 3**：`Port already in use`
- **解決**：確認使用 `$PORT` 而不是固定端口

**錯誤 4**：`Could not find a version that satisfies the requirement`
- **解決**：檢查 `requirements.txt` 中的依賴版本

---

## 💡 快速測試

在本地測試 Railway 的構建過程：

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

如果本地可以運行，Railway 應該也可以。

---

## 🎯 最可能的原因

根據經驗，最常見的原因是：

1. **Root Directory 沒有設置** - 佔 60%
2. **Procfile 不在正確位置** - 佔 30%
3. **環境變量缺失** - 佔 10%

---

## 📝 需要的信息

如果還是不行，請提供：

1. **Build Logs 的完整錯誤信息**（複製紅色部分）
2. **Root Directory 設置**（截圖或告訴我是什麼）
3. **GitHub 倉庫中 backend 目錄的文件列表**

有了這些信息，我可以給出更精確的解決方案！

