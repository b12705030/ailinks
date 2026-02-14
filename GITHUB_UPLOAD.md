# 📤 上傳到 GitHub 完整指南

## 🎯 前置準備

### 1. 安裝 Git

如果還沒安裝 Git：

**Windows**:
- 下載 [Git for Windows](https://git-scm.com/download/win)
- 安裝時選擇默認選項即可

**檢查是否已安裝**：
```bash
git --version
```

如果顯示版本號，說明已安裝。

### 2. 註冊 GitHub 帳號

1. 前往 [GitHub](https://github.com)
2. 註冊新帳號（如果還沒有）
3. 完成郵箱驗證

---

## 🚀 上傳步驟

### 步驟 1：在 GitHub 創建新倉庫

1. 登錄 GitHub
2. 點擊右上角 **+** → **New repository**
3. 填寫信息：
   - **Repository name**: `ailinks`（或你喜歡的名字）
   - **Description**: `AI 智能連結收集系統`（可選）
   - **Visibility**: 
     - **Public**（公開，免費）
     - **Private**（私有，需要付費或學生包）
   - **不要**勾選 "Initialize this repository with a README"（因為我們已經有文件了）
4. 點擊 **Create repository**

### 步驟 2：在本地初始化 Git

打開 PowerShell 或 Terminal，進入項目目錄：

```bash
cd C:\Users\tinti\Desktop\ailinks
```

初始化 Git：

```bash
git init
```

### 步驟 3：配置 Git（如果第一次使用）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的email@example.com"
```

### 步驟 4：添加文件

```bash
# 添加所有文件
git add .

# 或者只添加特定文件
git add backend/
git add frontend/
git add supabase/
git add *.md
```

### 步驟 5：創建 .gitignore（如果還沒有）

確保 `.gitignore` 文件存在，內容應該包含：

```
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
ENV/

# Node
node_modules/
npm-debug.log*

# Environment
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### 步驟 6：提交文件

```bash
git commit -m "Initial commit: Link Collector project"
```

### 步驟 7：連接到 GitHub 倉庫

```bash
# 替換為你的實際 GitHub 用戶名和倉庫名
git remote add origin https://github.com/你的用戶名/ailinks.git
```

例如：
```bash
git remote add origin https://github.com/tinti/ailinks.git
```

### 步驟 8：推送到 GitHub

```bash
# 推送到 main 分支
git branch -M main
git push -u origin main
```

如果提示輸入用戶名和密碼：
- **用戶名**：你的 GitHub 用戶名
- **密碼**：使用 **Personal Access Token**（不是 GitHub 密碼）

---

## 🔑 創建 Personal Access Token

如果 Git 要求密碼，需要創建 Token：

### 步驟：

1. 登錄 GitHub
2. 點擊右上角頭像 → **Settings**
3. 左側菜單 → **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. 點擊 **Generate new token** → **Generate new token (classic)**
6. 填寫：
   - **Note**: `ailinks-deploy`（描述）
   - **Expiration**: 選擇過期時間（或 No expiration）
   - **Select scopes**: 勾選 `repo`（全部倉庫權限）
7. 點擊 **Generate token**
8. **複製 Token**（只顯示一次，要保存好！）
9. 在 Git 要求密碼時，貼上這個 Token

---

## ✅ 驗證上傳成功

1. 刷新你的 GitHub 倉庫頁面
2. 應該能看到所有文件：
   - `backend/`
   - `frontend/`
   - `supabase/`
   - `README.md`
   - 等等

---

## 🔄 之後更新代碼

如果之後修改了代碼，需要再次上傳：

```bash
# 1. 查看修改的文件
git status

# 2. 添加修改的文件
git add .

# 3. 提交
git commit -m "描述你的修改"

# 4. 推送到 GitHub
git push
```

---

## 🚨 常見問題

### Q: `git: command not found`

**解決**：Git 沒有安裝或沒有添加到 PATH，重新安裝 Git。

### Q: `fatal: remote origin already exists`

**解決**：已經添加過 remote，可以：
```bash
# 查看現有的 remote
git remote -v

# 如果需要修改
git remote set-url origin https://github.com/你的用戶名/ailinks.git
```

### Q: `Permission denied`

**解決**：
1. 確認 GitHub 用戶名正確
2. 使用 Personal Access Token 而不是密碼
3. 確認 Token 有 `repo` 權限

### Q: 想忽略某些文件

編輯 `.gitignore` 文件，添加要忽略的文件或目錄。

---

## 📝 快速命令參考

```bash
# 初始化
git init

# 添加文件
git add .

# 提交
git commit -m "你的提交信息"

# 連接 GitHub
git remote add origin https://github.com/你的用戶名/ailinks.git

# 推送到 GitHub
git branch -M main
git push -u origin main

# 之後更新
git add .
git commit -m "更新信息"
git push
```

---

## 🎉 完成！

上傳完成後，你就可以：
1. ✅ 在 Railway 部署時選擇這個倉庫
2. ✅ 在 Vercel 部署前端時選擇這個倉庫
3. ✅ 隨時更新代碼並推送到 GitHub

---

## 💡 提示

- **不要上傳 `.env` 文件**（已在 `.gitignore` 中）
- **定期提交**：每次完成一個功能就提交一次
- **寫清楚的提交信息**：方便之後查看歷史

需要幫助？告訴我你卡在哪一步！

