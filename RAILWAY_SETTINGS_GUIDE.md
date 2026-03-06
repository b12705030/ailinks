# 🚂 Railway 設置詳細指南

## 📍 如何找到 Settings

### 方法一：從服務頁面進入

1. **登錄 Railway** 後，進入你的項目
2. 點擊你創建的**服務**（Service）
3. 在服務頁面，你會看到幾個標籤：
   - **Deployments**
   - **Metrics**
   - **Settings** ← 點擊這個
   - **Variables**
   - **Logs**

### 方法二：如果看不到 Settings

如果創建項目後還沒有服務，需要先：

1. **創建服務**：
   - 在項目頁面，點擊 **+ New**
   - 選擇 **GitHub Repo**
   - 選擇你的 `ailinks` 倉庫
   - Railway 會自動創建服務

2. **等待服務創建完成**後，點擊服務進入

---

## ⚙️ Settings 頁面內容

進入 Settings 後，你應該能看到：

### 1. Root Directory（根目錄）

**位置**：Settings 頁面的 **General** 部分

**如果看不到**：
- 可能在新版本的 Railway 中，這個選項在 **Deploy** 標籤
- 或者需要點擊 **Configure** 按鈕

**設置方法**：
1. 找到 **Root Directory** 或 **Source** 選項
2. 輸入：`backend`
3. 保存

### 2. Generate Domain（生成域名）

**位置**：Settings 頁面的 **Networking** 或 **Domains** 部分

**如果找不到**：
- 可能在 **Networking** 標籤
- 或者服務部署成功後才會出現
- 或者在新版本中，域名會自動生成

**替代方法**：
1. 進入 **Networking** 標籤
2. 點擊 **Generate Domain** 或 **Add Domain**
3. Railway 會自動生成一個域名

---

## 🔄 Railway 新版本界面

如果界面看起來不同，可能是新版本。試試這些位置：

### 查找 Root Directory：

1. **方法 A**：點擊服務 → **Deploy** 標籤 → 找到 **Source** 或 **Root Directory**
2. **方法 B**：點擊服務 → **Settings** → **General** → **Source**
3. **方法 C**：在服務頁面，點擊右上角的 **⚙️** 圖標

### 查找 Domain：

1. **方法 A**：點擊服務 → **Networking** 標籤
2. **方法 B**：點擊服務 → **Settings** → **Networking**
3. **方法 C**：部署成功後，在服務概覽頁面會顯示域名

---

## 🎯 快速檢查清單

### 步驟 1：確認服務已創建

- [ ] 項目中有服務（Service）
- [ ] 服務狀態不是 "Creating"

### 步驟 2：進入服務設置

- [ ] 點擊服務進入詳情頁
- [ ] 能看到多個標籤（Deployments, Settings, Variables 等）

### 步驟 3：查找配置選項

**Root Directory**：
- [ ] 在 Settings → General
- [ ] 或在 Deploy 標籤
- [ ] 設置為 `backend`

**Domain**：
- [ ] 在 Networking 標籤
- [ ] 或在服務概覽頁面
- [ ] 點擊 Generate Domain

---

## 💡 如果還是找不到

### 選項 1：使用 Railway CLI

如果網頁界面找不到，可以使用命令行：

```bash
# 安裝 Railway CLI
npm i -g @railway/cli

# 登錄
railway login

# 進入項目目錄
cd backend

# 部署
railway up
```

### 選項 2：檢查服務狀態

1. 確認服務已經創建
2. 等待服務完全初始化（可能需要幾分鐘）
3. 刷新頁面

### 選項 3：重新創建服務

如果服務有問題：

1. 刪除現有服務
2. 重新創建：
   - 點擊 **+ New** → **GitHub Repo**
   - 選擇 `ailinks` 倉庫
   - 這次 Railway 可能會自動檢測到 `backend` 目錄

---

## 📸 界面位置示意

### 舊版 Railway：

```
項目頁面
└── 服務 (Service)
    ├── Deployments
    ├── Settings ← 點擊這裡
    │   ├── General
    │   │   └── Root Directory ← 在這裡設置
    │   └── Networking
    │       └── Generate Domain ← 在這裡
    ├── Variables
    └── Logs
```

### 新版 Railway：

```
項目頁面
└── 服務 (Service)
    ├── Deploy ← 可能在這裡
    │   └── Source / Root Directory
    ├── Networking ← Domain 在這裡
    ├── Variables
    └── Settings
```

---

## 🚨 最簡單的方法

如果找不到這些選項，試試這個：

1. **讓 Railway 自動檢測**：
   - 刪除現有服務
   - 重新創建服務
   - 選擇 GitHub 倉庫時，Railway 可能會自動檢測到 `backend` 目錄

2. **或者先部署看看**：
   - 不設置 Root Directory
   - 直接部署
   - 如果失敗，錯誤日誌會告訴你問題在哪裡

---

## ❓ 需要幫助？

告訴我：
1. 你現在在 Railway 的哪個頁面？
2. 能看到哪些標籤？（Deployments, Settings, Variables 等）
3. 服務的狀態是什麼？（Creating, Building, Running 等）

我可以根據你的具體情況給出更精確的指導！

