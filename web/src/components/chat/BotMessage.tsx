import { useState } from 'react'
import { HiSparkles, HiChevronDown, HiChevronRight, HiCodeBracket, HiTableCells } from 'react-icons/hi2'
import { useTranslation } from 'react-i18next'
import type { ChatResponse } from '../../http/query'
import { SqlBlock } from './SqlBlock'
import { ChartBlock } from './ChartBlock'
import { DataTable } from './DataTable'

interface BotMessageProps {
  content: string
  data?: ChatResponse
}

export function BotMessage({ content, data }: BotMessageProps) {
  const { t } = useTranslation()
  const [sqlExpanded, setSqlExpanded] = useState(false)
  const [tableExpanded, setTableExpanded] = useState(false)

  const hasChart = data && data.chart_data.data.length > 0 && data.chart_data.type !== 'table'
  const hasData = data && data.chart_data.data.length > 0

  return (
    <div className="flex gap-3 py-5">
      <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 ring-1 ring-indigo-200/80 dark:ring-indigo-800/80 shrink-0">
        <HiSparkles className="h-4 w-4 text-indigo-500 dark:text-indigo-400" />
      </div>
      <div className="flex-1 min-w-0 pt-1 space-y-3">
        <p className="text-[13px] text-zinc-700 dark:text-zinc-300 whitespace-pre-wrap break-words leading-relaxed">{content}</p>

        {data && (
          <div className="space-y-2.5">
            {hasChart && (
              <ChartBlock
                type={data.chart_data.type}
                data={data.chart_data.data}
                config={data.chart_data.config}
              />
            )}

            {data.sql && (
              <Collapsible
                icon={<HiCodeBracket className="h-3.5 w-3.5" />}
                label={t('chat.sqlQuery')}
                badge={t('common.sql')}
                expanded={sqlExpanded}
                onToggle={() => setSqlExpanded(v => !v)}
              >
                <SqlBlock sql={data.sql} />
              </Collapsible>
            )}

            {hasData && (
              <Collapsible
                icon={<HiTableCells className="h-3.5 w-3.5" />}
                label={t('chat.dataPreview')}
                badge={t('common.rows', { count: data.record_count })}
                expanded={tableExpanded}
                onToggle={() => setTableExpanded(v => !v)}
              >
                <DataTable data={data.chart_data.data} />
              </Collapsible>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function Collapsible({ icon, label, badge, expanded, onToggle, children }: {
  icon: React.ReactNode
  label: string
  badge?: string
  expanded: boolean
  onToggle: () => void
  children: React.ReactNode
}) {
  return (
    <div className="rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 overflow-hidden bg-white dark:bg-zinc-900/50">
      <button
        onClick={onToggle}
        className="flex items-center gap-2 w-full px-3.5 py-2.5 text-xs font-medium text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors duration-200 ease-out"
      >
        <span className="text-zinc-400">{icon}</span>
        {expanded ? <HiChevronDown className="h-3 w-3" /> : <HiChevronRight className="h-3 w-3" />}
        <span>{label}</span>
        {badge && (
          <span className="ml-auto px-1.5 py-0.5 text-[10px] font-medium rounded-md bg-zinc-100 dark:bg-zinc-800 text-zinc-400">{badge}</span>
        )}
      </button>
      <div
        className={`grid overflow-hidden transition-[grid-template-rows,opacity,border-color] duration-250 ease-out ${
          expanded
            ? 'grid-rows-[1fr] opacity-100 border-t border-zinc-200/80 dark:border-zinc-800/80'
            : 'grid-rows-[0fr] opacity-70 border-t border-transparent'
        }`}
      >
        <div className="min-h-0">
          {children}
        </div>
      </div>
    </div>
  )
}
