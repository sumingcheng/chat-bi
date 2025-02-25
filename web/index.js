// 全局变量
let templates = []
let currentTemplateId = null

// DOM 元素
const messageArea = document.getElementById('messageArea')
const userInput = document.getElementById('userInput')
const sendBtn = document.getElementById('sendBtn')
const adminBtn = document.getElementById('adminBtn')
const adminPanel = document.getElementById('adminPanel')
const closeAdminBtn = document.getElementById('closeAdminBtn')
const templateList = document.getElementById('templateList')
const templateForm = document.getElementById('templateForm')
const templateName = document.getElementById('templateName')
const templateDescription = document.getElementById('templateDescription')
const templateSQL = document.getElementById('templateSQL')
const saveTemplateBtn = document.getElementById('saveTemplateBtn')
const cancelTemplateBtn = document.getElementById('cancelTemplateBtn')

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  // 监听发送按钮点击
  sendBtn.addEventListener('click', sendMessage)

  // 监听输入框回车键
  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  })

  // 监听管理员面板按钮
  adminBtn.addEventListener('click', toggleAdminPanel)
  closeAdminBtn.addEventListener('click', toggleAdminPanel)

  // 监听模板表单提交
  templateForm.addEventListener('submit', (e) => {
    e.preventDefault()
    saveTemplate()
  })

  // 监听取消按钮
  cancelTemplateBtn.addEventListener('click', resetTemplateForm)

  // 加载模板数据
  loadTemplates()
})

// 发送消息
function sendMessage() {
  const message = userInput.value.trim()
  if (!message) return

  // 添加用户消息到聊天区域
  addMessage(message, 'user')

  // 清空输入框
  userInput.value = ''

  // 模拟处理中状态
  const loadingMessage = addMessage('正在分析您的问题...', 'assistant')

  // 模拟API调用延迟
  setTimeout(() => {
    // 移除加载消息
    messageArea.removeChild(loadingMessage)

    // 处理响应
    processResponse(message)
  }, 1500)
}

// 添加消息到聊天区域
function addMessage(content, type) {
  const messageDiv = document.createElement('div')
  messageDiv.className = `message ${type}`

  const messageContent = document.createElement('div')
  messageContent.className = 'message-content'

  const paragraph = document.createElement('p')
  paragraph.textContent = content
  messageContent.appendChild(paragraph)

  messageDiv.appendChild(messageContent)

  // 如果是助手消息，添加满意度评价
  if (type === 'assistant') {
    const feedback = document.createElement('div')
    feedback.className = 'feedback'

    const likeBtn = document.createElement('button')
    likeBtn.innerHTML = '<i class="fas fa-thumbs-up"></i>'
    likeBtn.addEventListener('click', () => handleFeedback(messageDiv, true))

    const dislikeBtn = document.createElement('button')
    dislikeBtn.innerHTML = '<i class="fas fa-thumbs-down"></i>'
    dislikeBtn.addEventListener('click', () => handleFeedback(messageDiv, false))

    feedback.appendChild(likeBtn)
    feedback.appendChild(dislikeBtn)

    messageDiv.appendChild(feedback)
  }

  messageArea.appendChild(messageDiv)

  // 滚动到底部
  messageArea.scrollTop = messageArea.scrollHeight

  return messageDiv
}

// 处理满意度评价
function handleFeedback(messageDiv, isPositive) {
  const feedbackDiv = messageDiv.querySelector('.feedback')
  const buttons = feedbackDiv.querySelectorAll('button')

  // 重置所有按钮
  buttons.forEach(btn => btn.classList.remove('active'))

  // 激活选中的按钮
  if (isPositive) {
    buttons[0].classList.add('active')
  } else {
    buttons[1].classList.add('active')
  }

  // 这里可以发送反馈到服务器
  console.log(`用户提供了${isPositive ? '正面' : '负面'}反馈`)
}

// 处理响应
function processResponse(query) {
  // 模拟不同类型的响应
  const responseTypes = ['text', 'chart', 'noData']
  const randomType = responseTypes[Math.floor(Math.random() * responseTypes.length)]

  switch (randomType) {
    case 'text':
      addMessage(`根据您的问题"${query}"，我找到了以下信息：这是一个文本回答示例。`, 'assistant')
      break

    case 'chart':
      const chartResponse = addMessage(`根据您的问题"${query}"，以下是相关的数据图表：`, 'assistant')
      addChart(chartResponse, getRandomChartType())
      break

    case 'noData':
      addMessage(`抱歉，我无法找到与"${query}"相关的数据。请尝试其他问题或修改您的查询。`, 'assistant')
      break
  }
}

