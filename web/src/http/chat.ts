// 重新导出query.ts中的API，为了保持向后兼容
export { chatQuery as query, type ChatRequest, type ChatResponse } from './query'

// 导出聊天API对象
export const chatApi = {
  query: async (params: import('./query').ChatRequest): Promise<import('./query').ChatResponse> => {
    const { chatQuery } = await import('./query')
    return chatQuery(params)
  }
} 