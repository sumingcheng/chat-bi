import request from './index'

// 请求类型定义
export interface ChatRequest {
  question: string
  session_id?: string
}

// 响应类型定义
export interface ChatResponse {
  query_id: string
  answer: string
  chart_data: {
    type: 'bar' | 'line' | 'pie' | 'table'
    data: Record<string, any>[]
    config: Record<string, any>
  }
  sql: string
  record_count: number
}

// Chat-BI 智能对话接口
export const chatQuery = (params: ChatRequest): Promise<ChatResponse> => {
  return request.post('/chat', params)
}

// 导出常用的API函数
export const queryAPI = {
  chat: chatQuery,
}
