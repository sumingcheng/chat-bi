import { HiChartBar, HiCube, HiUsers, HiShoppingCart, HiArrowTrendingUp, HiTableCells } from 'react-icons/hi2'
import { useTranslation } from 'react-i18next'

interface WelcomeScreenProps {
  onExampleClick: (question: string) => void
}

const examples = [
  { icon: HiArrowTrendingUp, key: 'salesTrend', color: 'text-blue-500 bg-blue-50 dark:bg-blue-900/20' },
  { icon: HiCube, key: 'productRanking', color: 'text-violet-500 bg-violet-50 dark:bg-violet-900/20' },
  { icon: HiUsers, key: 'customerAnalysis', color: 'text-amber-500 bg-amber-50 dark:bg-amber-900/20' },
  { icon: HiChartBar, key: 'categoryComparison', color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-900/20' },
  { icon: HiShoppingCart, key: 'orderStatus', color: 'text-rose-500 bg-rose-50 dark:bg-rose-900/20' },
  { icon: HiTableCells, key: 'inventoryAlert', color: 'text-cyan-500 bg-cyan-50 dark:bg-cyan-900/20' },
]

export function WelcomeScreen({ onExampleClick }: WelcomeScreenProps) {
  const { t } = useTranslation()

  return (
    <div className="flex flex-col items-center justify-center h-full px-4">
      <div className="max-w-xl w-full">
        {/* 品牌区域 */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-indigo-600 shadow-lg shadow-indigo-600/20 mb-5">
            <span className="text-lg font-bold text-white tracking-tight">BI</span>
          </div>
          <h2 className="text-2xl font-bold text-zinc-800 dark:text-zinc-100 mb-2 tracking-tight">{t('welcome.title')}</h2>
          <p className="text-sm text-zinc-500 leading-relaxed">
            {t('welcome.description')}
          </p>
        </div>

        {/* 示例卡片 */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {examples.map((ex, i) => (
            <button
              key={i}
              onClick={() => onExampleClick(t(`welcome.examples.${ex.key}.question`))}
              className="group flex flex-col items-start gap-2.5 p-4 rounded-xl border border-zinc-200/80 dark:border-zinc-800/80 bg-white dark:bg-zinc-900 text-left hover:border-zinc-300 dark:hover:border-zinc-700 hover:shadow-sm hover:shadow-zinc-200/40 dark:hover:shadow-zinc-900/30 transition-[border-color,box-shadow,background-color] duration-200 ease-out"
            >
              <div className={`flex items-center justify-center w-8 h-8 rounded-lg ${ex.color}`}>
                <ex.icon className="h-4 w-4" />
              </div>
              <div>
                <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors duration-200 ease-out">{t(`welcome.examples.${ex.key}.title`)}</span>
                <p className="text-[11px] text-zinc-400 leading-relaxed mt-0.5 line-clamp-2">{t(`welcome.examples.${ex.key}.question`)}</p>
              </div>
            </button>
          ))}
        </div>

        {/* 底部提示 */}
        <p className="text-center text-[11px] text-zinc-400 mt-8">
          {t('welcome.footer')}
        </p>
      </div>
    </div>
  )
}
