import { useTranslation } from 'react-i18next'
import { formatNumber } from '../../lib/utils'

interface DataTableProps {
  data: Record<string, unknown>[]
}

export function DataTable({ data }: DataTableProps) {
  const { i18n } = useTranslation()

  if (!data.length) {
    return null
  }

  const columns = Object.keys(data[0])

  return (
    <div className="max-h-80 overflow-auto">
      <table className="w-full text-xs">
        <thead className="sticky top-0 bg-zinc-50 dark:bg-zinc-900 z-10">
          <tr>
            <th className="text-left px-3.5 py-2.5 font-medium text-zinc-400 border-b border-zinc-200/80 dark:border-zinc-800/80 w-10 text-center">#</th>
            {columns.map(col => (
              <th key={col} className="text-left px-3.5 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 border-b border-zinc-200/80 dark:border-zinc-800/80 whitespace-nowrap">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800/50">
          {data.map((row, i) => (
            <tr key={i} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors duration-150 ease-out">
              <td className="px-3.5 py-2 text-zinc-300 dark:text-zinc-600 text-center tabular-nums">{i + 1}</td>
              {columns.map(col => {
                const val = row[col]
                const isNumber = typeof val === 'number'
                return (
                  <td key={col} className={`px-3.5 py-2 whitespace-nowrap ${isNumber ? 'text-indigo-600 dark:text-indigo-400 tabular-nums font-medium' : 'text-zinc-700 dark:text-zinc-300'}`}>
                    {isNumber ? formatNumber(val, i18n.resolvedLanguage) : String(val ?? '')}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
