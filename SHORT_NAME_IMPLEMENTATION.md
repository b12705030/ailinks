# Short Name 功能實現指南

## 📋 概述

已實現後端 AI 自動生成 `short_name`（簡短易識別名稱）功能，用於在宇宙視圖的節點標籤上顯示。

## ✅ 已完成的修改

### 1. 數據庫遷移
- **文件**: `supabase/migrations/002_add_short_name.sql`
- **內容**: 添加 `short_name` 字段和索引

### 2. AI 分類器 (`backend/app/services/ai_classifier.py`)
- ✅ 添加 `_generate_short_name()` 方法：使用 LLM 生成簡短名稱（4-8個字）
- ✅ 添加 `_fallback_short_name()` 方法：後備方案（從標題/域名提取）
- ✅ 更新 `classify()` 方法：在分類時自動生成 `short_name`

### 3. 數據模型 (`backend/app/models/link.py`)
- ✅ 在 `LinkResponse` 中添加 `short_name: Optional[str] = None` 字段

### 4. API 端點 (`backend/app/api/links.py`)
- ✅ 在創建連結時保存 `short_name` 到數據庫

### 5. Chat API (`backend/app/api/chat.py`)
- ✅ 在返回連結時包含 `short_name` 字段

### 6. 前端 Android (`app/src/main/java/com/tca940120/ailinks/MainActivity.kt`)
- ✅ 在 `Link` 數據類中添加 `shortName: String?` 字段
- ✅ 在 JSON 解析時讀取 `short_name` 字段
- ✅ 在 `generateShortLabel()` 中優先使用 `shortName`

## 🚀 部署步驟

### 步驟 1: 執行數據庫遷移

在 Supabase Dashboard 中執行以下 SQL：

```sql
-- 添加 short_name 字段到 links 表
ALTER TABLE links ADD COLUMN IF NOT EXISTS short_name TEXT;

-- 添加索引以便搜索
CREATE INDEX IF NOT EXISTS idx_links_short_name ON links(short_name);
```

或者使用 Supabase CLI：

```bash
cd supabase/migrations
supabase db push
```

### 步驟 2: 部署後端代碼

將更新後的後端代碼部署到 Railway（或其他平台）：

```bash
cd backend
# 確保所有依賴已安裝
pip install -r requirements.txt

# 部署到 Railway（根據你的部署方式）
```

### 步驟 3: 測試

1. **添加新連結**：添加一個新連結，檢查是否自動生成 `short_name`
2. **查看 API 響應**：確認返回的 JSON 包含 `short_name` 字段
3. **檢查前端顯示**：在 Android 應用的宇宙視圖中，節點標籤應顯示 AI 生成的名稱

## 📝 功能說明

### AI 生成邏輯

1. **優先使用 Tags**：如果有 AI tags，優先組合前 1-2 個標籤
2. **LLM 生成**：調用 OpenAI API 生成簡短描述性名稱
3. **後備方案**：如果 LLM 失敗，從標題或域名提取

### 生成範例

- "YouTube 美食料理頻道" → "美食料理"
- "Python 程式設計教學" → "Python教學"
- "溫馨的愛情小說推薦" → "暖心小說"
- "健身運動教學網站" → "健身教學"

### 前端使用

前端會按以下優先級顯示標籤：

1. **shortName**（後端 AI 生成）← 最優先
2. AI tags 組合
3. 從 summary/description 提取關鍵詞
4. 從 title 提取關鍵詞
5. 清理後的域名

## 🔍 故障排除

### 問題：新連結沒有 `short_name`

**檢查**：
1. 確認數據庫遷移已執行
2. 檢查後端日誌，確認 AI 分類器是否正常運行
3. 確認 OpenAI API Key 是否正確配置

### 問題：前端顯示舊名稱

**解決**：
1. 清除應用緩存
2. 重新啟動應用
3. 確認 API 返回包含 `short_name` 字段

### 問題：現有連結沒有 `short_name`

**解決**：
可以創建一個腳本來為現有連結生成 `short_name`：

```python
# backend/scripts/generate_short_names.py
from app.services.database import DatabaseService
from app.services.ai_classifier import AIClassifier

async def generate_missing_short_names():
    db = DatabaseService()
    classifier = AIClassifier()
    
    # 獲取所有沒有 short_name 的連結
    links = await db.get_links(limit=1000)
    
    for link in links:
        if not link.get('short_name'):
            # 生成 short_name
            ai_result = await classifier.classify(
                url=link['url'],
                title=link.get('title'),
                description=link.get('description'),
                domain=link['domain']
            )
            
            # 更新數據庫
            await db.update_link(link['id'], {
                'short_name': ai_result.get('short_name')
            })
```

## 📊 API 響應範例

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "url": "https://example.com/article",
  "title": "Python 程式設計教學",
  "short_name": "Python教學",
  "ai_category": "學習",
  "ai_tags": ["Python", "程式設計", "教學"],
  ...
}
```

## 🎯 下一步

- [ ] 為現有連結批量生成 `short_name`
- [ ] 優化 AI 提示詞以提高名稱質量
- [ ] 添加名稱長度驗證
- [ ] 考慮緩存機制以減少 API 調用

