const zhCN = {
  common: {
    language: '语言',
    english: '英文',
    chinese: '中文',
    light: '浅色',
    dark: '深色',
    switchTheme: '切换主题',
    online: '在线',
    copy: '复制',
    copied: '已复制',
    sql: 'SQL',
    rows: '{{count}} 条',
    items: '{{count}} 项数据',
    clear: '清空',
  },
  chat: {
    newConversation: '新对话',
    emptyConversation: '暂无对话记录',
    conversationCount: '{{count}} 条',
    clearConversationConfirm: '确定清空当前对话？',
    assistantTagline: 'AI 驱动的数据分析助手',
    inputPlaceholder: '描述你的数据查询需求...',
    inputHint: 'Enter 发送 · Shift+Enter 换行',
    loading: '正在查询数据并生成分析...',
    errorMessage: '抱歉，处理请求时发生错误，请稍后重试。',
    dataPreview: '数据预览',
    sqlQuery: 'SQL 查询',
  },
  welcome: {
    title: '有什么可以帮您？',
    description: '输入自然语言问题，自动查询数据库并生成可视化图表',
    footer: '支持柱状图 / 折线图 / 饼图 / 表格等多种可视化方式',
    examples: {
      salesTrend: {
        title: '销售趋势',
        question: '显示最近30天每天的销售额变化趋势',
      },
      productRanking: {
        title: '产品排行',
        question: '销量最高的前10款产品及其总销量',
      },
      customerAnalysis: {
        title: '客户分析',
        question: '每个客户的总购买金额和订单数量统计',
      },
      categoryComparison: {
        title: '类别对比',
        question: '各个产品类别的销售额占比分析',
      },
      orderStatus: {
        title: '订单状态',
        question: '不同订单状态的数量分布情况',
      },
      inventoryAlert: {
        title: '库存预警',
        question: '库存数量少于10的产品清单',
      },
    },
  },
  chart: {
    defaultTitle: '图表',
    bar: '柱状图',
    line: '折线图',
    pie: '饼图',
  },
  llm: {
    provider: '渠道',
    model: '模型',
    loadProvidersFailed: '加载 LLM 渠道失败',
    loadModelsFailed: '加载模型列表失败',
    selectionUpdated: '模型已切换',
    selectionUpdateFailed: '模型切换失败',
  },
} as const

export default zhCN
