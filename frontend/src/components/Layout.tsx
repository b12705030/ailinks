import { Link, useLocation } from 'react-router-dom'
import { Home, Plus, BarChart3 } from 'lucide-react'
import './Layout.css'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  
  return (
    <div className="layout">
      <header className="header">
        <h1>🔗 Link Collector</h1>
        <p className="subtitle">AI 智能連結收集系統</p>
      </header>
      
      <nav className="nav">
        <Link 
          to="/" 
          className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}
        >
          <Home size={20} />
          <span>連結列表</span>
        </Link>
        <Link 
          to="/add" 
          className={`nav-item ${location.pathname === '/add' ? 'active' : ''}`}
        >
          <Plus size={20} />
          <span>添加連結</span>
        </Link>
        <Link 
          to="/reports" 
          className={`nav-item ${location.pathname === '/reports' ? 'active' : ''}`}
        >
          <BarChart3 size={20} />
          <span>週報</span>
        </Link>
      </nav>
      
      <main className="main">
        {children}
      </main>
    </div>
  )
}

