import { useAuthStore } from '../stores/auth'

class ChatWebSocketService {
  constructor() {
    this.ws = null
    this.messageHandlers = []
    this.connectionHandlers = []
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.messageHistory = []
    this.retryTimeout = null
  }

  // Подключение к WebSocket
  async connect(onMessage, onConnectionStatus) {
    const authStore = useAuthStore()
    
    if (!authStore.token) {
      throw new Error('Токен авторизации отсутствует')
    }

    // Добавляем обработчики
    this.addMessageHandler(onMessage)
    this.addConnectionHandler(onConnectionStatus)

    // Если уже подключены, возвращаем
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      return true
    }

    try {
      // Очищаем предыдущий таймаут реконнекта
      if (this.retryTimeout) {
        clearTimeout(this.retryTimeout)
        this.retryTimeout = null
      }

      // Формируем URL с токеном (ВАЖНО: правильный путь к вашему бекенду)
      const wsUrl = this.buildWebSocketUrl(authStore.token)
      console.log('Подключаемся к WebSocket:', wsUrl)
      
      this.ws = new WebSocket(wsUrl)

      return new Promise((resolve, reject) => {
        // Таймаут подключения (10 секунд)
        const connectionTimeout = setTimeout(() => {
          if (this.ws.readyState !== WebSocket.OPEN) {
            this.ws.close()
            reject(new Error('Таймаут подключения к WebSocket'))
          }
        }, 10000)

        this.ws.onopen = () => {
          console.log('✅ WebSocket подключен')
          clearTimeout(connectionTimeout)
          this.reconnectAttempts = 0
          this.notifyConnectionStatus(true)
          resolve(true)
        }

        this.ws.onmessage = (event) => {
          console.log('📨 Получено сообщение:', event.data)
          this.handleMessage(event.data)
        }

        this.ws.onclose = (event) => {
          console.log('❌ WebSocket отключен. Код:', event.code, 'Причина:', event.reason)
          clearTimeout(connectionTimeout)
          this.notifyConnectionStatus(false)
          
          // Не пытаемся переподключаться если пользователь сам отключился (код 1000)
          if (event.code !== 1000) {
            this.attemptReconnect()
          }
        }

        this.ws.onerror = (error) => {
          console.error('⚠️ WebSocket ошибка:', error)
          clearTimeout(connectionTimeout)
          this.notifyConnectionStatus(false)
          reject(error)
        }
      })
    } catch (error) {
      console.error('Ошибка подключения к WebSocket:', error)
      throw error
    }
  }

  // Построение URL для WebSocket (ИСПРАВЛЕНО!)
  buildWebSocketUrl(token) {
    // Получаем базовый URL из .env или используем localhost по умолчанию
    const apiUrl = import.meta.env.VITE_API_URL || 'localhost:8000'
    
    // Определяем протокол WebSocket (ws или wss)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    
    // Убираем http/https из URL если они есть
    const cleanApiUrl = apiUrl.replace(/^https?:\/\//, '')
    
    // Формируем полный URL (ВАЖНО: правильный путь к endpoint)
    return `${protocol}//${cleanApiUrl}/chat/ws?token=${encodeURIComponent(token)}`
  }

  // Обработка входящих сообщений
  handleMessage(data) {
    try {
      const message = JSON.parse(data)
      console.log('📝 Парсинг сообщения:', message)
      
      // Добавляем тип сообщения для удобства
      if (!message.type) {
        if (message.action) {
          message.type = 'connection'
        } else if (message.is_admin !== undefined) {
          message.type = 'user'
        } else {
          message.type = 'system'
        }
      }
      
      this.messageHistory.push(message)
      
      // Уведомляем все обработчики
      this.messageHandlers.forEach(handler => {
        try {
          handler(message)
        } catch (error) {
          console.error('Ошибка в обработчике сообщения:', error)
        }
      })
    } catch (error) {
      console.error('Ошибка парсинга сообщения:', error, 'Данные:', data)
      
      // Если это не JSON, все равно добавляем как системное сообщение
      const fallbackMessage = {
        type: 'system',
        message: data,
        timestamp: new Date().toISOString(),
        id: Date.now()
      }
      
      this.messageHistory.push(fallbackMessage)
      this.messageHandlers.forEach(handler => handler(fallbackMessage))
    }
  }

  sendMessage(text) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket не подключен')
    }

    if (!text.trim()) {
      return
    }

    try {
      const messageData = text.trim()
      
      console.log('📤 Отправка сообщения:', messageData)
      this.ws.send(messageData)

      const authStore = useAuthStore()
      const tempMessage = {
        id: Date.now(),
        type: 'user',
        user_id: authStore.user?.id,
        user_name: authStore.user?.full_name || 'Вы',
        user_email: authStore.user?.email,
        is_admin: authStore.user?.is_admin || false,
        message: text.trim(),
        created_at: new Date().toISOString(),
        timestamp: new Date().toISOString()
      }
      
      this.messageHandlers.forEach(handler => handler(tempMessage))
      
      return true
    } catch (error) {
      console.error('Ошибка отправки сообщения:', error)
      throw error
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log('Превышено максимальное количество попыток переподключения')
      return
    }

    this.reconnectAttempts++

    const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1), 30000)

    console.log(`🔄 Попытка переподключения ${this.reconnectAttempts}/${this.maxReconnectAttempts} через ${delay}ms`)

    this.retryTimeout = setTimeout(async () => {
      try {
        await this.connect()
      } catch (error) {
        console.error('Ошибка переподключения:', error)
        this.attemptReconnect()
      }
    }, delay)
  }

  disconnect() {
    console.log('Отключение WebSocket...')

    if (this.retryTimeout) {
      clearTimeout(this.retryTimeout)
      this.retryTimeout = null
    }
    
    if (this.ws) {

      this.ws.onclose = null
      this.ws.onerror = null
      
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.close(1000, 'Пользователь отключился')
      }
      
      this.ws = null
    }

    this.messageHandlers = []
    this.connectionHandlers = []
    this.reconnectAttempts = 0
    
    console.log('WebSocket отключен')
  }

  addMessageHandler(handler) {
    if (handler && typeof handler === 'function') {
      this.messageHandlers.push(handler)
    }
  }

  removeMessageHandler(handler) {
    const index = this.messageHandlers.indexOf(handler)
    if (index > -1) {
      this.messageHandlers.splice(index, 1)
    }
  }

  addConnectionHandler(handler) {
    if (handler && typeof handler === 'function') {
      this.connectionHandlers.push(handler)
    }
  }

  removeConnectionHandler(handler) {
    const index = this.connectionHandlers.indexOf(handler)
    if (index > -1) {
      this.connectionHandlers.splice(index, 1)
    }
  }

  notifyConnectionStatus(connected) {
    console.log(`📡 Статус соединения: ${connected ? 'Подключено' : 'Отключено'}`)
    this.connectionHandlers.forEach(handler => {
      try {
        handler(connected)
      } catch (error) {
        console.error('Ошибка в обработчике статуса соединения:', error)
      }
    })
  }

  getHistory() {
    return [...this.messageHistory]
  }

  clearHistory() {
    this.messageHistory = []
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN
  }

  getStatus() {
    if (!this.ws) return 'disconnected'
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting'
      case WebSocket.OPEN:
        return 'connected'
      case WebSocket.CLOSING:
        return 'closing'
      case WebSocket.CLOSED:
        return 'disconnected'
      default:
        return 'unknown'
    }
  }
}

export const chatService = new ChatWebSocketService()