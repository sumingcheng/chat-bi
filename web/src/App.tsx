import { useEffect, useRef } from 'react';
import { Toaster } from 'react-hot-toast';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { Button } from './components/ui/Button';
import { useChatStore } from './store/chat';
import { chatApi } from './http/chat';
import { HiSparkles, HiTrash, HiChartBar, HiUsers, HiShoppingCart, HiCube } from 'react-icons/hi2';

function App() {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { messages, isLoading, addMessage, setLoading, clearMessages } = useChatStore();

  // 查询示例数据
  const queryExamples = [
    {
      icon: HiChartBar,
      title: '销售趋势分析',
      question: '显示最近30天每天的销售额变化趋势',
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: HiCube,
      title: '产品销量排行',
      question: '销量最高的前10款产品及其总销量',
      color: 'from-purple-500 to-purple-600',
    },
    {
      icon: HiUsers,
      title: '客户购买分析',
      question: '每个客户的总购买金额和订单数量统计',
      color: 'from-emerald-500 to-emerald-600',
    },
    {
      icon: HiChartBar,
      title: '产品类别对比',
      question: '各个产品类别的销售额占比分析',
      color: 'from-orange-500 to-orange-600',
    },
    {
      icon: HiShoppingCart,
      title: '订单状态分布',
      question: '不同订单状态的数量分布情况',
      color: 'from-pink-500 to-pink-600',
    },
    {
      icon: HiUsers,
      title: '客户注册趋势',
      question: '按月统计新客户注册数量的变化趋势',
      color: 'from-indigo-500 to-indigo-600',
    },
    {
      icon: HiCube,
      title: '库存预警分析',
      question: '库存数量少于10的产品清单',
      color: 'from-red-500 to-red-600',
    },
    {
      icon: HiUsers,
      title: '高价值客户',
      question: '购买总金额超过5000元的VIP客户信息',
      color: 'from-yellow-500 to-yellow-600',
    },
    {
      icon: HiCube,
      title: '产品价格分析',
      question: '不同价格区间的产品数量分布',
      color: 'from-teal-500 to-teal-600',
    },
    {
      icon: HiChartBar,
      title: '月度销售业绩',
      question: '最近6个月每月的销售额和订单数量对比',
      color: 'from-cyan-500 to-cyan-600',
    },
  ];

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    try {
      setLoading(true);

      // 添加用户消息
      addMessage({
        type: 'user',
        content,
        timestamp: new Date(),
      });

      // 调用API
      const response = await chatApi.query({ question: content });

      // 添加Bot回复
      addMessage({
        type: 'bot',
        content: response.answer,
        timestamp: new Date(),
        data: response,
      });
    } catch (error) {
      console.error('发送消息失败:', error);
      addMessage({
        type: 'bot',
        content: '抱歉，处理您的请求时发生了错误。请稍后重试。',
        timestamp: new Date(),
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (question: string) => {
    handleSendMessage(question);
  };

  const handleClearMessages = () => {
    if (messages.length > 0 && window.confirm('确定要清空所有对话记录吗？')) {
      clearMessages();
    }
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* 顶部工具栏 */}
      <header className="flex items-center justify-between px-4 py-3 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 flex-shrink-0">
        <div className="flex items-center space-x-2">
          <div className="relative">
            <HiSparkles className="h-6 w-6 text-primary animate-pulse" />
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-primary/30 rounded-full animate-ping"></div>
          </div>
          <h1 className="text-lg font-semibold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">Chat-BI</h1>
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-sm text-muted-foreground hidden sm:block">{hasMessages ? `${messages.length} 条对话` : '智能商业数据分析助手'}</div>

          {/* 清空按钮 */}
          {hasMessages && (
            <Button
              size="sm"
              variant="outline"
              onClick={handleClearMessages}
              className="text-destructive hover:text-destructive hover:bg-destructive/10 border-destructive/20 transition-all duration-200"
            >
              <HiTrash className="h-4 w-4 mr-2" />
              清空记录
            </Button>
          )}
        </div>
      </header>

      {/* 聊天区域 */}
      <div className="flex-1 overflow-hidden">
        {hasMessages ? (
          <div className="h-full overflow-y-auto">
            <div className="max-w-4xl mx-auto px-4">
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message} isLast={index === messages.length - 1} />
              ))}

              {/* 加载指示器 - 优化动画效果 */}
              {isLoading && (
                <div className="py-6">
                  <div className="flex items-start space-x-4">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center shadow-md">
                      <HiSparkles className="h-4 w-4 text-white animate-spin" />
                    </div>
                    <div className="flex-1">
                      <div className="flex space-x-1 mb-2">
                        <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-green-500 rounded-full animate-bounce [animation-delay:-0.3s] shadow-sm"></div>
                        <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-green-500 rounded-full animate-bounce [animation-delay:-0.15s] shadow-sm"></div>
                        <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-green-500 rounded-full animate-bounce shadow-sm"></div>
                      </div>
                      <p className="text-sm text-muted-foreground">正在分析您的问题...</p>
                      <div className="mt-2 w-32 h-1 bg-muted rounded-full overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-green-400 to-green-500 rounded-full animate-pulse"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} className="h-4" />
            </div>
          </div>
        ) : (
          /* 欢迎页面 - 优化视觉效果 */
          <div className="h-full overflow-y-auto p-8">
            <div className="max-w-6xl mx-auto">
              {/* 主标题区域 */}
              <div className="text-center mb-12">
                <div className="relative w-24 h-24 mx-auto mb-8">
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/30 to-primary/10 rounded-full animate-pulse"></div>
                  <div className="absolute inset-2 bg-gradient-to-br from-primary/40 to-primary/20 rounded-full flex items-center justify-center">
                    <HiSparkles className="h-12 w-12 text-primary animate-bounce" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-4 h-4 bg-primary/50 rounded-full animate-ping"></div>
                  <div className="absolute -bottom-1 -left-1 w-3 h-3 bg-primary/40 rounded-full animate-ping [animation-delay:0.5s]"></div>
                </div>

                <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-primary via-primary/80 to-primary/60 bg-clip-text text-transparent">欢迎使用 Chat-BI</h2>
                <p className="text-muted-foreground mb-8 text-lg font-medium">您的智能商业数据分析助手</p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm max-w-3xl mx-auto">
                  <div className="group flex items-center justify-center space-x-3 p-4 rounded-xl bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border border-blue-200 dark:border-blue-700/50 hover:shadow-md transition-all duration-200">
                    <div className="w-3 h-3 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full group-hover:animate-pulse"></div>
                    <span className="font-medium text-blue-700 dark:text-blue-300">自然语言查询数据库</span>
                  </div>
                  <div className="group flex items-center justify-center space-x-3 p-4 rounded-xl bg-gradient-to-r from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border border-purple-200 dark:border-purple-700/50 hover:shadow-md transition-all duration-200">
                    <div className="w-3 h-3 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full group-hover:animate-pulse"></div>
                    <span className="font-medium text-purple-700 dark:text-purple-300">生成智能数据分析报告</span>
                  </div>
                  <div className="group flex items-center justify-center space-x-3 p-4 rounded-xl bg-gradient-to-r from-emerald-50 to-emerald-100 dark:from-emerald-900/20 dark:to-emerald-800/20 border border-emerald-200 dark:border-emerald-700/50 hover:shadow-md transition-all duration-200">
                    <div className="w-3 h-3 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-full group-hover:animate-pulse"></div>
                    <span className="font-medium text-emerald-700 dark:text-emerald-300">可视化展示查询结果</span>
                  </div>
                </div>
              </div>

              {/* 查询示例区域 */}
              <div className="mb-8">
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-semibold mb-2 text-foreground">💡 尝试这些查询示例</h3>
                  <p className="text-muted-foreground">点击下方任意示例开始您的数据分析之旅</p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
                  {queryExamples.map((example, index) => (
                    <div
                      key={index}
                      onClick={() => handleExampleClick(example.question)}
                      className="group cursor-pointer p-3 rounded-lg border border-border bg-card hover:bg-accent/50 hover:shadow-md transition-all duration-200 transform hover:-translate-y-0.5"
                    >
                      <div className="flex flex-col items-center text-center space-y-2">
                        <div
                          className={`w-8 h-8 rounded-lg bg-gradient-to-br ${example.color} flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow duration-200`}
                        >
                          <example.icon className="h-4 w-4 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-medium text-xs text-foreground mb-1 group-hover:text-primary transition-colors duration-200">{example.title}</h4>
                          <p className="text-[10px] text-muted-foreground line-clamp-2 group-hover:text-foreground/80 transition-colors duration-200">{example.question}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="text-center">
                <p className="text-xs text-muted-foreground opacity-70">或在下方输入框中描述您的数据需求开始对话</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 输入区域 */}
      <ChatInput onSubmit={handleSendMessage} disabled={isLoading} className="flex-shrink-0" />

      {/* 全局通知 */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: 'hsl(var(--card))',
            color: 'hsl(var(--card-foreground))',
            border: '1px solid hsl(var(--border))',
            borderRadius: '12px',
            boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
          },
        }}
      />
    </div>
  );
}

export default App;
