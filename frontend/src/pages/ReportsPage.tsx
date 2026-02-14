import { useState, useEffect } from 'react'
import { reportsApi, WeeklyReport } from '../api/client'
import { format } from 'date-fns'
import { zhTW } from 'date-fns/locale'
import './ReportsPage.css'

export default function ReportsPage() {
  const [report, setReport] = useState<WeeklyReport | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadReport()
  }, [])

  const loadReport = async () => {
    setLoading(true)
    try {
      const data = await reportsApi.getWeekly()
      setReport(data)
    } catch (error) {
      console.error('Error loading report:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">加載中...</div>
  }

  if (!report) {
    return <div className="empty-state">暫無數據</div>
  }

  return (
    <div className="reports-page">
      <div className="report-header">
        <h2>📊 本週連結收集報告</h2>
        <p className="report-date">
          {format(new Date(report.week_start), 'yyyy年MM月dd日', { locale: zhTW })} 起
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{report.total_links}</div>
          <div className="stat-label">總連結數</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{report.unique_domains}</div>
          <div className="stat-label">不同域名</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{report.unique_sources}</div>
          <div className="stat-label">不同來源</div>
        </div>
      </div>

      <div className="report-section">
        <h3>🏷️ 分類分布</h3>
        <div className="category-list">
          {Object.entries(report.category_distribution).map(([category, count]) => (
            <div key={category} className="category-item">
              <span className="category-name">{category}</span>
              <div className="category-bar">
                <div
                  className="category-fill"
                  style={{
                    width: `${(count / report.total_links) * 100}%`,
                  }}
                />
              </div>
              <span className="category-count">{count}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="report-section">
        <h3>🤖 AI 分析</h3>
        <div className="ai-analysis">
          {report.ai_analysis}
        </div>
      </div>

      {report.top_links.length > 0 && (
        <div className="report-section">
          <h3>⭐ 推薦回看的連結</h3>
          <div className="top-links">
            {report.top_links.map((link, idx) => (
              <div key={link.id} className="top-link-item">
                <div className="top-link-rank">{idx + 1}</div>
                <div className="top-link-content">
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="top-link-title"
                  >
                    {link.title || link.domain}
                  </a>
                  {link.summary && (
                    <p className="top-link-summary">{link.summary}</p>
                  )}
                  <div className="top-link-meta">
                    <span>{link.domain}</span>
                    {link.ai_category && (
                      <span className="category-badge">{link.ai_category}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

