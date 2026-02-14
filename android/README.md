# Android Share Target 配置

這個目錄包含 Android Share Target 的配置說明，讓你可以從任何應用直接分享連結到 Link Collector。

## 方式 1：使用 Android App（推薦）

如果你要開發一個 Android App，可以在 `AndroidManifest.xml` 中添加：

```xml
<activity
    android:name=".ShareActivity"
    android:label="保存到 Link Collector"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
</activity>
```

然後在 `ShareActivity` 中：

```kotlin
class ShareActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT)
        val sharedTitle = intent.getStringExtra(Intent.EXTRA_SUBJECT)
        
        if (sharedText != null) {
            // 提取 URL
            val url = extractUrl(sharedText)
            
            // 調用 API
            saveLink(url, getSourceApp(intent))
        }
        
        finish()
    }
    
    private fun getSourceApp(intent: Intent): String {
        val packageName = intent.`package` ?: return "unknown"
        return when {
            packageName.contains("instagram") -> "instagram"
            packageName.contains("facebook") -> "facebook"
            packageName.contains("messenger") -> "messenger"
            packageName.contains("threads") -> "threads"
            else -> "unknown"
        }
    }
}
```

## 方式 2：使用 Shortcuts（更簡單）

如果你不想開發完整 App，可以使用 Android Shortcuts：

1. 安裝 [Shortcuts](https://play.google.com/store/apps/details?id=com.rhmsoft.shortcuts)
2. 創建一個新的 Shortcut
3. 設置 Intent Action 為 `android.intent.action.SEND`
4. 設置 Intent Data 為 `text/plain`
5. 在 Shortcut 中調用你的 API

## 方式 3：使用 Tasker（自動化）

如果你有 Tasker，可以創建一個 Profile：

1. Event → Intent Received
2. Action: `android.intent.action.SEND`
3. MIME Type: `text/plain`
4. Task: HTTP Request 到你的 API

## API 調用示例

```bash
curl -X POST http://your-api-url/api/links \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "source_app": "instagram"
  }'
```

## 測試

你可以使用以下命令測試 Share Target：

```bash
adb shell am start -a android.intent.action.SEND \
  -t text/plain \
  --es android.intent.extra.TEXT "https://example.com/test"
```
