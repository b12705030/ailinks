# 🌐 Railway 公開域名設置

## ❌ 內部域名 vs ✅ 公開域名

### 內部域名（不能用）
```
ailinks.railway.internal  ← 這個只能內部使用
```

### 公開域名（要用這個）
```
ailinks-production.up.railway.app  ← 這個可以從外部訪問
```

---

## 🔍 如何找到/生成公開域名

### 方法一：Networking 標籤

1. **進入服務頁面**
2. **點擊 Networking 標籤**
3. 你會看到：
   - **Public Domain** 部分
   - 如果沒有，點擊 **"Generate Domain"** 或 **"Add Domain"** 按鈕
4. Railway 會生成一個公開域名，格式：
   ```
   ailinks-production.up.railway.app
   ```
   或
   ```
   你的服務名-隨機字符.up.railway.app
   ```

### 方法二：Settings → Networking

1. **進入 Settings**
2. **找到 Networking 部分**
3. **點擊 "Generate Domain"**

### 方法三：服務概覽頁

1. **在服務頁面頂部**
2. 如果有公開域名，會直接顯示
3. 格式：`https://xxx.up.railway.app`

---

## 🚀 生成公開域名步驟

### 詳細步驟：

1. **進入你的服務頁面**
2. **點擊 Networking 標籤**（在頂部標籤欄）
3. **找到 "Public Domain" 或 "Domains" 部分**
4. **點擊 "Generate Domain" 按鈕**
5. **等待幾秒鐘**，Railway 會生成一個域名
6. **複製這個域名**

生成的域名格式：
```
https://ailinks-production-xxxx.up.railway.app
```

---

## ✅ 找到公開域名後

### 更新 Android App

在 `ShareActivity.kt` 中：

```kotlin
private val API_URL = "https://ailinks-production-xxxx.up.railway.app/api/links"
```

（替換為你的實際域名）

### 測試

在瀏覽器訪問：
```
https://你的公開域名.up.railway.app/docs
```

應該能看到 API 文檔。

---

## 🔍 如何區分

### 內部域名特徵：
- 結尾是 `.railway.internal`
- 只能在同一 Railway 項目內使用
- 不能用於外部訪問

### 公開域名特徵：
- 結尾是 `.up.railway.app`
- 可以從任何地方訪問
- 用於外部 API 調用

---

## 💡 如果找不到 Generate Domain 按鈕

可能的原因：
1. **服務還在部署中** - 等待部署完成
2. **界面版本不同** - 可能在 Settings → Networking
3. **需要付費計劃** - 免費版應該也有，但可能有限制

**解決**：
- 等待部署完成（Deployments 顯示綠色 ✅）
- 刷新頁面
- 檢查不同標籤

---

## 🎯 快速檢查

1. **進入服務頁面**
2. **查看頂部** - 是否有 `https://xxx.up.railway.app` 格式的域名
3. **點擊 Networking 標籤** - 查看 Public Domain
4. **如果沒有，點擊 Generate Domain**

告訴我你在 Networking 標籤看到了什麼，我可以幫你找到正確的域名！