// 添加图表到消息
function addChart(messageDiv, chartType) {
  const messageContent = messageDiv.querySelector('.message-content')

  const chartContainer = document.createElement('div')
  chartContainer.className = 'chart-container'

  const canvas = document.createElement('canvas')
  chartContainer.appendChild(canvas)
  messageContent.appendChild(chartContainer)

  // 创建随机数据
  const labels = ['一月', '二月', '三月', '四月', '五月', '六月', '七月']
  const data = Array.from({ length: 7 }, () => Math.floor(Math.random() * 100))

  // 创建图表
  const ctx = canvas.getContext('2d')
  let chart

  switch (chartType) {
    case 'line':
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '数据趋势',
            data: data,
            borderColor: '#3182ce',
            backgroundColor: 'rgba(49, 130, 206, 0.1)',
            tension: 0.3,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
      break

    case 'bar':
      chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: '数据统计',
            data: data,
            backgroundColor: 'rgba(49, 130, 206, 0.7)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
      break

    case 'pie':
      chart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: [
              '#3182ce', '#38b2ac', '#4299e1', '#9f7aea',
              '#ed8936', '#ecc94b', '#48bb78'
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
      break
  }

  // 滚动到底部
  messageArea.scrollTop = messageArea.scrollHeight
}

// 获取随机图表类型
function getRandomChartType() {
  const types = ['line', 'bar', 'pie']
  return types[Math.floor(Math.random() * types.length)]
}

// 切换管理员面板
function toggleAdminPanel() {
  adminPanel.classList.toggle('active')
}

// 加载模板数据
function loadTemplates() {
  // 模拟从服务器获取模板数据
  templates = [
    { id: 1, name: '销售趋势', description: '过去7天的销售趋势', sql: 'SELECT date, SUM(amount) FROM sales WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) GROUP BY date' },
    { id: 2, name: '产品分类统计', description: '各产品类别的销售额', sql: 'SELECT category, SUM(amount) FROM sales GROUP BY category' }
  ]

  renderTemplates()
}

// 渲染模板列表
function renderTemplates() {
  templateList.innerHTML = ''

  if (templates.length === 0) {
    const emptyMessage = document.createElement('li')
    emptyMessage.textContent = '暂无模板'
    emptyMessage.style.fontStyle = 'italic'
    emptyMessage.style.color = '#718096'
    templateList.appendChild(emptyMessage)
    return
  }

  templates.forEach(template => {
    const li = document.createElement('li')

    const templateInfo = document.createElement('div')
    templateInfo.className = 'template-info'
    templateInfo.textContent = `${template.name} - ${template.description}`

    const actions = document.createElement('div')
    actions.className = 'template-actions'

    const editBtn = document.createElement('button')
    editBtn.innerHTML = '<i class="fas fa-edit"></i>'
    editBtn.addEventListener('click', () => editTemplate(template.id))

    const deleteBtn = document.createElement('button')
    deleteBtn.innerHTML = '<i class="fas fa-trash"></i>'
    deleteBtn.addEventListener('click', () => deleteTemplate(template.id))

    actions.appendChild(editBtn)
    actions.appendChild(deleteBtn)

    li.appendChild(templateInfo)
    li.appendChild(actions)

    templateList.appendChild(li)
  })
}

// 编辑模板
function editTemplate(id) {
  const template = templates.find(t => t.id === id)
  if (!template) return

  currentTemplateId = id
  templateName.value = template.name
  templateDescription.value = template.description
  templateSQL.value = template.sql
}

// 删除模板
function deleteTemplate(id) {
  if (confirm('确定要删除此模板吗？')) {
    templates = templates.filter(t => t.id !== id)
    renderTemplates()

    // 如果正在编辑被删除的模板，重置表单
    if (currentTemplateId === id) {
      resetTemplateForm()
    }
  }
}

// 保存模板
function saveTemplate() {
  const name = templateName.value.trim()
  const description = templateDescription.value.trim()
  const sql = templateSQL.value.trim()

  if (!name || !description || !sql) {
    alert('请填写所有字段')
    return
  }

  if (currentTemplateId) {
    // 更新现有模板
    const index = templates.findIndex(t => t.id === currentTemplateId)
    if (index !== -1) {
      templates[index] = {
        id: currentTemplateId,
        name,
        description,
        sql
      }
    }
  } else {
    // 添加新模板
    const newId = templates.length > 0 ? Math.max(...templates.map(t => t.id)) + 1 : 1
    templates.push({
      id: newId,
      name,
      description,
      sql
    })
  }

  renderTemplates()
  resetTemplateForm()
}

// 重置模板表单
function resetTemplateForm() {
  currentTemplateId = null
  templateForm.reset()
}
