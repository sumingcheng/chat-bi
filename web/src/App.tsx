import { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import { Button } from './components/ui/Button'
import { Input } from './components/ui/Input'
import { useChatStore } from './store/chat'
import { queryAPI } from './http/query'
import { IoSend } from 'react-icons/io5'
import { AiOutlineLoading3Quarters } from 'react-icons/ai'
import { HiOutlineChartBar } from 'react-icons/hi2'
import { formatDate } from './lib/utils'

function App() {
  const [input, setInput] = useState('')
  const { messages, loading, addMessage, setLoading } = useChatStore()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const question = input.trim()
    setInput('')

    // 添加用户消息
    addMessage({
      type: 'user',
      content: question,
    })

    setLoading(true)

    try {
      // 调用API
      const result = await queryAPI.chat({ question })
      
      // 添加Bot响应
      addMessage({
        type: 'bot',
        content: result.answer,
        data: result,
      })
    } catch (error) {
      // 错误已经在axios拦截器中处理了
      addMessage({
        type: 'bot',
        content: '抱歉，查询时出现了错误，请稍后重试。',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Toaster position="top-center" />
      
      {/* 头部 */}
      <header className="border-b bg-card/50 backdrop-blur">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <HiOutlineChartBar className="h-8 w-8 text-primary" />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Chat-BI
            </h1>
            <span className="text-sm text-muted-foreground ml-2">智能商业分析对话系统</span>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6 max-w-4xl">
        {/* 聊天区域 */}
        <div className="flex flex-col h-[calc(100vh-200px)]">
          {/* 消息列表 */}
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-4">
            {messages.length === 0 ? (
              <div className="text-center text-muted-foreground py-12">
                <HiOutlineChartBar className="h-16 w-16 mx-auto mb-4 opacity-50" />
                <p className="text-lg mb-2">欢迎使用 Chat-BI</p>
                <p className="text-sm">请输入您的问题，我会帮您分析数据并生成可视化图表</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.type === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    <div className="text-sm">{message.content}</div>
                    {message.data && (
                      <div className="mt-3 p-3 bg-card rounded border text-xs text-muted-foreground">
                        <div className="flex justify-between items-center mb-2">
                          <span>查询结果</span>
                          <span>{message.data.record_count} 条记录</span>
                        </div>
                        <div className="font-mono text-xs bg-muted p-2 rounded mb-2">
                          {message.data.sql}
                        </div>
                        <div className="text-xs">
                          图表类型: {message.data.chart_data.type}
                        </div>
                      </div>
                    )}
                    <div className="text-xs opacity-70 mt-2">
                      {formatDate(message.timestamp)}
                    </div>
                  </div>
                </div>
              ))
            )}
            
            {loading && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-lg p-4 flex items-center gap-2">
                  <AiOutlineLoading3Quarters className="h-4 w-4 animate-spin" />
                  <span className="text-sm">正在分析数据...</span>
                </div>
              </div>
            )}
          </div>

          {/* 输入框 */}
          <div className="border-t pt-4">
            <form onSubmit={handleSubmit} className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="请输入您的问题，例如：最近一个月的销售额是多少？"
                className="flex-1"
                disabled={loading}
              />
              <Button type="submit" disabled={loading || !input.trim()}>
                {loading ? (
                  <AiOutlineLoading3Quarters className="h-4 w-4 animate-spin" />
                ) : (
                  <IoSend className="h-4 w-4" />
                )}
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
