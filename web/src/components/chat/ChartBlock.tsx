import ReactECharts from 'echarts-for-react'
import { useTranslation } from 'react-i18next'
import { HiChartBarSquare } from 'react-icons/hi2'
import { generateChartOption } from '../../lib/chart'

interface ChartBlockProps {
  type: string
  data: Record<string, unknown>[]
  config: Record<string, unknown>
}

export function ChartBlock({ type, data, config }: ChartBlockProps) {
  const { t, i18n } = useTranslation()
  const option = generateChartOption(type, data, config as Parameters<typeof generateChartOption>[2], i18n.resolvedLanguage)
  const chartTypeLabel = t(`chart.${type}`, { defaultValue: t('chart.defaultTitle') })

  if (!Object.keys(option).length) {
    return null
  }

  return (
    <div className="rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 overflow-hidden bg-white dark:bg-zinc-900/50">
      <div className="flex items-center gap-2 px-3.5 py-2.5 border-b border-zinc-200/80 dark:border-zinc-800/80">
        <HiChartBarSquare className="h-4 w-4 text-indigo-500" />
        <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400">{chartTypeLabel}</span>
        <span className="text-[10px] text-zinc-400">{t('common.items', { count: data.length })}</span>
      </div>
      <div className="p-2">
        <ReactECharts option={option} style={{ height: 340 }} opts={{ renderer: 'svg' }} />
      </div>
    </div>
  )
}
