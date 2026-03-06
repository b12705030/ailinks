# 🐛 Android App 調試指南

## 📱 查看錯誤日誌

### 方法 1：使用 Android Studio Logcat

1. **連接手機到電腦**
2. **打開 Android Studio**
3. **打開 Logcat**（底部面板）
4. **過濾日誌**：
   - 在搜索框輸入：`MainActivity` 或 `ShareActivity`
   - 或者選擇 `Error` 級別查看錯誤

### 方法 2：使用 ADB 命令

```bash
# 查看所有日誌
adb logcat

# 只查看錯誤
adb logcat *:E

# 查看 MainActivity 和 ShareActivity 的日誌
adb logcat MainActivity:D ShareActivity:D *:S
```

### 方法 3：在手機上查看

1. **開發者選項** → **錯誤報告**
2. 或者使用 **Log Viewer** App

---

## 🔍 常見錯誤和解決方法

### 錯誤 1：Network Security Config

**錯誤訊息**：
```
java.net.UnknownServiceException: CLEARTEXT communication not permitted
```

**解決方法**：
在 `app/src/main/res/xml/` 創建 `network_security_config.xml`：

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>
```

然後在 `AndroidManifest.xml` 的 `<application>` 標籤中添加：
```xml
android:networkSecurityConfig="@xml/network_security_config"
```

---

### 錯誤 2：找不到類別

**錯誤訊息**：
```
java.lang.ClassNotFoundException
```

**解決方法**：
1. **Clean Project**：`Build` → `Clean Project`
2. **Rebuild Project**：`Build` → `Rebuild Project`
3. **Sync Project**：點擊 `Sync Now`

---

### 錯誤 3：權限問題

**錯誤訊息**：
```
java.lang.SecurityException: Permission denied
```

**解決方法**：
確認 `AndroidManifest.xml` 中有：
```xml
<uses-permission android:name="android.permission.INTERNET" />
```

---

### 錯誤 4：空指針異常

**錯誤訊息**：
```
java.lang.NullPointerException
```

**解決方法**：
查看 Logcat 中的完整堆棧跟踪，找到具體是哪一行代碼出錯。

---

## 🧪 測試步驟

### 1. 測試 MainActivity

1. 打開 App
2. 查看是否顯示連結列表
3. 點擊右上角刷新按鈕
4. 查看 Logcat 日誌

### 2. 測試 ShareActivity

1. 從其他 App（如瀏覽器）分享一個連結
2. 選擇 "保存到 Link Collector"
3. 查看 Toast 訊息
4. 查看 Logcat 日誌

### 3. 測試手動添加

1. 打開 App
2. 點擊右下角 + 按鈕
3. 輸入一個 URL
4. 點擊添加
5. 查看是否成功

---

## 📋 日誌標籤

- `MainActivity`：主界面相關日誌
- `ShareActivity`：分享功能相關日誌

---

## 💡 如果還是無法解決

請提供以下信息：

1. **完整的錯誤日誌**（從 Logcat 複製）
2. **錯誤發生的時間**（打開 App 時？分享時？）
3. **Android 版本**
4. **手機型號**

這樣我可以更準確地幫你解決問題！

