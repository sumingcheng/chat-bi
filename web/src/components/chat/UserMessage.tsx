import { HiUser } from 'react-icons/hi2'

interface UserMessageProps {
  content: string
}

export function UserMessage({ content }: UserMessageProps) {
  return (
    <div className="flex gap-3 py-5">
      <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-zinc-100 dark:bg-zinc-800 ring-1 ring-zinc-200/80 dark:ring-zinc-700/80 shrink-0">
        <HiUser className="h-4 w-4 text-zinc-500 dark:text-zinc-400" />
      </div>
      <div className="flex-1 min-w-0 pt-1">
        <p className="text-[13px] font-medium text-zinc-800 dark:text-zinc-200 whitespace-pre-wrap break-words leading-relaxed">{content}</p>
      </div>
    </div>
  )
}
