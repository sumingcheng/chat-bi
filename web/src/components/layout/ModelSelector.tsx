import { useEffect, useMemo, useState } from 'react'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { HiCpuChip } from 'react-icons/hi2'
import { llmApi, type LLMProvider, type LLMSelection } from '../../http/llm'

export function ModelSelector() {
  const { t } = useTranslation()
  const [providers, setProviders] = useState<LLMProvider[]>([])
  const [models, setModels] = useState<string[]>([])
  const [selection, setSelection] = useState<LLMSelection | null>(null)
  const [loading, setLoading] = useState(false)

  const configuredProviders = useMemo(
    () => providers.filter(provider => provider.configured),
    [providers]
  )

  useEffect(() => {
    void loadProviders()
  }, [])

  useEffect(() => {
    if (selection?.provider) {
      void loadModels(selection.provider)
    }
  }, [selection?.provider])

  const loadProviders = async () => {
    try {
      const response = await llmApi.providers()
      setProviders(response.providers)
      setSelection(response.selection)
    } catch {
      toast.error(t('llm.loadProvidersFailed'))
    }
  }

  const loadModels = async (provider: string) => {
    setLoading(true)
    try {
      const response = await llmApi.models(provider)
      setModels(response.models)
    } catch {
      setModels([])
      toast.error(t('llm.loadModelsFailed'))
    } finally {
      setLoading(false)
    }
  }

  const handleProviderChange = async (provider: string) => {
    const nextProvider = providers.find(item => item.provider === provider)
    const nextModel = nextProvider?.default_model ?? ''
    await updateSelection({ provider, model: nextModel })
  }

  const handleModelChange = async (model: string) => {
    if (!selection) {
      return
    }

    await updateSelection({ provider: selection.provider, model })
  }

  const updateSelection = async (nextSelection: LLMSelection) => {
    if (!nextSelection.provider || !nextSelection.model) {
      return
    }

    setLoading(true)
    try {
      const updated = await llmApi.updateSelection(nextSelection)
      setSelection(updated)
      toast.success(t('llm.selectionUpdated'))
    } catch {
      toast.error(t('llm.selectionUpdateFailed'))
    } finally {
      setLoading(false)
    }
  }

  if (!selection) {
    return null
  }

  return (
    <div className="hidden md:flex items-center gap-1.5 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 px-2 py-1">
      <HiCpuChip className="h-3.5 w-3.5 text-indigo-500" />
      <select
        value={selection.provider}
        onChange={event => void handleProviderChange(event.target.value)}
        disabled={loading}
        className="max-w-24 bg-transparent text-[10px] font-medium text-zinc-600 dark:text-zinc-300 outline-none disabled:opacity-50"
        aria-label={t('llm.provider')}
      >
        {configuredProviders.map(provider => (
          <option key={provider.provider} value={provider.provider}>
            {provider.name}
          </option>
        ))}
      </select>
      <div className="h-3 w-px bg-zinc-200 dark:bg-zinc-700" />
      <select
        value={selection.model}
        onChange={event => void handleModelChange(event.target.value)}
        disabled={loading || models.length === 0}
        className="max-w-40 bg-transparent text-[10px] font-medium text-zinc-600 dark:text-zinc-300 outline-none disabled:opacity-50"
        aria-label={t('llm.model')}
      >
        {models.includes(selection.model) ? null : (
          <option value={selection.model}>{selection.model}</option>
        )}
        {models.map(model => (
          <option key={model} value={model}>
            {model}
          </option>
        ))}
      </select>
    </div>
  )
}
