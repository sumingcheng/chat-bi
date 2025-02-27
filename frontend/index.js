$(document).ready(() => {
  // 初始化Bootstrap的工具提示
  $('[data-bs-toggle="tooltip"]').tooltip()

  // 状态管理
  const state = {
    templates: [],
    currentTemplateId: null,
    currentQueryId: null
  }

  // 添加基础URL配置
  const API_BASE_URL = 'http://127.0.0.1:13000'

  // 工具函数
  const utils = {
    getRandomItem: arr => arr[Math.floor(Math.random() * arr.length)],
    createChartData: () => ({
      labels: ['一月', '二月', '三月', '四月', '五月', '六月', '七月'],
      data: Array.from({ length: 7 }, () => Math.floor(Math.random() * 100))
    })
  }

  // 消息处理
  const messageHandler = {
    send: async () => {
      const message = $('#userInput').val().trim()
      if (!message) return

      messageHandler.addToChat(message, 'user')
      $('#userInput').val('')

      const loadingMessage = messageHandler.addToChat('正在分析您的问题...', 'assistant')

      try {
        const response = await fetch(`${API_BASE_URL}/api/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ user_input: message })
        })

        const result = await response.json()
        $(loadingMessage).remove()

        if (result.status === 'success') {
          state.currentQueryId = result.query_id
          messageHandler.displayResponse(result)
        } else {
          messageHandler.addToChat('抱歉，处理您的请求时出现错误。', 'assistant')
        }
      } catch (error) {
        $(loadingMessage).remove()
        messageHandler.addToChat('抱歉，服务器出现错误。', 'assistant')
      }
    },

    displayResponse: (result) => {
      const $message = $(messageHandler.addToChat('', 'assistant'))
      const $content = $message.find('.message-content')

      if (result.sql_query) {
        $content.append($('<pre>').text(result.sql_query))
      }

      if (result.data && result.data.length > 0) {
        if (result.suggested_visualization) {
          chartHandler.add($message, result.suggested_visualization, result.data)
        } else {
          // 显示表格数据
          const $table = $('<table>').addClass('table table-sm')
          // ... 构建表格逻辑 ...
          $content.append($table)
        }
      }
    },

    addToChat: (content, type) => {
      const messageHtml = `
        <div class="message ${type}">
          <div class="message-content">${content}</div>
          ${type === 'assistant' ? `
            <div class="feedback">
              <button class="like"><i class="fas fa-thumbs-up"></i></button>
              <button class="dislike"><i class="fas fa-thumbs-down"></i></button>
            </div>
          ` : ''}
        </div>
      `
      const $message = $(messageHtml)
      $('#messageArea').append($message).scrollTop($('#messageArea')[0].scrollHeight)
      return $message[0]
    }
  }

  // 反馈处理
  const feedbackHandler = {
    submit: async (level) => {
      if (!state.currentQueryId) return

      try {
        await fetch(`${API_BASE_URL}/api/satisfaction`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            query_id: state.currentQueryId,
            satisfaction_level: level
          })
        })
      } catch (error) {
        console.error('提交反馈失败:', error)
      }
    }
  }

  // 图表处理
  const chartHandler = {
    add: ($messageDiv, type, data) => {
      const $container = $('<div>').addClass('chart-container')
      const $canvas = $('<canvas>')
      $container.append($canvas)
      $messageDiv.find('.message-content').append($container)

      const { labels, data: chartData } = utils.createChartData()
      const chartConfigs = {
        line: {
          type: 'line',
          data: {
            labels,
            datasets: [{
              label: '数据趋势',
              data: chartData,
              borderColor: '#3182ce',
              backgroundColor: 'rgba(49, 130, 206, 0.1)',
              tension: 0.3,
              fill: true
            }]
          }
        },
        bar: {
          type: 'bar',
          data: {
            labels,
            datasets: [{
              label: '数据统计',
              data: chartData,
              backgroundColor: 'rgba(49, 130, 206, 0.7)'
            }]
          }
        },
        pie: {
          type: 'pie',
          data: {
            labels,
            datasets: [{
              data: chartData,
              backgroundColor: [
                '#3182ce', '#38b2ac', '#4299e1', '#9f7aea',
                '#ed8936', '#ecc94b', '#48bb78'
              ]
            }]
          }
        }
      }

      new Chart($canvas[0].getContext('2d'), {
        ...chartConfigs[type],
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
    }
  }

  // 模板管理
  const templateHandler = {
    load: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/templates/`)
        state.templates = await response.json()
        templateHandler.render()
      } catch (error) {
        console.error('加载模板失败:', error)
      }
    },

    render: () => {
      const $list = $('#templateList').empty()

      if (state.templates.length === 0) {
        $list.append(
          $('<li>暂无模板</li>')
            .css({ fontStyle: 'italic', color: '#718096' })
        )
        return
      }

      state.templates.forEach(template => {
        const $li = $('<li>').addClass('list-group-item d-flex justify-content-between align-items-center')
        $li.append($('<div>').text(`${template.name} - ${template.description}`))

        const $actions = $('<div>').addClass('template-actions')
        $actions.append(
          $('<button>').html('<i class="fas fa-edit"></i>').click(() => templateHandler.edit(template.id)),
          $('<button>').html('<i class="fas fa-trash"></i>').click(() => templateHandler.delete(template.id))
        )

        $li.append($actions)
        $list.append($li)
      })
    },

    edit: (id) => {
      const template = state.templates.find(t => t.id === id)
      if (!template) return

      state.currentTemplateId = id
      $('#templateName').val(template.name)
      $('#templateDescription').val(template.description)
      $('#templateSQL').val(template.sql)
    },

    delete: async (id) => {
      if (!confirm('确定要删除此模板吗？')) return

      try {
        await fetch(`${API_BASE_URL}/api/templates/${id}`, { method: 'DELETE' })
        await templateHandler.load()

        if (state.currentTemplateId === id) {
          templateHandler.resetForm()
        }
      } catch (error) {
        alert('删除模板失败')
        console.error(error)
      }
    },

    save: async (e) => {
      e.preventDefault()
      const formData = {
        scenario: $('#templateName').val().trim(),
        description: $('#templateDescription').val().trim(),
        sql_text: $('#templateSQL').val().trim()
      }

      if (!formData.scenario || !formData.description || !formData.sql_text) {
        alert('请填写所有字段')
        return
      }

      try {
        if (state.currentTemplateId) {
          await fetch(`${API_BASE_URL}/api/templates/${state.currentTemplateId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
          })
        } else {
          await fetch(`${API_BASE_URL}/api/templates/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
          })
        }

        await templateHandler.load()
        templateHandler.resetForm()
      } catch (error) {
        alert('保存模板失败')
        console.error(error)
      }
    },

    resetForm: () => {
      state.currentTemplateId = null
      $('#templateForm').trigger('reset')
    }
  }

  // 事件绑定
  $('#sendBtn').on('click', messageHandler.send)
  $('#userInput').on('keypress', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      messageHandler.send()
    }
  })

  $(document).on('click', '.feedback button', function () {
    const $btn = $(this)
    const level = $btn.hasClass('like') ? 'satisfied' : 'unsatisfied'

    $btn.closest('.feedback').find('button').removeClass('active')
    $btn.addClass('active')

    feedbackHandler.submit(level)
  })

  $('#templateForm').on('submit', templateHandler.save)
  $('#cancelTemplateBtn').on('click', templateHandler.resetForm)

  // 初始化
  templateHandler.load()
})

// 切换管理员面板
function toggleAdminPanel() {
  $('#adminPanel').toggleClass('active')
}
