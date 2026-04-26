import type { EChartsOption } from 'echarts'
import { formatNumber, normalizeLocale } from './utils'

interface ChartConfig {
  xField?: string
  yField?: string
  colorField?: string
  angleField?: string
  [key: string]: unknown
}

export function generateChartOption(
  type: string,
  data: Record<string, unknown>[],
  config: ChartConfig,
  locale?: string
): EChartsOption {
  if (!data.length) {
    return {}
  }

  const resolvedLocale = normalizeLocale(locale)
  const resolvedConfig = resolveChartConfig(type, data, config)
  const xValues = data.map(item => item[resolvedConfig.xField ?? ''] ?? Object.values(item)[0])
  const yValues = data.map(item => item[resolvedConfig.yField ?? ''] ?? Object.values(item)[1])

  switch (type) {
    case 'bar':
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          valueFormatter: (value) => typeof value === 'number' ? formatNumber(value, resolvedLocale) : String(value ?? ''),
        },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: xValues as string[], axisLabel: { rotate: data.length > 8 ? 30 : 0 } },
        yAxis: { type: 'value', axisLabel: { formatter: (value: number) => formatNumber(value, resolvedLocale) } },
        series: [{
          name: resolvedConfig.yField ?? '',
          type: 'bar',
          data: yValues as number[],
          itemStyle: { borderRadius: [4, 4, 0, 0], color: '#6366f1' },
          barMaxWidth: 40,
        }],
      }

    case 'line':
      return {
        tooltip: {
          trigger: 'axis',
          valueFormatter: (value) => typeof value === 'number' ? formatNumber(value, resolvedLocale) : String(value ?? ''),
        },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: xValues as string[] },
        yAxis: { type: 'value', axisLabel: { formatter: (value: number) => formatNumber(value, resolvedLocale) } },
        series: [{
          name: resolvedConfig.yField ?? '',
          type: 'line',
          data: yValues as number[],
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: { width: 2, color: '#6366f1' },
          itemStyle: { color: '#6366f1' },
          areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(99,102,241,0.15)' }, { offset: 1, color: 'rgba(99,102,241,0)' }] } },
        }],
      }

    case 'pie':
      return {
        tooltip: {
          trigger: 'item',
          formatter: (params: any) => {
            const value = typeof params.value === 'number' ? params.value : Number(params.value ?? 0)
            const percent = typeof params.percent === 'number' ? params.percent : 0
            return `${params.name}: ${formatNumber(value, resolvedLocale)} (${percent}%)`
          },
        },
        legend: { type: 'scroll', orient: 'horizontal', bottom: 0 },
        series: [{
          name: '',
          type: 'pie',
          radius: ['40%', '65%'],
          data: data.map(item => ({
            name: String(item[resolvedConfig.colorField ?? ''] ?? Object.values(item)[0]),
            value: Number(item[resolvedConfig.angleField ?? ''] ?? Object.values(item)[1]) || 0,
          })),
          emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.2)' } },
          label: { show: true, formatter: '{b}\n{d}%' },
        }],
      }

    default:
      return {}
  }
}

function resolveChartConfig(
  type: string,
  data: Record<string, unknown>[],
  config: ChartConfig
): ChartConfig {
  const columns = Object.keys(data[0] ?? {})
  const numericColumns = columns.filter(column => isNumericColumn(data, column))
  const dimensionColumns = columns.filter(column => !numericColumns.includes(column))

  if (type === 'pie') {
    return {
      ...config,
      colorField: pickValidColumn(config.colorField, dimensionColumns, dimensionColumns[0]),
      angleField: pickValidColumn(config.angleField, numericColumns, pickNumericColumn(numericColumns)),
    }
  }

  return {
    ...config,
    xField: pickValidColumn(config.xField, dimensionColumns, pickDimensionColumn(dimensionColumns)),
    yField: pickValidColumn(config.yField, numericColumns, pickNumericColumn(numericColumns)),
  }
}

function isNumericColumn(data: Record<string, unknown>[], column: string): boolean {
  const values = data.map(item => item[column]).filter(value => value !== null && value !== undefined)
  return values.length > 0 && values.every(value => typeof value === 'number')
}

function pickValidColumn(column: string | undefined, validColumns: string[], fallback: string | undefined): string {
  if (column && validColumns.includes(column)) {
    return column
  }

  return fallback ?? ''
}

function pickNumericColumn(columns: string[]): string {
  return pickColumnByKeywords(columns, ['percentage', 'percent', 'ratio', 'rate', 'share', 'amount', 'sales', 'total', 'count', 'qty', 'quantity'])
}

function pickDimensionColumn(columns: string[]): string {
  return pickColumnByKeywords(columns, ['name', 'category', 'type', 'status', 'date', 'time', 'month', 'day'])
}

function pickColumnByKeywords(columns: string[], keywords: string[]): string {
  for (const keyword of keywords) {
    const matchedColumn = columns.find(column => column.toLowerCase().includes(keyword))
    if (matchedColumn) {
      return matchedColumn
    }
  }

  return columns[0] ?? ''
}
