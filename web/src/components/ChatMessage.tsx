import { Avatar, AvatarFallback } from './ui/Avatar';
import { Button } from './ui/Button';
import { Tooltip, TooltipContent, TooltipTrigger, TooltipProvider } from './ui/Tooltip';
import { cn, formatDate } from '../lib/utils';
import { 
  HiUser, 
  HiCpuChip, 
  HiClipboard, 
  HiCheck, 
  HiCodeBracket,
  HiChartBarSquare,
  HiTableCells,
  HiEye,
  HiSparkles
} from 'react-icons/hi2';
import type { ChatMessage as ChatMessageType } from '../store/chat';
import { useState } from 'react';

interface ChatMessageProps {
  message: ChatMessageType;
  isLast?: boolean;
}

export function ChatMessage({ message, isLast = false }: ChatMessageProps) {
  const [copied, setCopied] = useState(false);
  const [copiedSql, setCopiedSql] = useState(false);
  const isUser = message.type === 'user';

  const handleCopy = async (text: string, isSql = false) => {
    try {
      await navigator.clipboard.writeText(text);
      if (isSql) {
        setCopiedSql(true);
        setTimeout(() => setCopiedSql(false), 2000);
      } else {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

  return (
    <TooltipProvider>
      <div className={cn('group relative py-6 px-4 mx-auto max-w-4xl', isUser ? 'bg-background' : 'bg-muted/30')}>
        <div className="flex items-start space-x-4">
          {/* 头像 - 优化渐变效果 */}
          <Avatar className="h-8 w-8 flex-shrink-0">
            <AvatarFallback className={cn(
              isUser 
                ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-md' 
                : 'bg-gradient-to-br from-green-500 to-green-600 text-white shadow-md'
            )}>
              {isUser ? <HiUser className="h-4 w-4" /> : <HiSparkles className="h-4 w-4" />}
            </AvatarFallback>
          </Avatar>

          <div className="flex-1 min-w-0">
            {/* 消息内容 */}
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-sm leading-relaxed whitespace-pre-wrap break-words m-0">{message.content}</p>
            </div>

            {/* Bot消息的额外信息 */}
            {message.data && (
              <div className="mt-6 space-y-4">
                {/* SQL查询 - 优化设计 */}
                <div className="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden shadow-sm">
                  <div className="flex items-center justify-between p-4 bg-gradient-to-r from-slate-100 to-slate-50 dark:from-slate-800 dark:to-slate-700 border-b border-slate-200 dark:border-slate-600">
                    <div className="flex items-center space-x-2">
                      <div className="p-1.5 bg-blue-500 rounded-md">
                        <HiCodeBracket className="h-4 w-4 text-white" />
                      </div>
                      <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300">SQL查询</h4>
                    </div>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button 
                          size="sm" 
                          variant="ghost" 
                          className="h-8 px-3 text-xs hover:bg-white/50 dark:hover:bg-slate-700/50" 
                          onClick={() => handleCopy(message.data!.sql, true)}
                        >
                          {copiedSql ? (
                            <>
                              <HiCheck className="h-3 w-3 text-green-500 mr-1.5" />
                              <span className="text-green-600 dark:text-green-400">已复制</span>
                            </>
                          ) : (
                            <>
                              <HiClipboard className="h-3 w-3 mr-1.5" />
                              复制
                            </>
                          )}
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>{copiedSql ? '已复制到剪贴板' : '复制SQL代码'}</TooltipContent>
                    </Tooltip>
                  </div>
                  <div className="p-4">
                    <pre className="text-xs bg-slate-900 dark:bg-slate-950 text-green-400 p-4 rounded-lg font-mono overflow-x-auto whitespace-pre-wrap shadow-inner border border-slate-700">
                      <code>{message.data.sql}</code>
                    </pre>
                  </div>
                </div>

                {/* 查询结果统计 - 优化卡片设计 */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border border-blue-200 dark:border-blue-700/50 rounded-xl p-4 shadow-sm">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-blue-500 rounded-lg">
                        <HiTableCells className="h-4 w-4 text-white" />
                      </div>
                      <div>
                        <p className="text-xs text-blue-600 dark:text-blue-400 font-medium">结果数量</p>
                        <p className="text-lg font-bold text-blue-800 dark:text-blue-300">{message.data.record_count} 条</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border border-purple-200 dark:border-purple-700/50 rounded-xl p-4 shadow-sm">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-purple-500 rounded-lg">
                        <HiChartBarSquare className="h-4 w-4 text-white" />
                      </div>
                      <div>
                        <p className="text-xs text-purple-600 dark:text-purple-400 font-medium">图表类型</p>
                        <p className="text-lg font-bold text-purple-800 dark:text-purple-300 capitalize">{message.data.chart_data.type}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* 数据预览 - 优化表格设计 */}
                {message.data.chart_data.data.length > 0 && (
                  <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900/20 dark:to-emerald-800/20 border border-emerald-200 dark:border-emerald-700/50 rounded-xl overflow-hidden shadow-sm">
                    <div className="flex items-center space-x-2 p-4 bg-gradient-to-r from-emerald-100 to-emerald-50 dark:from-emerald-800/30 dark:to-emerald-700/30 border-b border-emerald-200 dark:border-emerald-600/50">
                      <div className="p-1.5 bg-emerald-500 rounded-md">
                        <HiEye className="h-4 w-4 text-white" />
                      </div>
                      <h4 className="text-sm font-semibold text-emerald-700 dark:text-emerald-300">数据预览</h4>
                    </div>
                    <div className="overflow-x-auto">
                      <table className="w-full text-xs">
                        <thead>
                          <tr className="bg-emerald-100/50 dark:bg-emerald-800/20">
                            {Object.keys(message.data.chart_data.data[0]).map((key) => (
                              <th key={key} className="text-left p-3 font-semibold text-emerald-700 dark:text-emerald-300 border-b border-emerald-200 dark:border-emerald-600/30">
                                {key}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {message.data.chart_data.data.slice(0, 3).map((row, index) => (
                            <tr key={index} className={cn(
                              "border-b border-emerald-100 dark:border-emerald-700/30 hover:bg-emerald-50 dark:hover:bg-emerald-800/10 transition-colors",
                              index % 2 === 0 ? "bg-white/50 dark:bg-emerald-900/5" : "bg-emerald-50/30 dark:bg-emerald-800/5"
                            )}>
                              {Object.values(row).map((value, i) => (
                                <td key={i} className="p-3 text-emerald-800 dark:text-emerald-200 font-medium">
                                  {String(value)}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                      {message.data.chart_data.data.length > 3 && (
                        <div className="p-3 text-center bg-emerald-50/50 dark:bg-emerald-800/10">
                          <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                            ... 还有 {message.data.chart_data.data.length - 3} 条数据
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 时间戳 */}
            <div className="mt-4 text-xs text-muted-foreground">{formatDate(message.timestamp)}</div>
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
        
        {/* 分割线 - 最后一条消息不显示 */}
        {!isLast && (
          <div className="mt-6 mx-4">
            <div className="h-px bg-gradient-to-r from-transparent via-border to-transparent opacity-50"></div>
          </div>
        )}
      </div>
    </TooltipProvider>
  );
}
