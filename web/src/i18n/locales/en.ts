const en = {
  common: {
    language: 'Language',
    english: 'English',
    chinese: 'Chinese',
    light: 'Light',
    dark: 'Dark',
    switchTheme: 'Switch theme',
    online: 'Online',
    copy: 'Copy',
    copied: 'Copied',
    sql: 'SQL',
    rows: '{{count}} rows',
    items: '{{count}} items',
    clear: 'Clear',
  },
  chat: {
    newConversation: 'New chat',
    emptyConversation: 'No conversations yet',
    conversationCount: '{{count}} msgs',
    clearConversationConfirm: 'Clear the current conversation?',
    assistantTagline: 'AI-powered analytics assistant',
    inputPlaceholder: 'Describe the data question you want to explore...',
    inputHint: 'Enter to send · Shift+Enter for a new line',
    loading: 'Querying data and building the analysis...',
    errorMessage: 'Sorry, something went wrong. Please try again later.',
    dataPreview: 'Data preview',
    sqlQuery: 'SQL query',
  },
  welcome: {
    title: 'What would you like to analyze?',
    description: 'Ask in natural language and get database answers with charts.',
    footer: 'Supports bar, line, pie, table, and other visualization types',
    examples: {
      salesTrend: {
        title: 'Sales trend',
        question: 'Show the daily sales trend for the last 30 days',
      },
      productRanking: {
        title: 'Product ranking',
        question: 'List the top 10 products by total sales volume',
      },
      customerAnalysis: {
        title: 'Customer analysis',
        question: 'Summarize total purchase amount and order count for each customer',
      },
      categoryComparison: {
        title: 'Category comparison',
        question: 'Analyze the sales share of each product category',
      },
      orderStatus: {
        title: 'Order status',
        question: 'Show the distribution of order counts by status',
      },
      inventoryAlert: {
        title: 'Inventory alert',
        question: 'List products with inventory below 10',
      },
    },
  },
  chart: {
    defaultTitle: 'Chart',
    bar: 'Bar chart',
    line: 'Line chart',
    pie: 'Pie chart',
  },
  llm: {
    provider: 'Provider',
    model: 'Model',
    loadProvidersFailed: 'Failed to load LLM providers',
    loadModelsFailed: 'Failed to load model list',
    selectionUpdated: 'Model updated',
    selectionUpdateFailed: 'Failed to update model',
  },
} as const

export default en
