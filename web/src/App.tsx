import * as React from 'react';
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
          <HiSparkles className="h-6 w-6 text-primary" />
          <h1 className="text-lg font-semibold">Chat-BI</h1>
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-sm text-muted-foreground hidden sm:block">{hasMessages ? `${messages.length} 条对话` : '智能商业数据分析助手'}</div>

          {/* 清空按钮 */}
          {hasMessages && (
            <Button size="sm" variant="outline" onClick={handleClearMessages} className="text-destructive hover:text-destructive">
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
                <ChatMessage key={index} message={message} />
              ))}

              {/* 加载指示器 */}
              {isLoading && (
                <div className="py-6">
                  <div className="flex items-start space-x-4">
                    <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
                      <HiSparkles className="h-4 w-4 text-white animate-pulse" />
                    </div>
                    <div className="flex-1">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                      </div>
                      <p className="text-sm text-muted-foreground mt-2">正在分析您的问题...</p>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} className="h-4" />
            </div>
          </div>
        ) : (
          /* 欢迎页面 */
          <div className="h-full flex items-center justify-center p-8">
            <div className="text-center max-w-md">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-primary/20 to-primary/10 rounded-full flex items-center justify-center">
                <HiSparkles className="h-10 w-10 text-primary" />
              </div>
              <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">欢迎使用 Chat-BI</h2>
              <p className="text-muted-foreground mb-8 text-lg">您的智能商业数据分析助手</p>
              <div className="space-y-4 text-sm">
                <div className="flex items-center justify-center space-x-3 p-3 rounded-lg bg-muted/30">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  <span>自然语言查询数据库</span>
                </div>
                <div className="flex items-center justify-center space-x-3 p-3 rounded-lg bg-muted/30">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  <span>生成智能数据分析报告</span>
                </div>
                <div className="flex items-center justify-center space-x-3 p-3 rounded-lg bg-muted/30">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  <span>可视化展示查询结果</span>
                </div>
              </div>
              <p className="text-xs text-muted-foreground mt-8">在下方输入框中描述您的数据需求开始对话</p>
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
          },
        }}
      />
    </div>
  );
}

export default App;
