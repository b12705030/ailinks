# 📱 Android App 完整設置指南

## 🎯 使用 Kotlin DSL (build.gradle.kts)

如果你創建項目時選擇了 Kotlin DSL，文件會是 `build.gradle.kts`，語法稍有不同。

---

## 📝 步驟 1：添加依賴

編輯 `app/build.gradle.kts`，在 `dependencies` 區塊中添加：

```kotlin
dependencies {
    // ... 其他依賴
    
    // 添加這兩行
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```

**注意**：Kotlin DSL 使用雙引號和括號 `implementation("...")`，而不是單引號。

---

## 📝 步驟 2：配置 AndroidManifest.xml

在 `app/src/main/AndroidManifest.xml` 中添加：

```xml
<manifest ...>
    <application ...>
        <!-- 原有的 Activity -->
        <activity
            android:name=".MainActivity"
            ...>
        </activity>
        
        <!-- 添加這個 ShareActivity -->
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
    </application>
</manifest>
```

---

## 📝 步驟 3：創建 ShareActivity

在 `app/src/main/java/com/yourname/linkcollector/` 目錄下創建 `ShareActivity.kt`：

```kotlin
package com.yourname.linkcollector

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
    
    // ⚠️ 重要：替換為你的雲端 API URL
    private val API_URL = "https://your-app.up.railway.app/api/links"
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT) ?: ""
        
        if (sharedText.isNotEmpty()) {
            val url = extractUrl(sharedText)
            val sourceApp = getSourceApp(intent)
            
            if (url.isNotEmpty()) {
                saveLink(url, sourceApp)
            } else {
                showToast("未找到有效的 URL")
                finish()
            }
        } else {
            showToast("未收到分享內容")
            finish()
        }
    }
    
    private fun extractUrl(text: String): String {
        val urlPattern = Pattern.compile(
            "(https?://[\\w\\-]+(\\.[\\w\\-]+)+([\\w\\-\\.,@?^=%&:/~\\+#]*[\\w\\-\\@?^=%&/~\\+#])?)",
            Pattern.CASE_INSENSITIVE
        )
        val matcher = urlPattern.matcher(text)
        return if (matcher.find()) matcher.group(1) else ""
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
                    .url(API_URL)
                    .post(requestBody)
                    .build()
                
                val response = client.newCall(request).execute()
                
                runOnUiThread {
                    if (response.isSuccessful) {
                        showToast("✅ 連結已保存！")
                    } else {
                        showToast("❌ 保存失敗：${response.message}")
                    }
                    finish()
                }
            } catch (e: Exception) {
                runOnUiThread {
                    showToast("❌ 錯誤：${e.message}")
                    finish()
                }
            }
        }
    }
    
    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
```

**重要**：記得將 `com.yourname.linkcollector` 替換為你的實際 package name！

---

## 📝 步驟 4：添加網絡權限

在 `app/src/main/AndroidManifest.xml` 的 `<manifest>` 標籤內添加：

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    ...>
    
    <!-- 添加網絡權限 -->
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application ...>
        ...
    </application>
</manifest>
```

---

## 📝 步驟 5：同步項目

1. 點擊 Android Studio 頂部的 **Sync Now** 按鈕
2. 等待 Gradle 同步完成
3. 確保沒有錯誤

---

## 📝 步驟 6：編譯 APK

### 方法一：Build APK

1. 點擊 **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
2. 等待編譯完成
3. 點擊 **locate** 找到 APK 文件
4. 將 APK 傳到手機並安裝

### 方法二：直接運行（如果有 USB 調試）

1. 連接手機到電腦
2. 啟用手機的 USB 調試
3. 點擊 **Run** 按鈕（綠色播放圖標）
4. 選擇你的手機
5. 自動安裝並運行

---

## 🔧 常見問題

### Q: Gradle 同步失敗？

**錯誤**：`Could not resolve com.squareup.okhttp3:okhttp`

**解決**：
1. 檢查網絡連接
2. 在 `settings.gradle.kts` 確認有正確的倉庫：
   ```kotlin
   repositories {
       google()
       mavenCentral()
   }
   ```

### Q: 找不到 ShareActivity？

**解決**：
1. 確認文件在正確的目錄：`app/src/main/java/com/yourname/linkcollector/ShareActivity.kt`
2. 確認 package name 正確
3. 重新同步項目

### Q: 編譯錯誤？

**常見錯誤**：
- **未導入依賴**：確認 `build.gradle.kts` 中的依賴已添加
- **語法錯誤**：確認使用 Kotlin DSL 語法（雙引號）
- **權限問題**：確認已添加 INTERNET 權限

---

## ✅ 完成後測試

1. 安裝 APK 到手機
2. 在 Facebook 找到一個連結
3. 點擊「分享」
4. 應該能看到「保存到 Link Collector」選項
5. 選擇後，應該會顯示「✅ 連結已保存！」

---

## 🎉 完成！

現在你可以隨時從任何 App 分享連結到你的系統了！

如果有任何問題，請檢查：
- Android Studio 的 Build 輸出
- Logcat 中的錯誤信息
- API URL 是否正確

