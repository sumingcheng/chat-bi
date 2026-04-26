import { useState } from 'react'
import { HiClipboard, HiCheck } from 'react-icons/hi2'
import { useTranslation } from 'react-i18next'

interface SqlBlockProps {
  sql: string
}

export function SqlBlock({ sql }: SqlBlockProps) {
  const { t } = useTranslation()
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(sql)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="relative group">
      <pre className="p-4 text-[12px] font-mono leading-relaxed text-emerald-300 bg-zinc-900 dark:bg-zinc-950 overflow-x-auto whitespace-pre-wrap selection:bg-indigo-500/30">
        <code>{sql}</code>
      </pre>
      <button
        onClick={handleCopy}
        className="absolute top-2.5 right-2.5 flex items-center gap-1 px-2 py-1 rounded-md text-[10px] font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-400 hover:text-zinc-200 opacity-0 translate-y-0.5 group-hover:opacity-100 group-hover:translate-y-0 transition-[opacity,transform,background-color,color] duration-200 ease-out"
      >
        {copied ? (
          <>
            <HiCheck className="h-3 w-3 text-green-400" />
            <span className="text-green-400">{t('common.copied')}</span>
          </>
        ) : (
          <>
            <HiClipboard className="h-3 w-3" />
            <span>{t('common.copy')}</span>
          </>
        )}
      </button>
    </div>
  )
}
