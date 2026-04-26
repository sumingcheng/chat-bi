import { useState, useRef, useEffect, type KeyboardEvent } from 'react'
import { HiPaperAirplane } from 'react-icons/hi2'
import { useTranslation } from 'react-i18next'
import { cn } from '../lib/utils'

interface ChatInputProps {
  onSubmit: (message: string) => void
  disabled?: boolean
}

export function ChatInput({ onSubmit, disabled = false }: ChatInputProps) {
  const { t } = useTranslation()
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`
    }
  }, [input])

  const handleSubmit = () => {
    if (input.trim() && !disabled) {
      onSubmit(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="bg-white dark:bg-zinc-950 shrink-0">
      <div className="max-w-3xl mx-auto px-4 pb-4 pt-2">
        <div className="relative flex items-end rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 shadow-sm focus-within:border-indigo-300 dark:focus-within:border-indigo-700 focus-within:shadow-md focus-within:shadow-indigo-500/5 transition-[border-color,box-shadow,background-color] duration-200 ease-out">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={t('chat.inputPlaceholder')}
            disabled={disabled}
            rows={1}
            className="flex-1 min-h-[44px] max-h-[160px] px-4 py-3 text-[13px] bg-transparent border-none outline-none resize-none text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400"
          />
          <button
            onClick={handleSubmit}
            disabled={!input.trim() || disabled}
            className={cn(
              'p-2.5 m-1.5 rounded-xl transition-[background-color,box-shadow,color,opacity] duration-200 ease-out',
              input.trim() && !disabled
                ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm shadow-indigo-600/15 hover:shadow-md hover:shadow-indigo-600/10'
                : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400 cursor-not-allowed'
            )}
          >
            <HiPaperAirplane className="h-4 w-4" />
          </button>
        </div>
        <p className="text-center text-[10px] text-zinc-400 mt-2">{t('chat.inputHint')}</p>
      </div>
    </div>
  )
}
