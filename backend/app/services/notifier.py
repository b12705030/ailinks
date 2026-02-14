from app.config import settings
from typing import Dict, Optional
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Notifier:
    """通知服务（Telegram / Email）"""
    
    async def send_weekly_report(self, stats: Dict, ai_analysis: str):
        """發送週報"""
        # 生成報告內容
        report_content = self._format_weekly_report(stats, ai_analysis)
        
        # 發送到 Telegram
        if settings.telegram_bot_token and settings.telegram_chat_id:
            await self._send_telegram(report_content)
        
        # 發送 Email
        if settings.smtp_host:
            await self._send_email("📊 本週連結收集報告", report_content)
    
    def _format_weekly_report(self, stats: Dict, ai_analysis: str) -> str:
        """格式化週報內容"""
        content = f"""
📊 本週連結收集報告

📈 統計
• 總連結數: {stats.get('total_links', 0)}
• 不同域名: {stats.get('unique_domains', 0)}
• 不同來源: {stats.get('unique_sources', 0)}

🏷️ 分類分布
"""
        for category, count in stats.get('category_distribution', {}).items():
            content += f"• {category}: {count}\n"
        
        content += f"\n🔗 來源分布\n"
        for source, count in stats.get('source_distribution', {}).items():
            content += f"• {source}: {count}\n"
        
        content += f"\n🤖 AI 分析\n{ai_analysis}\n"
        
        if stats.get('top_links'):
            content += "\n⭐ 推薦回看的連結\n"
            for i, link in enumerate(stats['top_links'][:5], 1):
                title = link.get('title', '無標題')
                url = link.get('url', '')
                content += f"{i}. {title}\n   {url}\n"
        
        return content
    
    async def _send_telegram(self, message: str):
        """發送 Telegram 消息"""
        try:
            url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
            async with httpx.AsyncClient() as client:
                await client.post(
                    url,
                    json={
                        "chat_id": settings.telegram_chat_id,
                        "text": message,
                        "parse_mode": "Markdown"
                    }
                )
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
    
    async def _send_email(self, subject: str, content: str):
        """發送 Email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.email_from
            msg['To'] = settings.email_from  # 發送給自己
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")

