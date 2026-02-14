import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://192.168.1.105:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Link {
  id: string
  url: string
  title: string | null
  description: string | null
  summary: string | null
  image_url: string | null
  domain: string
  source_app: string | null
  content_type: string | null
  ai_category: string | null
  ai_tags: string[]
  importance_score: number
  reviewed: boolean
  created_at: string
  updated_at: string
}

export interface LinkCreate {
  url: string
  source_app?: string
  title?: string
  description?: string
}

export interface WeeklyReport {
  week_start: string
  total_links: number
  unique_domains: number
  unique_sources: number
  category_distribution: Record<string, number>
  top_links: Link[]
  ai_analysis: string
}

export const linksApi = {
  create: async (data: LinkCreate): Promise<Link> => {
    const response = await apiClient.post<Link>('/api/links', data)
    return response.data
  },
  
  getAll: async (params?: {
    limit?: number
    offset?: number
    category?: string
    reviewed?: boolean
    search?: string
  }): Promise<Link[]> => {
    const response = await apiClient.get<Link[]>('/api/links', { params })
    return response.data
  },
  
  getById: async (id: string): Promise<Link> => {
    const response = await apiClient.get<Link>(`/api/links/${id}`)
    return response.data
  },
  
  update: async (id: string, data: Partial<Link>): Promise<Link> => {
    const response = await apiClient.patch<Link>(`/api/links/${id}`, data)
    return response.data
  },
  
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/links/${id}`)
  },
}

export const reportsApi = {
  getWeekly: async (weekStart?: string): Promise<WeeklyReport> => {
    const response = await apiClient.get<WeeklyReport>('/api/reports/weekly', {
      params: weekStart ? { week_start: weekStart } : undefined,
    })
    return response.data
  },
}

