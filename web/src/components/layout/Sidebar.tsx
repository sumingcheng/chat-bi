import { HiPlus, HiTrash, HiChatBubbleLeftRight, HiChevronLeft } from 'react-icons/hi2'
import { useTranslation } from 'react-i18next'
import { cn, formatDate } from '../../lib/utils'
import { useChatStore } from '../../store/chat'

interface SidebarProps {
  collapsed: boolean
  onToggle: () => void
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const { t, i18n } = useTranslation()
  const { conversations, activeConversationId, createConversation, switchConversation, deleteConversation } = useChatStore()

  return (
    <aside
      className={cn(
        'flex flex-col h-full bg-zinc-50/80 dark:bg-zinc-900/80 border-r border-zinc-200/80 dark:border-zinc-800/80 transition-[width,opacity] duration-300 ease-out',
        collapsed ? 'w-0 overflow-hidden opacity-0' : 'w-64 opacity-100'
      )}
    >
      {/* Logo + 收起 */}
      <div className="flex items-center justify-between h-12 px-4 border-b border-zinc-200/80 dark:border-zinc-800/80">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-indigo-600 flex items-center justify-center">
            <span className="text-[10px] font-bold text-white">BI</span>
          </div>
          <span className="text-sm font-semibold text-zinc-800 dark:text-zinc-200 tracking-tight">Chat-BI</span>
        </div>
        <button onClick={onToggle} className="p-1.5 rounded-lg hover:bg-zinc-200/80 dark:hover:bg-zinc-800 text-zinc-400 transition-colors duration-200 ease-out">
          <HiChevronLeft className="h-4 w-4" />
        </button>
      </div>

      {/* 新建按钮 */}
      <div className="p-3">
        <button
          onClick={() => createConversation()}
          className="flex items-center justify-center w-full gap-2 px-3 py-2.5 text-sm font-medium rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm shadow-indigo-600/15 hover:shadow-md hover:shadow-indigo-600/10 transition-[background-color,box-shadow] duration-200 ease-out"
        >
          <HiPlus className="h-4 w-4" />
          {t('chat.newConversation')}
        </button>
      </div>

      {/* 会话列表 */}
      <div className="flex-1 overflow-y-auto px-3 pb-3 space-y-0.5">
        {conversations.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-zinc-400">
            <HiChatBubbleLeftRight className="h-8 w-8 mb-2 opacity-30" />
            <p className="text-xs">{t('chat.emptyConversation')}</p>
          </div>
        )}
        {conversations.map(conv => {
          const isActive = conv.id === activeConversationId
          const msgCount = conv.messages.length
          const displayTitle = msgCount === 0 ? t('chat.newConversation') : conv.title
          return (
            <div
              key={conv.id}
              onClick={() => switchConversation(conv.id)}
              className={cn(
                'group relative flex items-start gap-2.5 px-3 py-2.5 rounded-lg cursor-pointer transition-[background-color,box-shadow,color] duration-200 ease-out',
                isActive
                  ? 'bg-white dark:bg-zinc-800 shadow-sm ring-1 ring-zinc-200/80 dark:ring-zinc-700/80'
                  : 'hover:bg-white/60 dark:hover:bg-zinc-800/50'
              )}
            >
              <HiChatBubbleLeftRight className={cn(
                'h-4 w-4 shrink-0 mt-0.5',
                isActive ? 'text-indigo-500' : 'text-zinc-400'
              )} />
              <div className="flex-1 min-w-0">
                <p className={cn(
                  'text-sm truncate',
                  isActive ? 'font-medium text-zinc-800 dark:text-zinc-100' : 'text-zinc-600 dark:text-zinc-400'
                )}>{displayTitle}</p>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-[10px] text-zinc-400">{formatDate(conv.createdAt, i18n.resolvedLanguage)}</span>
                  {msgCount > 0 && (
                    <span className="text-[10px] text-zinc-400">{t('chat.conversationCount', { count: msgCount })}</span>
                  )}
                </div>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); deleteConversation(conv.id) }}
                className="absolute right-2 top-2 flex items-center justify-center w-6 h-6 rounded-md bg-zinc-100 dark:bg-zinc-700 hover:bg-red-50 dark:hover:bg-red-900/30 text-zinc-400 hover:text-red-500 opacity-0 translate-y-0.5 pointer-events-none group-hover:opacity-100 group-hover:translate-y-0 group-hover:pointer-events-auto transition-[opacity,transform,background-color,color] duration-200 ease-out"
              >
                <HiTrash className="h-3 w-3" />
              </button>
            </div>
          )
        })}
      </div>

      {/* 底部信息 */}
      <div className="px-4 py-3 border-t border-zinc-200/80 dark:border-zinc-800/80">
        <p className="text-[10px] text-zinc-400 text-center">{t('chat.assistantTagline')}</p>
      </div>
    </aside>
  )
}
