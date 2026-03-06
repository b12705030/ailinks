# 🔍 檢查 AI 分類和標題提取

## 問題描述

連結可以成功新增，但是：
- ❌ 沒有經過 AI 分類
- ❌ 沒有顯示標題

## 可能的原因

### 1. Railway 後端沒有配置 OpenAI API Key

**檢查方法**：

1. **登入 Railway**
2. **選擇你的項目**
3. **點擊 "Variables" 標籤**
4. **檢查是否有以下環境變量**：
   - `OPENAI_API_KEY` - 必須設置
   - `OPENAI_MODEL` - 可選（默認：gpt-4o-mini）

**如果沒有設置**：
1. 在 Railway Variables 中添加：
   ```
   OPENAI_API_KEY=sk-你的API密鑰
   OPENAI_MODEL=gpt-4o-mini
   ```
2. **重新部署**（Railway 會自動重新部署）

### 2. AI 處理失敗但連結仍被保存

**檢查方法**：

1. **查看 Railway 日誌**：
   - 在 Railway 項目中點擊 "Deployments"
   - 選擇最新的部署
   - 查看 "Logs"
   - 搜索錯誤訊息

2. **常見錯誤**：
   - `OpenAI API key not found` - API key 未設置
   - `Rate limit exceeded` - API 調用次數超限
   - `Invalid API key` - API key 無效

### 3. 數據庫中的數據不完整

**檢查方法**：

1. **在 Supabase 中查看數據**：
   - 登入 Supabase
   - 選擇你的項目
   - 打開 "Table Editor"
   - 查看 `links` 表
   - 檢查以下欄位：
     - `title` - 應該有值
     - `ai_category` - 應該有值（如：娛樂、學習等）
     - `ai_tags` - 應該是數組
     - `summary` - 應該有值

2. **如果欄位為空或 null**：
   - 說明 AI 處理失敗
   - 需要檢查 Railway 日誌

## 解決步驟

### 步驟 1：檢查 Railway 環境變量

1. 登入 Railway
2. 選擇項目
3. 點擊 "Variables"
4. 確認 `OPENAI_API_KEY` 已設置

### 步驟 2：測試 API

在瀏覽器中打開：
```
https://ailinks-production.up.railway.app/docs
```

1. **測試創建連結**：
   - 點擊 `POST /api/links`
   - 點擊 "Try it out"
   - 輸入測試 URL：
     ```json
     {
       "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
       "source_app": "test"
     }
     ```
   - 點擊 "Execute"
   - 查看響應：
     - 應該包含 `title`
     - 應該包含 `ai_category`
     - 應該包含 `ai_tags`
     - 應該包含 `summary`

2. **如果響應中沒有這些欄位**：
   - 查看 Railway 日誌
   - 檢查是否有錯誤訊息

### 步驟 3：檢查 Railway 日誌

1. 在 Railway 項目中
2. 點擊 "Deployments"
3. 選擇最新的部署
4. 查看 "Logs"
5. 搜索：
   - `Error`
   - `OpenAI`
   - `AI classification`

### 步驟 4：重新測試

1. **從 Android App 分享一個連結**
2. **等待幾秒**（AI 處理需要時間）
3. **刷新列表**
4. **檢查是否顯示標題和分類**

## 如果還是沒有標題和分類

### 臨時解決方案：手動觸發 AI 處理

可以創建一個 API 端點來重新處理現有的連結：

```python
@router.post("/{link_id}/reclassify")
async def reclassify_link(link_id: str):
    """重新對連結進行 AI 分類"""
    # 獲取連結
    link = await db.get_link_by_id(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # 重新提取元數據
    metadata = await metadata_extractor.extract(link['url'])
    
    # 重新 AI 分類
    ai_result = await ai_classifier.classify(
        url=link['url'],
        title=metadata.get('title'),
        description=metadata.get('description'),
        domain=metadata.get('domain', '')
    )
    
    # 更新連結
    update_data = {
        'title': metadata.get('title'),
        'description': metadata.get('description'),
        'ai_category': ai_result.get('ai_category'),
        'ai_tags': ai_result.get('ai_tags', []),
        'summary': ai_result.get('summary')
    }
    
    result = await db.update_link(link_id, update_data)
    return LinkResponse(**result)
```

## 快速檢查清單

- [ ] Railway 環境變量中有 `OPENAI_API_KEY`
- [ ] OpenAI API Key 有效
- [ ] Railway 日誌中沒有錯誤
- [ ] Supabase 數據庫中的連結有 `title` 和 `ai_category`
- [ ] Android App 正確顯示數據

## 下一步

1. **檢查 Railway 環境變量**
2. **查看 Railway 日誌**
3. **測試 API 端點**
4. **告訴我結果**

這樣我可以更準確地幫你解決問題！

