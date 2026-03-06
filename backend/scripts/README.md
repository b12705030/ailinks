# 批量更新脚本

## update_short_names.py

批量更新所有链接的 `short_name`，使用新的逻辑（包含 AI 总结）重新生成。

### 使用方法

1. **激活虚拟环境**（重要！）
   ```bash
   cd backend
   
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows CMD
   venv\Scripts\activate.bat
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **确保环境变量已配置**
   - 确保 `.env` 文件在 `backend` 目录下
   - 包含必要的配置（Supabase、OpenAI API Key）

3. **运行脚本**
   ```bash
   python scripts/update_short_names.py
   ```

   或者使用 Python 模块方式：
   ```bash
   python -m scripts.update_short_names
   ```

### 注意事项

⚠️ **重要提示**：
- 这会重新生成**所有**链接的 `short_name`
- 会调用 OpenAI API，可能需要一些时间（取决于链接数量）
- 会消耗 OpenAI API 额度
- 建议在非高峰期运行

### 脚本功能

- 获取所有链接（最多 10000 个）
- 对每个链接重新生成 `short_name`（使用新的逻辑，包含 AI 总结）
- 更新数据库中的 `short_name` 字段
- 显示进度和结果统计

### 输出示例

```
==================================================
批量更新所有链接的 short_name
==================================================

开始获取所有链接...
找到 50 个链接

[1/50] 处理链接: Python 程式設計教學
  生成 short_name: Python教學
  ✓ 更新成功

[2/50] 处理链接: Nuphy Halo75 機械鍵盤開箱
  生成 short_name: Nuphy鍵盤
  ✓ 更新成功

...

==================================================
更新完成！
总计: 50 个链接
成功: 50 个
失败: 0 个
==================================================
```

