"""
批量更新所有链接的 short_name
使用新的逻辑（包含 AI 总结）重新生成 short_name
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# 设置工作目录为 backend 目录
os.chdir(backend_dir)

from app.services.database import DatabaseService
from app.services.ai_classifier import AIClassifier


async def update_all_short_names():
    """更新所有链接的 short_name"""
    db = DatabaseService()
    classifier = AIClassifier()
    
    print("开始获取所有链接...")
    # 获取所有链接
    all_links = await db.get_links(limit=10000, offset=0)
    total = len(all_links)
    print(f"找到 {total} 个链接")
    
    if total == 0:
        print("没有链接需要更新")
        return
    
    updated_count = 0
    failed_count = 0
    
    for i, link in enumerate(all_links, 1):
        try:
            link_id = link.get('id')
            url = link.get('url', '')
            title = link.get('title')
            description = link.get('description')
            summary = link.get('summary', '')  # AI 总结
            domain = link.get('domain', '')
            ai_category = link.get('ai_category', '')
            ai_tags = link.get('ai_tags', [])
            
            if not isinstance(ai_tags, list):
                ai_tags = []
            
            print(f"\n[{i}/{total}] 处理链接: {title or url[:50]}")
            
            # 重新生成 short_name（使用新的逻辑，包含 summary）
            short_name = await classifier._generate_short_name(
                url=url,
                title=title,
                description=description,
                summary=summary,  # 使用 AI 总结
                domain=domain,
                category=ai_category,
                tags=ai_tags
            )
            
            print(f"  生成 short_name: {short_name}")
            
            # 更新数据库
            await db.update_link(str(link_id), {'short_name': short_name})
            updated_count += 1
            
            print(f"  ✓ 更新成功")
            
            # 避免 API 调用过快，稍微延迟
            await asyncio.sleep(0.5)
            
        except Exception as e:
            failed_count += 1
            print(f"  ✗ 更新失败: {str(e)}")
            continue
    
    print(f"\n{'='*50}")
    print(f"更新完成！")
    print(f"总计: {total} 个链接")
    print(f"成功: {updated_count} 个")
    print(f"失败: {failed_count} 个")
    print(f"{'='*50}")


if __name__ == "__main__":
    print("="*50)
    print("批量更新所有链接的 short_name")
    print("="*50)
    print("\n注意：")
    print("1. 这会重新生成所有链接的 short_name")
    print("2. 会调用 OpenAI API，可能需要一些时间")
    print("3. 会消耗 OpenAI API 额度")
    print("\n开始执行...\n")
    
    asyncio.run(update_all_short_names())

