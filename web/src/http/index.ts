import axios, { type AxiosResponse } from 'axios'
import toast from 'react-hot-toast'

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:13000/api',
  timeout: 1000 * 60 * 60,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等认证信息
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response

    // 后端统一返回格式：{ success: boolean, data: any, error?: any }
    if (data.success) {
      return data.data // 直接返回data字段
    } else {
      // 业务错误
      const errorMsg = data.error?.message || '请求失败'
      toast.error(errorMsg)
      return Promise.reject(new Error(errorMsg))
    }
  },
  (error) => {
    // 网络错误或HTTP状态码错误
    const errorMsg = error.response?.data?.message || error.message || '网络错误'
    toast.error(errorMsg)
    return Promise.reject(error)
  }
)

export default request
