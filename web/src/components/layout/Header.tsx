import { useState } from 'react'
import { HiBars3, HiTrash, HiSignal, HiSun, HiMoon } from 'react-icons/hi2'
import { useTranslation } from 'react-i18next'
import { useChatStore } from '../../store/chat'
import { getTheme, setTheme, type ThemeMode } from '../../lib/theme'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '../ui/Tooltip'
import { ModelSelector } from './ModelSelector'

interface HeaderProps {
  sidebarCollapsed: boolean
  onToggleSidebar: () => void
}

export function Header({ sidebarCollapsed, onToggleSidebar }: HeaderProps) {
  const { t, i18n } = useTranslation()
  const { activeConversation, clearCurrentMessages } = useChatStore()
  const [theme, setThemeState] = useState<ThemeMode>(() => getTheme())
  const conv = activeConversation()
  const hasMessages = conv && conv.messages.length > 0
  const currentLanguage = i18n.resolvedLanguage?.startsWith('zh') ? 'zh-CN' : 'en'
  const conversationTitle = conv?.messages.length ? conv.title : t('chat.newConversation')
  const nextTheme: ThemeMode = theme === 'dark' ? 'light' : 'dark'
  const themeToggleLabel = `${t('common.switchTheme')}: ${nextTheme === 'dark' ? t('common.dark') : t('common.light')}`

  const handleChangeLanguage = (language: 'en' | 'zh-CN') => {
    void i18n.changeLanguage(language)
  }

  const handleToggleTheme = () => {
    const nextTheme: ThemeMode = theme === 'dark' ? 'light' : 'dark'
    setTheme(nextTheme)
    setThemeState(nextTheme)
  }

  return (
    <header className="flex items-center justify-between h-12 px-4 border-b border-zinc-200/80 dark:border-zinc-800/80 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-sm shrink-0">
      <div className="flex items-center gap-3">
        {sidebarCollapsed && (
          <button onClick={onToggleSidebar} className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-500 transition-colors duration-200 ease-out">
            <HiBars3 className="h-5 w-5" />
          </button>
        )}
        {sidebarCollapsed && (
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 rounded bg-indigo-600 flex items-center justify-center">
              <span className="text-[8px] font-bold text-white">BI</span>
            </div>
            <span className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">Chat-BI</span>
          </div>
        )}
        {conv && (
          <div className="flex items-center gap-2">
            {!sidebarCollapsed && <div className="w-px h-4 bg-zinc-200 dark:bg-zinc-700" />}
            <span className="text-xs text-zinc-400 truncate max-w-[200px]">{conversationTitle}</span>
          </div>
        )}
      </div>

      <TooltipProvider delayDuration={120}>
        <div className="flex items-center gap-2">
          <ModelSelector />
          <Tooltip>
            <TooltipTrigger asChild>
              <button
                onClick={handleToggleTheme}
                className="flex items-center justify-center w-8 h-8 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 text-zinc-500 dark:text-zinc-300 hover:text-zinc-700 dark:hover:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-[background-color,color,border-color] duration-200 ease-out"
                aria-label={themeToggleLabel}
              >
                {theme === 'dark' ? <HiSun className="h-4 w-4" /> : <HiMoon className="h-4 w-4" />}
              </button>
            </TooltipTrigger>
            <TooltipContent>
              {themeToggleLabel}
            </TooltipContent>
          </Tooltip>
          <div className="flex items-center rounded-lg border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 p-0.5">
            <button
              onClick={() => handleChangeLanguage('en')}
              className={`px-2 py-1 text-[10px] font-medium rounded-md transition-[background-color,color,box-shadow] duration-200 ease-out ${
                currentLanguage === 'en'
                  ? 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300'
              }`}
              aria-label={t('common.english')}
            >
              EN
            </button>
            <button
              onClick={() => handleChangeLanguage('zh-CN')}
              className={`px-2 py-1 text-[10px] font-medium rounded-md transition-[background-color,color,box-shadow] duration-200 ease-out ${
                currentLanguage === 'zh-CN'
                  ? 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300'
              }`}
              aria-label={t('common.chinese')}
            >
              中文
            </button>
          </div>
          <div className="hidden sm:flex items-center gap-1.5 px-2 py-1 rounded-full bg-emerald-50 dark:bg-emerald-900/20">
            <HiSignal className="h-3 w-3 text-emerald-500" />
            <span className="text-[10px] font-medium text-emerald-600 dark:text-emerald-400">{t('common.online')}</span>
          </div>
          {hasMessages && (
            <button
              onClick={() => { if (window.confirm(t('chat.clearConversationConfirm'))) { clearCurrentMessages() } }}
              className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs rounded-lg text-zinc-500 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200 ease-out"
            >
              <HiTrash className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">{t('common.clear')}</span>
            </button>
          )}
        </div>
      </TooltipProvider>
    </header>
  )
}
