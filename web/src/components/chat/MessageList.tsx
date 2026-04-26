import { useEffect, useRef } from 'react'
import { useChatStore } from '../../store/chat'
import { UserMessage } from './UserMessage'
import { BotMessage } from './BotMessage'
import { LoadingIndicator } from './LoadingIndicator'

export function MessageList() {
  const bottomRef = useRef<HTMLDivElement>(null)
  const { activeConversation, isLoading } = useChatStore()
  const conv = activeConversation()
  const messages = conv?.messages ?? []

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages.length, isLoading])

  return (
    <div className="h-full overflow-y-auto scroll-smooth">
      <div className="max-w-3xl mx-auto px-4 py-4 divide-y divide-zinc-100 dark:divide-zinc-800/50">
        {messages.map(msg =>
          msg.type === 'user'
            ? <UserMessage key={msg.id} content={msg.content} />
            : <BotMessage key={msg.id} content={msg.content} data={msg.data} />
        )}
        {isLoading && <LoadingIndicator />}
        <div ref={bottomRef} className="h-2 border-none" />
      </div>
    </div>
  )
}
