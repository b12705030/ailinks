# 🧹 完整清理和重建指南

## ⚠️ 重要：必須完全清理

如果修改後還是出現舊錯誤，需要**完全清理項目**。

---

## 📋 步驟 1：在 Android Studio 中清理

### 方法 A：使用菜單（推薦）

1. **Clean Project**
   - `Build` → `Clean Project`
   - 等待完成

2. **Invalidate Caches / Restart**
   - `File` → `Invalidate Caches...`
   - 勾選所有選項
   - 點擊 `Invalidate and Restart`
   - Android Studio 會重啟

3. **Rebuild Project**
   - `Build` → `Rebuild Project`
   - 等待編譯完成

### 方法 B：手動刪除構建文件

1. **關閉 Android Studio**

2. **刪除構建文件夾**：
   - 刪除 `app/build/` 文件夾
   - 刪除 `.gradle/` 文件夾（如果存在）

3. **重新打開 Android Studio**

4. **Sync Project**
   - 點擊 `Sync Now` 或
   - `File` → `Sync Project with Gradle Files`

5. **Rebuild Project**
   - `Build` → `Rebuild Project`

---

## 📋 步驟 2：確認文件已更新

### 檢查 ShareActivity.kt

打開 `app/src/main/java/com/tca940120/ailinks/ShareActivity.kt`

確認第 7 行和第 19 行：

```kotlin
import androidx.activity.ComponentActivity  // 第 7 行

class ShareActivity : ComponentActivity() {  // 第 19 行
```

**不應該是**：
```kotlin
import androidx.appcompat.app.AppCompatActivity  // ❌ 錯誤
class ShareActivity : AppCompatActivity() {  // ❌ 錯誤
```

---

## 📋 步驟 3：重新安裝

### 方法 A：卸載舊版本

1. **在手機上卸載 App**
   - 設置 → 應用 → Link Collector → 卸載

2. **重新安裝**
   - 在 Android Studio 中運行 App

### 方法 B：直接覆蓋安裝

1. **在 Android Studio 中運行**
   - 點擊綠色 ▶️ 按鈕
   - 選擇你的手機

---

## 🔍 步驟 4：驗證修復

1. **從其他 App 分享連結**
2. **選擇「保存到 Link Collector」**
3. **應該看到 Toast 訊息**（不會崩潰）
4. **打開主 App，刷新列表**
5. **應該能看到剛才分享的連結**

---

## ⚠️ 如果還是出現錯誤

### 檢查 1：確認代碼已保存

- 在 Android Studio 中按 `Ctrl+S` 保存所有文件
- 確認文件標籤沒有 `*` 標記（表示未保存）

### 檢查 2：確認沒有多個 ShareActivity 文件

搜索項目中是否有其他 `ShareActivity.kt` 文件：
- 在 Android Studio 中按 `Ctrl+Shift+F`
- 搜索 `class ShareActivity`
- 確認只有一個文件

### 檢查 3：確認 Gradle 同步成功

- 查看底部狀態欄
- 確認沒有同步錯誤
- 如果有錯誤，點擊 `Sync Now`

---

## 💡 提示

如果修改後立即運行，Android Studio 可能使用緩存的舊版本。**必須先 Clean，再 Rebuild**。

---

## ✅ 完整流程總結

```
1. Clean Project
2. Invalidate Caches / Restart
3. Rebuild Project
4. 卸載手機上的舊版本
5. 重新安裝
6. 測試分享功能
```

按照這個順序操作，應該可以解決問題！

