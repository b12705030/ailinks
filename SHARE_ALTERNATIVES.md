# 📱 不用 Tasker 的分享方案

## 🎯 方案對比

| 方案 | 難度 | 費用 | 便利性 | 推薦度 |
|------|------|------|--------|--------|
| **Android App** | ⭐⭐⭐ | 免費 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Shortcuts App** | ⭐⭐ | 免費 | ⭐⭐⭐ | ⭐⭐⭐ |
| **瀏覽器書籤** | ⭐ | 免費 | ⭐⭐ | ⭐⭐ |
| **PWA + 分享 API** | ⭐⭐⭐ | 免費 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🚀 方案一：開發簡單的 Android App（最推薦）

### 優點
- ✅ **完全免費**
- ✅ **最方便**，一鍵分享
- ✅ **完全自定義**
- ✅ **可以發布到 Play Store**

### 缺點
- ⚠️ 需要一些 Android 開發知識
- ⚠️ 需要 Android Studio

### 快速開始

#### 1. 安裝 Android Studio

下載並安裝 [Android Studio](https://developer.android.com/studio)

#### 2. 創建新項目

1. 打開 Android Studio
2. **New Project** → **Empty Activity**
3. 設置：
   - Name: `LinkCollector`
   - Package: `com.yourname.linkcollector`
   - Language: **Kotlin**
   - Minimum SDK: **API 21** (Android 5.0)

#### 3. 添加依賴

**如果是 `build.gradle` (Groovy)**：
```gradle
dependencies {
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'
}
```

**如果是 `build.gradle.kts` (Kotlin DSL)**：
```kotlin
dependencies {
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```

#### 4. 配置 AndroidManifest.xml

在 `app/src/main/AndroidManifest.xml` 中添加：

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

#### 5. 創建 ShareActivity

創建 `app/src/main/java/com/yourname/linkcollector/ShareActivity.kt`：

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
    
    // 在這裡設置你的雲端 API URL
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
                    .url(API_URL)  // 使用雲端地址
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

#### 6. 編譯並安裝

1. 點擊 **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
2. 等待編譯完成
3. 將 APK 傳到手機並安裝
4. 或者使用 USB 調試直接安裝

#### 7. 使用

1. 在 Facebook 找到連結
2. 點擊「分享」
3. 選擇「保存到 Link Collector」
4. 自動保存！

---

## 🔧 方案二：使用 Shortcuts App（免費替代）

### 優點
- ✅ **完全免費**
- ✅ 不需要開發
- ✅ 設置相對簡單

### 缺點
- ⚠️ 功能有限
- ⚠️ 可能需要一些配置時間

### 步驟

1. **安裝 Shortcuts**
   - [Google Play 下載](https://play.google.com/store/apps/details?id=com.rhmsoft.shortcuts)

2. **創建 Shortcut**
   - 打開 Shortcuts
   - 點擊 **+** 創建新的
   - 命名為「保存到 Link Collector」

3. **設置 Intent**
   - **Intent Action**: `android.intent.action.SEND`
   - **MIME Type**: `text/plain`

4. **添加 HTTP Request**
   - 添加 **HTTP Request** 動作
   - **Method**: POST
   - **URL**: `https://your-app.up.railway.app/api/links`
   - **Headers**: `Content-Type: application/json`
   - **Body**:
     ```json
     {
       "url": "%text",
       "source_app": "facebook"
     }
     ```

5. **保存並使用**
   - 在 Facebook 分享時選擇這個 Shortcut

---

## 🌐 方案三：使用瀏覽器書籤（最簡單但需手動）

### 優點
- ✅ **完全免費**
- ✅ **不需要安裝任何東西**
- ✅ **設置超簡單**

### 缺點
- ⚠️ 需要手動複製貼上
- ⚠️ 不如自動分享方便

### 步驟

1. **創建書籤**

在手機瀏覽器中創建一個書籤，URL 為：

```javascript
javascript:(function(){
  const url = prompt('請貼上連結：');
  if(url) {
    fetch('https://your-app.up.railway.app/api/links', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({url: url, source_app: 'manual'})
    }).then(() => alert('✅ 已保存！')).catch(() => alert('❌ 保存失敗'));
  }
})();
```

2. **使用**
   - 在 Facebook 複製連結
   - 打開書籤
   - 貼上連結
   - 點擊確定

---

## 📱 方案四：PWA + Web Share API（現代瀏覽器）

### 優點
- ✅ **不需要安裝 App**
- ✅ **現代瀏覽器原生支持**
- ✅ **體驗接近原生 App**

### 缺點
- ⚠️ 需要修改前端代碼
- ⚠️ 不是所有瀏覽器都支持

### 實現步驟

#### 1. 添加 PWA 支持

創建 `frontend/public/manifest.json`：

```json
{
  "name": "Link Collector",
  "short_name": "LinkCollector",
  "description": "AI 智能連結收集系統",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ],
  "share_target": {
    "action": "/api/share",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url"
    }
  }
}
```

#### 2. 添加分享處理頁面

創建 `frontend/src/pages/SharePage.tsx`：

```typescript
import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { linksApi } from '../api/client'

export default function SharePage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  
  useEffect(() => {
    const url = searchParams.get('url') || searchParams.get('text')
    if (url) {
      linksApi.create({ url, source_app: 'web_share' })
        .then(() => {
          alert('✅ 連結已保存！')
          navigate('/')
        })
        .catch(() => {
          alert('❌ 保存失敗')
          navigate('/')
        })
    }
  }, [searchParams, navigate])
  
  return <div>處理中...</div>
}
```

---

## 💡 推薦方案

### 如果你：
- **會一點編程** → **開發 Android App**（方案一）
- **完全不會編程** → **使用 Shortcuts App**（方案二）
- **想要最簡單** → **瀏覽器書籤**（方案三，但需手動）

### 最推薦：開發 Android App

因為：
- ✅ 一次開發，永久使用
- ✅ 體驗最好
- ✅ 完全免費
- ✅ 可以自定義更多功能

---

## 🎯 快速決策樹

```
想要自動分享？
├─ 是
│  ├─ 會 Android 開發？
│  │  ├─ 是 → 開發 Android App ⭐⭐⭐⭐⭐
│  │  └─ 否 → 使用 Shortcuts App ⭐⭐⭐
│  └─ 不想開發？
│     └─ 使用 Shortcuts App ⭐⭐⭐
└─ 否（可以手動）
   └─ 使用瀏覽器書籤 ⭐⭐
```

---

## 🚀 開始使用

選擇最適合你的方案，按照步驟設置即可！

**推薦順序**：
1. Android App（如果會開發）
2. Shortcuts App（如果不會開發）
3. 瀏覽器書籤（最簡單但需手動）

