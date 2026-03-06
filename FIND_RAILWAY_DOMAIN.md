# 🔍 如何找到 Railway 域名

## 📍 方法一：服務概覽頁面（最簡單）

### 步驟：

1. **進入你的 Railway 項目**
2. **點擊服務**（Service）
3. **在服務頁面的頂部**，你會看到：

   ```
   ┌─────────────────────────────────────┐
   │  Service Name                       │
   │  https://ailinks-production.up.railway.app  ← 這裡！
   │  [Copy] [Settings]                  │
   └─────────────────────────────────────┘
   ```

4. **點擊域名旁邊的複製按鈕**，或直接複製域名

---

## 📍 方法二：Networking 標籤

### 步驟：

1. **進入服務頁面**
2. **點擊 Networking 標籤**
3. 你會看到：
   - **Public Domain** 或 **Domains**
   - 域名列表
   - 如果沒有域名，點擊 **Generate Domain** 或 **Add Domain**

---

## 📍 方法三：Settings → Networking

### 步驟：

1. **進入服務的 Settings**
2. **找到 Networking 部分**
3. 會顯示當前的域名
4. 如果沒有，點擊 **Generate Domain**

---

## 🎯 如果還沒有域名

### 生成域名：

1. **進入服務頁面**
2. **點擊 Networking 標籤**（或 Settings → Networking）
3. **點擊 "Generate Domain"** 或 **"Add Domain"** 按鈕
4. Railway 會自動生成一個域名，格式類似：
   - `ailinks-production.up.railway.app`
   - `your-service-name.up.railway.app`

---

## ✅ 找到域名後

### 更新 Android App

在 `ShareActivity.kt` 中：

```kotlin
private val API_URL = "https://你的域名.up.railway.app/api/links"
```

例如：
```kotlin
private val API_URL = "https://ailinks-production.up.railway.app/api/links"
```

### 測試 API

在瀏覽器訪問：
```
https://你的域名.up.railway.app/docs
```

應該能看到 FastAPI 文檔頁面。

---

## 📸 界面位置示意

### Railway 服務頁面結構：

```
服務頁面
├── 頂部：域名顯示 ← 最明顯的位置
├── Deployments
├── Networking ← 也在這裡
├── Settings
│   └── Networking ← 或者這裡
├── Variables
└── Logs
```

---

## 💡 提示

- 域名通常在服務頁面的**最頂部**，很明顯
- 如果服務還在部署中，可能還沒有域名
- 域名格式：`服務名-隨機字符.up.railway.app`

---

## 🚨 如果找不到

1. **確認服務已部署成功**（Deployments 顯示綠色 ✅）
2. **等待幾分鐘**，域名可能需要時間生成
3. **檢查 Networking 標籤**，點擊 Generate Domain

告訴我你現在在 Railway 的哪個頁面，我可以更精確地指導你！

