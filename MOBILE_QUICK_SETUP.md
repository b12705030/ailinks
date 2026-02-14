# 📱 手機快速訪問指南（3 步搞定）

## ✅ 已完成的配置

我已經修改了後端配置，允許手機訪問。現在只需要：

## 🚀 3 步完成

### 步驟 1：獲取你的 IP 地址

在 PowerShell 運行：
```powershell
ipconfig | findstr "IPv4"
```

你會看到類似：
```
IPv4 地址 . . . . . . . . . . . . : 192.168.1.100
```

記下這個 IP 地址（例如：`192.168.1.100`）

### 步驟 2：修改前端 API 地址

編輯 `frontend/src/api/client.ts`，將第 3 行改為：

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://[你的IP]:8000'
```

例如，如果你的 IP 是 `192.168.1.100`：
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://192.168.1.100:8000'
```

### 步驟 3：重啟服務

1. **重啟後端**（確保顯示 `Uvicorn running on http://0.0.0.0:8000`）
2. **重啟前端**（會顯示 Network 地址）

### 步驟 4：在手機訪問

確保手機和電腦連接到**同一個 Wi-Fi**，然後在手機瀏覽器輸入：

```
http://[你的IP]:3000
```

例如：`http://192.168.1.100:3000`

---

## 🎯 更簡單的方式（使用環境變量）

不想改代碼？可以創建 `frontend/.env.local`：

```env
VITE_API_URL=http://192.168.1.100:8000
```

（替換為你的實際 IP）

然後重啟前端即可！

---

## 🔍 如何確認 IP 是否正確？

在手機瀏覽器訪問：
```
http://[你的IP]:8000/docs
```

如果能看到 API 文檔頁面，說明 IP 正確！

---

## ❓ 常見問題

### Q: 手機無法訪問？
- ✅ 確認手機和電腦在同一 Wi-Fi
- ✅ 確認防火牆允許端口 3000 和 8000
- ✅ 嘗試關閉 VPN

### Q: 想在外網訪問？
需要部署到雲端（Railway/Vercel），參考 `MOBILE_SETUP.md` 的「方式二」

---

## 🎉 完成！

現在你可以在手機上使用 Link Collector 了！

更詳細的說明請查看 `MOBILE_SETUP.md`

