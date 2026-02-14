import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { linksApi } from '../api/client'
import './AddLinkPage.css'

export default function AddLinkPage() {
  const [url, setUrl] = useState('')
  const [sourceApp, setSourceApp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!url.trim()) {
      setError('請輸入連結')
      return
    }

    setLoading(true)
    setError('')

    try {
      await linksApi.create({
        url: url.trim(),
        source_app: sourceApp || undefined,
      })
      
      setUrl('')
      setSourceApp('')
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || '添加連結失敗')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="add-link-page">
      <div className="add-link-card">
        <h2>添加新連結</h2>
        <p className="subtitle">貼上連結，AI 會自動分類和整理</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="url">連結 URL *</label>
            <input
              id="url"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/article"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="source">來源（可選）</label>
            <select
              id="source"
              value={sourceApp}
              onChange={(e) => setSourceApp(e.target.value)}
              disabled={loading}
            >
              <option value="">手動添加</option>
              <option value="messenger">Messenger</option>
              <option value="instagram">Instagram</option>
              <option value="facebook">Facebook</option>
              <option value="threads">Threads</option>
              <option value="twitter">Twitter</option>
            </select>
          </div>

          {error && <div className="error">{error}</div>}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? '處理中...' : '添加連結'}
          </button>
        </form>
      </div>
    </div>
  )
}

