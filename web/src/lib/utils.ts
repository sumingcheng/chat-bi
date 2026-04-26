import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function normalizeLocale(locale?: string) {
  if (!locale) {
    return 'en'
  }

  return locale.startsWith('zh') ? 'zh-CN' : 'en'
}

export function formatDate(date: Date | string, locale?: string) {
  return new Intl.DateTimeFormat(normalizeLocale(locale), {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

export function formatNumber(value: number, locale?: string) {
  return new Intl.NumberFormat(normalizeLocale(locale)).format(value)
}