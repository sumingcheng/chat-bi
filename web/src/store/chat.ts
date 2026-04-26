import { create } from 'zustand'
import type { ChatResponse } from '../http/query'
import i18n from '../i18n'

export interface ChatMessage {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
  data?: ChatResponse
}

export interface Conversation {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: Date
}

interface ChatState {
  conversations: Conversation[]
  activeConversationId: string | null
  isLoading: boolean

  activeConversation: () => Conversation | undefined
  createConversation: () => string
  switchConversation: (id: string) => void
  deleteConversation: (id: string) => void
  addMessage: (message: Omit<ChatMessage, 'id'>) => void
  setLoading: (loading: boolean) => void
  clearCurrentMessages: () => void
}

const STORAGE_KEY = 'chat-bi-conversations'
const DEFAULT_CONVERSATION_TITLES = new Set(['New chat', '新对话'])

function getDefaultConversationTitle(): string {
  return i18n.t('chat.newConversation')
}

function isDefaultConversationTitle(title: string): boolean {
  return DEFAULT_CONVERSATION_TITLES.has(title)
}

function loadFromStorage(): { conversations: Conversation[]; activeId: string | null } {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return { conversations: [], activeId: null }
    }
    const parsed = JSON.parse(raw)
    const conversations = (parsed.conversations ?? []).map((c: Conversation) => ({
      ...c,
      createdAt: new Date(c.createdAt),
      messages: c.messages.map((m: ChatMessage) => ({ ...m, timestamp: new Date(m.timestamp) })),
    }))
    return { conversations, activeId: parsed.activeId ?? null }
  } catch {
    return { conversations: [], activeId: null }
  }
}

function saveToStorage(conversations: Conversation[], activeId: string | null) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ conversations, activeId }))
  } catch {
    // localStorage 满了就忽略
  }
}

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8)
}

const initial = loadFromStorage()

export const useChatStore = create<ChatState>((set, get) => ({
  conversations: initial.conversations,
  activeConversationId: initial.activeId,
  isLoading: false,

  activeConversation: () => {
    const { conversations, activeConversationId } = get()
    return conversations.find(c => c.id === activeConversationId)
  },

  createConversation: () => {
    const id = generateId()
    const conv: Conversation = {
      id,
      title: getDefaultConversationTitle(),
      messages: [],
      createdAt: new Date(),
    }
    set(state => {
      const conversations = [conv, ...state.conversations]
      saveToStorage(conversations, id)
      return { conversations, activeConversationId: id }
    })
    return id
  },

  switchConversation: (id) => {
    set(state => {
      saveToStorage(state.conversations, id)
      return { activeConversationId: id }
    })
  },

  deleteConversation: (id) => {
    set(state => {
      const conversations = state.conversations.filter(c => c.id !== id)
      const activeId = state.activeConversationId === id
        ? (conversations[0]?.id ?? null)
        : state.activeConversationId
      saveToStorage(conversations, activeId)
      return { conversations, activeConversationId: activeId }
    })
  },

  addMessage: (message) => {
    set(state => {
      let { activeConversationId } = state
      let conversations = [...state.conversations]

      // 没有活跃会话则自动创建
      if (!activeConversationId) {
        const id = generateId()
        conversations = [{ id, title: getDefaultConversationTitle(), messages: [], createdAt: new Date() }, ...conversations]
        activeConversationId = id
      }

      conversations = conversations.map(c => {
        if (c.id !== activeConversationId) {
          return c
        }
        const newMsg: ChatMessage = { ...message, id: generateId() }
        const messages = [...c.messages, newMsg]
        // 用第一条用户消息作为标题
        const title = isDefaultConversationTitle(c.title) && message.type === 'user'
          ? message.content.slice(0, 24)
          : c.title
        return { ...c, messages, title }
      })

      saveToStorage(conversations, activeConversationId)
      return { conversations, activeConversationId }
    })
  },

  setLoading: (isLoading) => set({ isLoading }),

  clearCurrentMessages: () => {
    set(state => {
      const conversations = state.conversations.map(c =>
        c.id === state.activeConversationId ? { ...c, messages: [], title: getDefaultConversationTitle() } : c
      )
      saveToStorage(conversations, state.activeConversationId)
      return { conversations }
    })
  },
}))
