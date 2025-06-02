import { useEffect, useRef } from 'react';
import { Toaster } from 'react-hot-toast';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { Button } from './components/ui/Button';
import { useChatStore } from './store/chat';
import { chatApi } from './http/chat';
import { HiSparkles, HiTrash } from 'react-icons/hi2';

function App() {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { messages, isLoading, addMessage, setLoading, clearMessages } = useChatStore();

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
          <div className="text-sm text-muted-foreground hidden sm:block">
            {hasMessages ? `${messages.length} 条对话` : '智能商业数据分析助手'}
          </div>

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
                <ChatMessage 
                  key={index} 
                  message={message} 
                  isLast={index === messages.length - 1}
                />
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
          <div className="h-full flex items-center justify-center p-8">
            <div className="text-center max-w-md">
              <div className="relative w-24 h-24 mx-auto mb-8">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/30 to-primary/10 rounded-full animate-pulse"></div>
                <div className="absolute inset-2 bg-gradient-to-br from-primary/40 to-primary/20 rounded-full flex items-center justify-center">
                  <HiSparkles className="h-12 w-12 text-primary animate-bounce" />
                </div>
                <div className="absolute -top-2 -right-2 w-4 h-4 bg-primary/50 rounded-full animate-ping"></div>
                <div className="absolute -bottom-1 -left-1 w-3 h-3 bg-primary/40 rounded-full animate-ping [animation-delay:0.5s]"></div>
              </div>
              
              <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-primary via-primary/80 to-primary/60 bg-clip-text text-transparent">
                欢迎使用 Chat-BI
              </h2>
              <p className="text-muted-foreground mb-8 text-lg font-medium">您的智能商业数据分析助手</p>
              
              <div className="space-y-4 text-sm">
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
              
              <p className="text-xs text-muted-foreground mt-8 opacity-70">在下方输入框中描述您的数据需求开始对话</p>
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
