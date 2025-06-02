import * as React from "react"
import { useState, useRef, useEffect } from "react"
import { Button } from "./ui/Button"
import { Textarea } from "./ui/Textarea"
import { cn } from "../lib/utils"
import { HiPaperAirplane, HiStop } from "react-icons/hi2"
import { useChatStore } from "../store/chat"

interface ChatInputProps {
  onSubmit: (message: string) => void
  disabled?: boolean
  className?: string
}

export function ChatInput({ onSubmit, disabled = false, className }: ChatInputProps) {
  const [input, setInput] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const { isLoading } = useChatStore()

  // 自动调整textarea高度
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const handleSubmit = () => {
    if (input.trim() && !disabled && !isLoading) {
      onSubmit(input.trim())
      setInput("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleStop = () => {
    // 这里可以添加停止生成的逻辑
    console.log("停止生成")
  }

  return (
    <div className={cn("border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60", className)}>
      <div className="max-w-4xl mx-auto p-4">
        <div className="relative">
          <Textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入您的问题... (Shift + Enter 换行)"
            disabled={disabled}
            className={cn(
              "min-h-[56px] max-h-[200px] resize-none rounded-xl border-2 pr-12",
              "focus:border-primary/50 focus:ring-0 focus:ring-offset-0",
              "scrollbar-thin scrollbar-thumb-muted scrollbar-track-transparent"
            )}
            rows={1}
          />
          
          {/* 发送按钮 */}
          <div className="absolute bottom-2 right-2">
            {isLoading ? (
              <Button
                size="icon"
                variant="ghost"
                className="h-8 w-8 rounded-full bg-red-500 hover:bg-red-600 text-white"
                onClick={handleStop}
              >
                <HiStop className="h-4 w-4" />
              </Button>
            ) : (
              <Button
                size="icon"
                variant="ghost"
                className={cn(
                  "h-8 w-8 rounded-full",
                  input.trim() && !disabled
                    ? "bg-primary hover:bg-primary/90 text-primary-foreground"
                    : "bg-muted text-muted-foreground cursor-not-allowed"
                )}
                onClick={handleSubmit}
                disabled={!input.trim() || disabled || isLoading}
              >
                <HiPaperAirplane className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
        
        {/* 提示文本 */}
        <div className="mt-2 text-xs text-muted-foreground text-center">
          Chat-BI 可以协助您进行数据分析和查询。请详细描述您的需求。
        </div>
      </div>
    </div>
  )
}