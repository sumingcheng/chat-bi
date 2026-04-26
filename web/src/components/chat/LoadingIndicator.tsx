import { HiSparkles } from 'react-icons/hi2'
import { useTranslation } from 'react-i18next'

export function LoadingIndicator() {
  const { t } = useTranslation()

  return (
    <div className="flex gap-3 py-5">
      <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 ring-1 ring-indigo-200/80 dark:ring-indigo-800/80 shrink-0">
        <HiSparkles className="h-4 w-4 text-indigo-500 dark:text-indigo-400" />
      </div>
      <div className="pt-2">
        <div className="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/80 dark:border-zinc-800/80">
          <div className="flex gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-[pulse_1.6s_ease-in-out_infinite]" />
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-[pulse_1.6s_ease-in-out_0.2s_infinite]" />
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-[pulse_1.6s_ease-in-out_0.4s_infinite]" />
          </div>
          <span className="text-xs text-zinc-400">{t('chat.loading')}</span>
        </div>
      </div>
    </div>
  )
}
