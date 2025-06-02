import { create } from 'zustand'
import type { ChatResponse } from '../http/query'

export interface ChatMessage {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
  data?: ChatResponse // bot消息包含查询结果
}

interface ChatState {
  messages: ChatMessage[]
  loading: boolean
  isLoading: boolean // 为了兼容新的组件
  addMessage: (message: Omit<ChatMessage, 'id'>) => void
  setLoading: (loading: boolean) => void
  clearMessages: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  loading: false,
  isLoading: false,

  addMessage: (message) => set((state) => ({
    messages: [...state.messages, {
      ...message,
      id: Date.now().toString(),
    }]
  })),

  setLoading: (loading) => set({ loading, isLoading: loading }),

  clearMessages: () => set({ messages: [] }),
})) 