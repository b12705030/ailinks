# 🔧 修復 Android App 錯誤 - 完整步驟

## 📋 步驟 1：重新編譯 App

### 在 Android Studio 中：

1. **清理項目**
   - 點擊菜單：`Build` → `Clean Project`
   - 等待完成

2. **重新構建**
   - 點擊菜單：`Build` → `Rebuild Project`
   - 等待編譯完成

3. **同步項目**
   - 如果看到 "Sync Now" 提示，點擊它
   - 或者：`File` → `Sync Project with Gradle Files`

---

## 📱 步驟 2：安裝到手機

### 方法 A：通過 USB 連接

1. **連接手機到電腦**
   - 使用 USB 線連接
   - 在手機上允許 USB 調試

2. **運行 App**
   - 點擊 Android Studio 頂部的綠色 ▶️ 按鈕
   - 或者：`Run` → `Run 'app'`
   - 選擇你的手機設備

### 方法 B：直接安裝 APK

1. **生成 APK**
   - `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
   - 等待構建完成

2. **找到 APK 文件**
   - 路徑：`app/build/outputs/apk/debug/app-debug.apk`

3. **傳輸到手機並安裝**
   - 通過 USB、藍牙或雲盤傳輸
   - 在手機上打開文件並安裝

---

## 🔍 步驟 3：查看錯誤日誌

### 方法 1：Android Studio Logcat（最簡單）

1. **打開 Logcat**
   - 在 Android Studio 底部找到 "Logcat" 標籤
   - 如果沒有，點擊 `View` → `Tool Windows` → `Logcat`

2. **連接手機**
   - 確保手機已連接並運行 App

3. **過濾日誌**
   - 在搜索框輸入：`MainActivity` 或 `ShareActivity`
   - 或者選擇級別：`Error` 或 `Warning`

4. **查看錯誤**
   - 紅色文字 = 錯誤
   - 黃色文字 = 警告
   - 點擊錯誤行可以看到完整堆棧跟踪

### 方法 2：使用 ADB 命令

1. **打開終端/命令提示符**

2. **運行命令**：
   ```bash
   # 查看所有錯誤
   adb logcat *:E
   
   # 查看 MainActivity 和 ShareActivity 的日誌
   adb logcat MainActivity:D ShareActivity:D *:S
   
   # 清除舊日誌並查看新日誌
   adb logcat -c && adb logcat MainActivity:D ShareActivity:D *:S
   ```

3. **複製錯誤訊息**
   - 在終端中選中錯誤文字
   - 複製並發給我

---

## 🐛 步驟 4：常見錯誤修復

### 錯誤 1：Network Security Config

**如果看到這個錯誤**：
```
java.net.UnknownServiceException: CLEARTEXT communication not permitted
```

**修復方法**：

1. **創建網絡安全配置文件**
   - 在 `app/src/main/res/` 創建 `xml` 文件夾（如果不存在）
   - 在 `xml` 文件夾中創建 `network_security_config.xml`

2. **添加內容**：
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

3. **更新 AndroidManifest.xml**
   - 在 `<application>` 標籤中添加：
   ```xml
   android:networkSecurityConfig="@xml/network_security_config"
   ```

### 錯誤 2：找不到類別

**如果看到這個錯誤**：
```
java.lang.ClassNotFoundException
```

**修復方法**：
1. `Build` → `Clean Project`
2. `Build` → `Rebuild Project`
3. 重啟 Android Studio

### 錯誤 3：權限問題

**如果看到這個錯誤**：
```
java.lang.SecurityException: Permission denied
```

**修復方法**：
- 確認 `AndroidManifest.xml` 中有：
  ```xml
  <uses-permission android:name="android.permission.INTERNET" />
  ```

---

## 📸 步驟 5：截圖錯誤（可選）

如果方便，可以：
1. 截圖手機上的錯誤訊息
2. 截圖 Logcat 中的錯誤日誌
3. 發給我，我可以更快幫你解決

---

## ✅ 檢查清單

在告訴我錯誤之前，請確認：

- [ ] 已重新編譯 App
- [ ] 已安裝到手機
- [ ] 已查看 Logcat 日誌
- [ ] 已複製錯誤訊息
- [ ] 已確認 AndroidManifest.xml 有 INTERNET 權限

---

## 🆘 如果還是無法解決

請提供以下信息：

1. **完整的錯誤日誌**（從 Logcat 複製，包括堆棧跟踪）
2. **錯誤發生的時間**：
   - [ ] 打開 App 時
   - [ ] 分享連結時
   - [ ] 手動添加連結時
   - [ ] 刷新列表時
3. **Android 版本**：設置 → 關於手機
4. **手機型號**

這樣我可以更準確地幫你解決問題！

