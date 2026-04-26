import { Toaster } from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { AppLayout } from './components/layout/AppLayout'
import { MessageList } from './components/chat/MessageList'
import { WelcomeScreen } from './components/chat/WelcomeScreen'
import { ChatInput } from './components/ChatInput'
import { useChatStore } from './store/chat'
import { chatApi } from './http/chat'

export default function App() {
  const { t } = useTranslation()
  const {
    activeConversation,
    activeConversationId,
    isLoading,
    createConversation,
    addMessage,
    setLoading,
  } = useChatStore()

  const conv = activeConversation()
  const hasMessages = conv && conv.messages.length > 0

  const handleSend = async (content: string) => {
    if (!activeConversationId) {
      createConversation()
    }

    setLoading(true)
    addMessage({ type: 'user', content, timestamp: new Date() })

    try {
      const response = await chatApi.query({ question: content })
      addMessage({ type: 'bot', content: response.answer, timestamp: new Date(), data: response })
    } catch {
      addMessage({ type: 'bot', content: t('chat.errorMessage'), timestamp: new Date() })
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppLayout>
      <div className="flex flex-col h-full">
        <div className="flex-1 overflow-hidden">
          {hasMessages
            ? <MessageList />
            : <WelcomeScreen onExampleClick={handleSend} />
          }
        </div>
        <ChatInput onSubmit={handleSend} disabled={isLoading} />
      </div>
      <Toaster position="top-right" toastOptions={{ duration: 3000 }} />
    </AppLayout>
  )
}
