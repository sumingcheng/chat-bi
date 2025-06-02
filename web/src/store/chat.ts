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
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void
  setLoading: (loading: boolean) => void
  clearMessages: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  loading: false,

  addMessage: (message) => set((state) => ({
    messages: [...state.messages, {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date(),
    }]
  })),

  setLoading: (loading) => set({ loading }),

  clearMessages: () => set({ messages: [] }),
})) 