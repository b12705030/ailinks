# 📱 Android 分享功能設置指南

## 🎯 目標

在滑 Facebook、Instagram、Threads 等 App 時，可以直接「分享」連結到 Link Collector，無需手動複製貼上。

---

## 🚀 方式一：使用 Tasker（最簡單，推薦！）

### 優點
- ✅ **無需開發**，只需要配置
- ✅ 功能強大，可以自動化很多操作
- ✅ 一次設置，永久使用

### 缺點
- ⚠️ 需要付費購買 Tasker（約 $3.49）
- ⚠️ 需要一些配置時間

### 設置步驟

#### 1. 安裝 Tasker

從 [Google Play](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) 購買並安裝 Tasker

#### 2. 創建 Profile（觸發條件）

1. 打開 Tasker
2. 點擊右下角 **+** 號
3. 選擇 **Event**
4. 選擇 **Intent Received**
5. 配置：
   - **Action**: `android.intent.action.SEND`
   - **MIME Type**: `text/plain`
6. 點擊返回，給 Profile 命名，例如：`分享到 Link Collector`

#### 3. 創建 Task（執行動作）

1. Tasker 會自動提示創建 Task，點擊 **New Task**
2. 命名為：`保存連結到 Link Collector`
3. 添加動作：

   **動作 1：變量設置**
   - 點擊 **+** → **Variables** → **Variable Set**
   - **Name**: `%shared_url`
   - **To**: `%text`（這是分享的文本）

   **動作 2：HTTP Request**
   - 點擊 **+** → **Net** → **HTTP Request**
   - **Method**: POST
   - **URL**: `http://192.168.1.105:8000/api/links`
     （替換為你的後端地址，如果是雲端部署就用雲端地址）
   - **Headers**:
     ```
     Content-Type: application/json
     ```
   - **Body**:
     ```json
     {
       "url": "%shared_url",
       "source_app": "%app_package"
     }
     ```

   **動作 3：通知（可選）**
   - 點擊 **+** → **Alert** → **Notify**
   - **Title**: 連結已保存
   - **Text**: `%shared_url`

#### 4. 測試

1. 在 Facebook 或其他 App 中找到一個連結
2. 點擊「分享」
3. 選擇「Tasker」或「分享到 Link Collector」
4. 應該會自動發送到你的 API

---

## 📱 方式二：開發簡單的 Android App（最完整）

### 優點
- ✅ 完全自定義
- ✅ 可以添加更多功能
- ✅ 可以發布到 Play Store

### 缺點
- ⚠️ 需要 Android 開發知識
- ⚠️ 需要時間開發

### 快速開發指南

#### 1. 創建 Android 項目

使用 Android Studio 創建新項目，最低 SDK 21

#### 2. 配置 AndroidManifest.xml

在 `AndroidManifest.xml` 中添加 Share Target：

```xml
<activity
    android:name=".ShareActivity"
    android:label="保存到 Link Collector"
    android:exported="true"
    android:theme="@android:style/Theme.Translucent.NoTitleBar">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
</activity>
```

#### 3. 創建 ShareActivity

```kotlin
package com.yourpackage.linkcollector

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.regex.Pattern

class ShareActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT) ?: ""
        val sharedTitle = intent.getStringExtra(Intent.EXTRA_SUBJECT) ?: ""
        
        if (sharedText.isNotEmpty()) {
            val url = extractUrl(sharedText)
            val sourceApp = getSourceApp(intent)
            
            if (url.isNotEmpty()) {
                saveLink(url, sourceApp)
            } else {
                Toast.makeText(this, "未找到有效的 URL", Toast.LENGTH_SHORT).show()
                finish()
            }
        } else {
            Toast.makeText(this, "未收到分享內容", Toast.LENGTH_SHORT).show()
            finish()
        }
    }
    
    private fun extractUrl(text: String): String {
        val urlPattern = Pattern.compile(
            "https?://[\\w\\-]+(\\.[\\w\\-]+)+([\\w\\-\\.,@?^=%&:/~\\+#]*[\\w\\-\\@?^=%&/~\\+#])?",
            Pattern.CASE_INSENSITIVE
        )
        val matcher = urlPattern.matcher(text)
        return if (matcher.find()) matcher.group() else ""
    }
    
    private fun getSourceApp(intent: Intent): String {
        val packageName = intent.`package` ?: return "unknown"
        return when {
            packageName.contains("instagram") -> "instagram"
            packageName.contains("facebook") || packageName.contains("katana") -> "facebook"
            packageName.contains("messenger") -> "messenger"
            packageName.contains("threads") -> "threads"
            packageName.contains("twitter") -> "twitter"
            else -> "unknown"
        }
    }
    
    private fun saveLink(url: String, sourceApp: String) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val client = OkHttpClient()
                val json = JSONObject().apply {
                    put("url", url)
                    put("source_app", sourceApp)
                }
                
                val requestBody = json.toString()
                    .toRequestBody("application/json".toMediaType())
                
                val request = Request.Builder()
                    .url("http://192.168.1.105:8000/api/links") // 替換為你的 API URL
                    .post(requestBody)
                    .build()
                
                val response = client.newCall(request).execute()
                
                runOnUiThread {
                    if (response.isSuccessful) {
                        Toast.makeText(
                            this@ShareActivity,
                            "連結已保存！",
                            Toast.LENGTH_SHORT
                        ).show()
                    } else {
                        Toast.makeText(
                            this@ShareActivity,
                            "保存失敗：${response.message}",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                    finish()
                }
            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(
                        this@ShareActivity,
                        "錯誤：${e.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                    finish()
                }
            }
        }
    }
}
```

#### 4. 添加依賴

在 `build.gradle` 中添加：

```gradle
dependencies {
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'
}
```

#### 5. 編譯並安裝

編譯 APK 並安裝到手機上即可。

---

## 🔧 方式三：使用 Shortcuts App（中等難度）

### 步驟

1. 安裝 [Shortcuts](https://play.google.com/store/apps/details?id=com.rhmsoft.shortcuts)
2. 創建新的 Shortcut
3. 設置 Intent Action 為 `android.intent.action.SEND`
4. 設置 Intent Data 為 `text/plain`
5. 添加 HTTP Request 動作，調用你的 API

---

## 💡 推薦方案

### 如果你：
- **不想開發** → 使用 **Tasker**（方式一）
- **想學習 Android 開發** → 開發 **Android App**（方式二）
- **想快速測試** → 使用 **Shortcuts**（方式三）

### 最推薦：Tasker

因為：
- ✅ 設置簡單（10 分鐘搞定）
- ✅ 功能強大（可以添加更多自動化）
- ✅ 不需要編程知識
- ✅ 一次購買，永久使用

---

## 🔍 注意事項

### 本地網絡訪問

如果你的後端在本地（`192.168.1.105:8000`），手機必須和電腦在同一 Wi-Fi 才能使用。

### 雲端部署

如果部署到 Railway/Vercel，就可以隨時隨地使用，不需要在同一網絡。

### API URL 配置

在 Tasker 或 Android App 中，記得將 API URL 改為：
- **本地**: `http://192.168.1.105:8000/api/links`
- **雲端**: `https://your-backend.railway.app/api/links`

---

## 🎉 完成！

設置完成後，你就可以：
1. 在 Facebook 看到喜歡的連結
2. 點擊「分享」
3. 選擇「Link Collector」或「Tasker」
4. 自動保存到你的系統！

享受自動化的便利吧！🚀

