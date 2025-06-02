import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // 允许外部访问
    port: 5173,      // 指定端口
    strictPort: true, // 端口被占用时不自动尝试下一个端口
    open: true,      // 自动打开浏览器
  },
})
