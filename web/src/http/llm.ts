import request from './index'

export interface LLMProvider {
  provider: string
  name: string
  configured: boolean
  base_url: string
  default_model: string
  active: boolean
}

export interface LLMSelection {
  provider: string
  model: string
}

export interface LLMProvidersResponse {
  providers: LLMProvider[]
  selection: LLMSelection
}

export interface LLMModelsResponse {
  provider: string
  models: string[]
}

export const llmApi = {
  providers: (): Promise<LLMProvidersResponse> => request.get('/llm/providers'),
  models: (provider: string): Promise<LLMModelsResponse> => request.get('/llm/models', { params: { provider } }),
  selection: (): Promise<LLMSelection> => request.get('/llm/selection'),
  updateSelection: (selection: LLMSelection): Promise<LLMSelection> => request.post('/llm/selection', selection),
}
