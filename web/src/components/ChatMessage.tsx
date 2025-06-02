import { Avatar, AvatarFallback } from './ui/Avatar';
import { Button } from './ui/Button';
import { Tooltip, TooltipContent, TooltipTrigger, TooltipProvider } from './ui/Tooltip';
import { cn, formatDate } from '../lib/utils';
import { HiUser, HiCpuChip, HiClipboard, HiCheck } from 'react-icons/hi2';
import type { ChatMessage as ChatMessageType } from '../store/chat';
import { useState } from 'react';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const [copied, setCopied] = useState(false);
  const isUser = message.type === 'user';

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

  return (
    <TooltipProvider>
      <div className={cn('group relative py-6 px-4 mx-auto max-w-4xl', isUser ? 'bg-background' : 'bg-muted/30')}>
        <div className="flex items-start space-x-4">
          {/* 头像 */}
          <Avatar className="h-8 w-8 flex-shrink-0">
            <AvatarFallback className={cn(isUser ? 'bg-blue-500 text-white' : 'bg-green-500 text-white')}>
              {isUser ? <HiUser className="h-4 w-4" /> : <HiCpuChip className="h-4 w-4" />}
            </AvatarFallback>
          </Avatar>

          <div className="flex-1 min-w-0">
            {/* 消息内容 */}
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-sm leading-relaxed whitespace-pre-wrap break-words m-0">{message.content}</p>
            </div>

            {/* Bot消息的额外信息 */}
            {message.data && (
              <div className="mt-4 space-y-3">
                {/* SQL查询 */}
                <div className="bg-card border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-medium">SQL查询</h4>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button size="icon" variant="ghost" className="h-6 w-6" onClick={() => handleCopy(message.data!.sql)}>
                          {copied ? <HiCheck className="h-3 w-3 text-green-500" /> : <HiClipboard className="h-3 w-3" />}
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>{copied ? '已复制' : '复制SQL'}</TooltipContent>
                    </Tooltip>
                  </div>
                  <pre className="text-xs bg-muted p-3 rounded font-mono overflow-x-auto whitespace-pre-wrap">{message.data.sql}</pre>
                </div>

                {/* 查询结果统计 */}
                <div className="bg-card border rounded-lg p-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">结果数量:</span>
                      <span className="ml-2 font-medium">{message.data.record_count} 条</span>
                    </div>
                    <div>
                      <span className="text-muted-foreground">图表类型:</span>
                      <span className="ml-2 font-medium capitalize">{message.data.chart_data.type}</span>
                    </div>
                  </div>
                </div>

                {/* 数据预览 */}
                {message.data.chart_data.data.length > 0 && (
                  <div className="bg-card border rounded-lg p-4">
                    <h4 className="text-sm font-medium mb-3">数据预览</h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-xs">
                        <thead>
                          <tr className="border-b">
                            {Object.keys(message.data.chart_data.data[0]).map((key) => (
                              <th key={key} className="text-left p-2 font-medium text-muted-foreground">
                                {key}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {message.data.chart_data.data.slice(0, 3).map((row, index) => (
                            <tr key={index} className="border-b">
                              {Object.values(row).map((value, i) => (
                                <td key={i} className="p-2">
                                  {String(value)}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                      {message.data.chart_data.data.length > 3 && (
                        <p className="text-xs text-muted-foreground mt-2 text-center">... 还有 {message.data.chart_data.data.length - 3} 条数据</p>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 时间戳 */}
            <div className="mt-3 text-xs text-muted-foreground">{formatDate(message.timestamp)}</div>
          </div>

          {/* 复制按钮 */}
          <div className="opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0">
            <Tooltip>
              <TooltipTrigger asChild>
                <Button size="icon" variant="ghost" className="h-6 w-6" onClick={() => handleCopy(message.content)}>
                  {copied ? <HiCheck className="h-3 w-3 text-green-500" /> : <HiClipboard className="h-3 w-3" />}
                </Button>
              </TooltipTrigger>
              <TooltipContent>{copied ? '已复制' : '复制消息'}</TooltipContent>
            </Tooltip>
          </div>
        </div>
      </div>
    </TooltipProvider>
  );
}
