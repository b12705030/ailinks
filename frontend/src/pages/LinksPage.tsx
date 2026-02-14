import { useState, useEffect } from 'react'
import { linksApi, Link } from '../api/client'
import { format } from 'date-fns'
import { zhTW } from 'date-fns/locale'
import './LinksPage.css'

const CATEGORIES = [
  '全部',
  '娛樂',
  '學習',
  '工作',
  '購物',
  '食譜',
  '健身',
  '旅遊',
  '靈感',
  '其他',
]

export default function LinksPage() {
  const [links, setLinks] = useState<Link[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('全部')
  const [searchQuery, setSearchQuery] = useState('')
  const [showReviewed, setShowReviewed] = useState<boolean | null>(null)

  useEffect(() => {
    loadLinks()
  }, [selectedCategory, showReviewed, searchQuery])

  const loadLinks = async () => {
    setLoading(true)
    try {
      const params: any = {
        limit: 100,
      }
      
      if (selectedCategory !== '全部') {
        params.category = selectedCategory
      }
      
      if (showReviewed !== null) {
        params.reviewed = showReviewed
      }
      
      if (searchQuery) {
        params.search = searchQuery
      }
      
      const data = await linksApi.getAll(params)
      setLinks(data)
    } catch (error) {
      console.error('Error loading links:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleToggleReviewed = async (link: Link) => {
    try {
      await linksApi.update(link.id, { reviewed: !link.reviewed })
      loadLinks()
    } catch (error) {
      console.error('Error updating link:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('確定要刪除這個連結嗎？')) return
    
    try {
      await linksApi.delete(id)
      loadLinks()
    } catch (error) {
      console.error('Error deleting link:', error)
    }
  }

  if (loading) {
    return <div className="loading">加載中...</div>
  }

  return (
    <div className="links-page">
      <div className="filters">
        <div className="filter-group">
          <label>分類：</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="filter-select"
          >
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat === '全部' ? '全部' : cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>状态：</label>
          <select
            value={showReviewed === null ? '全部' : showReviewed ? '已查看' : '未查看'}
            onChange={(e) => {
              const value = e.target.value
              setShowReviewed(value === '全部' ? null : value === '已查看')
            }}
            className="filter-select"
          >
            <option value="全部">全部</option>
            <option value="未查看">未查看</option>
            <option value="已查看">已查看</option>
          </select>
        </div>

        <div className="filter-group">
          <input
            type="text"
            placeholder="搜索链接..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      <div className="links-grid">
        {links.length === 0 ? (
          <div className="empty-state">
            <p>還沒有連結，快去添加一些吧！</p>
          </div>
        ) : (
          links.map((link) => (
            <LinkCard
              key={link.id}
              link={link}
              onToggleReviewed={() => handleToggleReviewed(link)}
              onDelete={() => handleDelete(link.id)}
            />
          ))
        )}
      </div>
    </div>
  )
}

function LinkCard({
  link,
  onToggleReviewed,
  onDelete,
}: {
  link: Link
  onToggleReviewed: () => void
  onDelete: () => void
}) {
  return (
    <div className={`link-card ${link.reviewed ? 'reviewed' : ''}`}>
      {link.image_url && (
        <div className="link-image">
          <img src={link.image_url} alt={link.title || ''} />
        </div>
      )}
      
      <div className="link-content">
        <div className="link-header">
          <h3>
            <a
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => onToggleReviewed()}
            >
              {link.title || link.domain}
            </a>
          </h3>
          {link.ai_category && (
            <span className="category-badge">{link.ai_category}</span>
          )}
        </div>

        {link.summary && (
          <p className="link-summary">{link.summary}</p>
        )}

        {link.description && !link.summary && (
          <p className="link-description">{link.description}</p>
        )}

        <div className="link-meta">
          <span className="domain">{link.domain}</span>
          {link.source_app && (
            <span className="source">{link.source_app}</span>
          )}
          <span className="date">
            {format(new Date(link.created_at), 'yyyy/MM/dd', { locale: zhTW })}
          </span>
        </div>

        {link.ai_tags.length > 0 && (
          <div className="link-tags">
            {link.ai_tags.map((tag, idx) => (
              <span key={idx} className="tag">{tag}</span>
            ))}
          </div>
        )}

        <div className="link-actions">
          <button
            onClick={onToggleReviewed}
            className={`btn ${link.reviewed ? 'btn-reviewed' : 'btn-unreviewed'}`}
          >
            {link.reviewed ? '✓ 已查看' : '未查看'}
          </button>
          <button onClick={onDelete} className="btn btn-delete">
            刪除
          </button>
        </div>
      </div>
    </div>
  )
}

