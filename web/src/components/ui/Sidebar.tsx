import * as React from "react"
import { Button } from "./Button"
import { cn } from "../../lib/utils"
import { HiTrash, HiSparkles } from "react-icons/hi2"
import { useChatStore } from "../../store/chat"

interface SidebarProps {
  className?: string
}

export function Sidebar({ className }: SidebarProps) {
  const { clearMessages, messages } = useChatStore()
  
  const handleClearMessages = () => {
    if (messages.length > 0 && window.confirm('确定要清空所有对话记录吗？')) {
      clearMessages()
    }
  }

  const hasMessages = messages.length > 0

  return (
    <div className={cn("flex flex-col h-full bg-card border-r", className)}>
      {/* 标题区域 */}
      <div className="p-4 border-b">
        <div className="flex items-center gap-3">
          <HiSparkles className="h-6 w-6 text-primary" />
          <h2 className="text-lg font-semibold">Chat-BI</h2>
        </div>
        <p className="text-xs text-muted-foreground mt-1">智能商业分析对话系统</p>
      </div>

      {/* 中间内容区域 */}
      <div className="flex-1 p-4">
        {hasMessages ? (
          <div className="space-y-4">
            <div className="text-sm text-muted-foreground">
              当前会话包含 {messages.length} 条消息
            </div>
            
            {/* 清空记录按钮 */}
            <Button 
              onClick={handleClearMessages}
              variant="outline"
              className="w-full justify-start gap-3 text-destructive hover:text-destructive"
            >
              <HiTrash className="h-4 w-4" />
              清空对话记录
            </Button>
          </div>
        ) : (
          <div className="text-center text-muted-foreground py-8">
            <HiSparkles className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">暂无对话记录</p>
            <p className="text-xs mt-1">开始您的第一个问题吧</p>
          </div>
        )}
      </div>

      {/* 底部信息 */}
      <div className="p-4 border-t">
        <div className="text-xs text-muted-foreground space-y-1">
          <p>Chat-BI v1.0</p>
          <p>支持自然语言查询数据库</p>
        </div>
      </div>
    </div>
  )
} 