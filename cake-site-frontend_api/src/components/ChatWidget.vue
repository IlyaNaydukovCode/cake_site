<template>
  <div class="chat-widget" :class="{ 'chat-expanded': isExpanded }">
    <!-- Кнопка открытия/закрытия -->
    <div class="chat-toggle" @click="toggleChat">
      <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
      <span class="toggle-icon">
        <span v-if="isExpanded">✕</span>
        <span v-else>💬</span>
      </span>
    </div>

    <!-- Контейнер чата -->
    <div v-if="isExpanded" class="chat-container">
      <div class="chat-header">
        <div class="header-left">
          <h3>Чат поддержки</h3>
          <span class="online-status">
            <span class="status-dot" :class="{ 
              online: isConnected, 
              connecting: connectionStatus === 'connecting' 
            }"></span>
            {{ connectionStatusText }}
          </span>
        </div>
        <button v-if="isConnected" @click="reconnect" class="reconnect-btn" title="Переподключиться">
          🔄
        </button>
      </div>

      <!-- Сообщения -->
      <div ref="messagesContainer" class="chat-messages">
        <div v-if="loading" class="loading-messages">
          <div class="spinner"></div>
          <span>Подключение к чату...</span>
        </div>
        
        <div v-else-if="messages.length === 0" class="empty-messages">
          <div class="empty-icon">💬</div>
          <p>Чат пуст</p>
          <p class="empty-hint">Начните общение!</p>
        </div>
        
        <div v-else>
          <div v-for="message in messages" :key="message.id || message.timestamp" 
               :class="['message', getMessageClass(message)]">
            <div class="message-header">
              <span class="message-sender">
                <template v-if="message.type === 'system' || message.action">
                  🤖 Система
                </template>
                <template v-else-if="message.user_id === currentUser?.id">
                  ✨ Вы
                </template>
                <template v-else>
                  👤 {{ message.user_name || 'Пользователь' }}
                  <span v-if="message.is_admin" class="admin-badge">Админ</span>
                </template>
              </span>
              <span class="message-time">
                {{ formatTime(message.timestamp || message.created_at) }}
              </span>
            </div>
            <div class="message-content">{{ message.message }}</div>
            
            <div v-if="message.is_broadcast" class="message-broadcast">
              📢 Рассылка
            </div>
            
            <div v-if="message.action === 'connected'" class="connection-event connected">
              ✅ Пользователь подключился
            </div>
            <div v-if="message.action === 'disconnected'" class="connection-event disconnected">
              ❌ Пользователь отключился
            </div>
          </div>
        </div>
      </div>

      <!-- Поле ввода -->
      <div class="chat-input-area">
        <div v-if="!isConnected && connectionStatus !== 'connecting'" class="connection-error">
          <div class="error-icon">⚠️</div>
          <div class="error-text">
            <strong>Соединение потеряно</strong>
            <p>Попробуйте переподключиться</p>
          </div>
          <button @click="reconnect" class="retry-btn">Повторить</button>
        </div>
        
        <div v-else-if="connectionStatus === 'connecting'" class="connection-connecting">
          <div class="spinner small"></div>
          <span>Подключение...</span>
        </div>
        
        <div class="input-wrapper">
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            @input="onInputChange"
            type="text"
            placeholder="Введите сообщение..."
            :disabled="!isConnected || sending"
            class="message-input"
            ref="messageInput"
          />
          <button 
            @click="sendMessage" 
            :disabled="!isConnected || sending || !inputMessage.trim()"
            class="send-button"
            :title="!isConnected ? 'Нет соединения' : 'Отправить'"
          >
            <span v-if="sending" class="sending-spinner"></span>
            <span v-else>➤</span>
          </button>
        </div>
        
        <div v-if="currentUser?.is_admin" class="admin-commands">
          <small><strong>Админ-команды:</strong> /users - список онлайн, /broadcast [сообщение] - рассылка</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { chatService } from '../services/websocket'

export default {
  name: 'ChatWidget',
  
  setup() {
    const authStore = useAuthStore()
    const isExpanded = ref(false)
    const isConnected = ref(false)
    const connectionStatus = ref('disconnected') // 'disconnected', 'connecting', 'connected'
    const inputMessage = ref('')
    const messages = ref([])
    const sending = ref(false)
    const loading = ref(true)
    const unreadCount = ref(0)
    const messagesContainer = ref(null)
    const messageInput = ref(null)

    const currentUser = computed(() => authStore.user)

    // Текст статуса соединения
    const connectionStatusText = computed(() => {
      switch (connectionStatus.value) {
        case 'connected': return 'Онлайн'
        case 'connecting': return 'Подключение...'
        case 'disconnected': return 'Оффлайн'
        default: return connectionStatus.value
      }
    })

    // Подключение к WebSocket
    const connectWebSocket = async () => {
      if (!currentUser.value) {
        console.log('Пользователь не авторизован, не подключаемся к WebSocket')
        loading.value = false
        return
      }
      
      console.log('🔄 Попытка подключения к WebSocket...')
      connectionStatus.value = 'connecting'
      loading.value = true
      
      try {
        await chatService.connect(
          onMessageReceived,
          onConnectionStatusChange
        )
        console.log('✅ Успешно подключились к WebSocket')
      } catch (error) {
        console.error('❌ Ошибка подключения к чату:', error)
        connectionStatus.value = 'disconnected'
        loading.value = false
        
        // Показываем ошибку в чате
        addSystemMessage(`Ошибка подключения: ${error.message}`)
      }
    }

    // Переподключение
    const reconnect = async () => {
      console.log('🔄 Ручное переподключение...')
      chatService.disconnect()
      await connectWebSocket()
    }

    // Отключение от WebSocket
    const disconnectWebSocket = () => {
      console.log('🔌 Отключение WebSocket...')
      chatService.disconnect()
    }

    // Обработка входящих сообщений
    const onMessageReceived = (message) => {
      console.log('📨 Обработка сообщения:', message)
      messages.value.push(message)
      
      // Если чат свернут и это не системное сообщение - увеличиваем счетчик
      if (!isExpanded.value && 
          message.type !== 'system' && 
          !message.action &&
          message.user_id !== currentUser.value?.id) {
        unreadCount.value++
      }
      
      // Автопрокрутка к новым сообщениям
      scrollToBottom()
    }

    // Добавление системного сообщения
    const addSystemMessage = (text) => {
      const systemMessage = {
        type: 'system',
        message: text,
        timestamp: new Date().toISOString(),
        id: Date.now()
      }
      messages.value.push(systemMessage)
      scrollToBottom()
    }

    // Обработка изменения статуса соединения
    const onConnectionStatusChange = (connected) => {
      console.log(`📡 Статус соединения изменился: ${connected ? 'подключено' : 'отключено'}`)
      
      isConnected.value = connected
      connectionStatus.value = connected ? 'connected' : 'disconnected'
      loading.value = false
      
      if (connected) {
        addSystemMessage('✅ Подключено к чату')
        
        // При переподключении загружаем историю
        loadMessageHistory()
        
        // Фокус на поле ввода
        nextTick(() => {
          if (messageInput.value) {
            messageInput.value.focus()
          }
        })
      } else {
        addSystemMessage('❌ Соединение потеряно')
      }
    }

    // Загрузка истории сообщений
    const loadMessageHistory = async () => {
      try {
        const history = await chatService.getHistory()
        messages.value = history
        scrollToBottom()
      } catch (error) {
        console.error('Ошибка загрузки истории:', error)
      }
    }

    // Отправка сообщения
    const sendMessage = async () => {
      const messageText = inputMessage.value.trim()
      
      if (!messageText || !isConnected.value || sending.value) {
        return
      }
      
      console.log('📤 Отправка сообщения:', messageText)
      sending.value = true
      
      try {
        await chatService.sendMessage(messageText)
        inputMessage.value = ''
        
        // Фокус обратно на поле ввода
        nextTick(() => {
          if (messageInput.value) {
            messageInput.value.focus()
          }
        })
      } catch (error) {
        console.error('Ошибка отправки сообщения:', error)
        addSystemMessage(`❌ Ошибка отправки: ${error.message}`)
      } finally {
        sending.value = false
      }
    }

    // Обработка изменения ввода
    const onInputChange = () => {
      // Можно добавить индикатор печати и т.д.
    }

    // Прокрутка к нижней части чата
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    // Переключение видимости чата
    const toggleChat = () => {
      isExpanded.value = !isExpanded.value
      
      if (isExpanded.value) {
        // При открытии чата сбрасываем счетчик непрочитанных
        unreadCount.value = 0
        
        // Подключаемся если еще не подключены
        if (!isConnected.value && connectionStatus.value !== 'connecting') {
          connectWebSocket()
        }
        
        // Прокручиваем к последним сообщениям
        scrollToBottom()
        
        // Фокус на поле ввода
        nextTick(() => {
          if (messageInput.value) {
            messageInput.value.focus()
          }
        })
      }
    }

    // Определение класса сообщения
    const getMessageClass = (message) => {
      if (message.type === 'system' || message.action) return 'system'
      if (message.user_id === currentUser.value?.id) return 'own'
      if (message.is_admin) return 'admin'
      if (message.is_broadcast) return 'broadcast'
      return 'other'
    }

    // Форматирование времени
    const formatTime = (timestamp) => {
      if (!timestamp) return ''
      
      try {
        const date = new Date(timestamp)
        const now = new Date()
        const diffMs = now - date
        const diffMins = Math.floor(diffMs / 60000)
        
        // Если меньше минуты назад
        if (diffMins < 1) return 'только что'
        
        // Если сегодня
        if (date.toDateString() === now.toDateString()) {
          return date.toLocaleTimeString('ru-RU', { 
            hour: '2-digit', 
            minute: '2-digit' 
          })
        }
        
        // Если вчера
        const yesterday = new Date(now)
        yesterday.setDate(yesterday.getDate() - 1)
        if (date.toDateString() === yesterday.toDateString()) {
          return 'вчера ' + date.toLocaleTimeString('ru-RU', { 
            hour: '2-digit', 
            minute: '2-digit' 
          })
        }
        
        // Иначе показываем дату
        return date.toLocaleDateString('ru-RU', {
          day: '2-digit',
          month: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (e) {
        return ''
      }
    }

    // Наблюдатель за авторизацией
    watch(() => authStore.isAuthenticated, (isAuth) => {
      console.log('👤 Статус авторизации изменился:', isAuth)
      
      if (isAuth) {
        // Если чат открыт, подключаемся
        if (isExpanded.value) {
          connectWebSocket()
        }
      } else {
        // При выходе очищаем все
        disconnectWebSocket()
        messages.value = []
        unreadCount.value = 0
        isConnected.value = false
        connectionStatus.value = 'disconnected'
      }
    })

    // Жизненный цикл
    onMounted(() => {
      console.log('🚀 ChatWidget mounted')
      
      // Если пользователь авторизован, подключаемся (чатом управляем через toggle)
      if (authStore.isAuthenticated && isExpanded.value) {
        connectWebSocket()
      } else {
        loading.value = false
      }
    })

    onUnmounted(() => {
      console.log('🗑️ ChatWidget unmounted')
      disconnectWebSocket()
    })

    return {
      isExpanded,
      isConnected,
      connectionStatus,
      connectionStatusText,
      inputMessage,
      messages,
      sending,
      loading,
      unreadCount,
      messagesContainer,
      messageInput,
      currentUser,
      toggleChat,
      sendMessage,
      reconnect,
      onInputChange,
      getMessageClass,
      formatTime
    }
  }
}
</script>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

.chat-toggle {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
  transition: all 0.3s ease;
  position: relative;
}

.chat-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.unread-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  min-width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
  padding: 0 5px;
  animation: pulse 2s infinite;
  border: 2px solid white;
  box-sizing: content-box;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.toggle-icon {
  font-size: 24px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-container {
  position: absolute;
  bottom: 70px;
  right: 0;
  width: 380px;
  height: 550px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease;
  border: 1px solid #e0e0e0;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.chat-header {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.online-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  opacity: 0.9;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
  transition: all 0.3s ease;
}

.status-dot.online {
  background: #20c997;
  box-shadow: 0 0 0 2px rgba(32, 201, 151, 0.2);
  animation: blink 2s infinite;
}

.status-dot.connecting {
  background: #ffa726;
  animation: pulse 1.5s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.reconnect-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.reconnect-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(180deg);
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
  scrollbar-width: thin;
  scrollbar-color: #ccc transparent;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}

.loading-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
  gap: 12px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #ff6b6b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner.small {
  width: 16px;
  height: 16px;
  border-width: 2px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
  text-align: center;
  padding: 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-hint {
  font-size: 13px;
  color: #888;
  margin-top: 4px;
}

.message {
  margin-bottom: 16px;
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 85%;
  animation: fadeIn 0.3s ease;
  word-wrap: break-word;
  position: relative;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 12px;
}

.message-sender {
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.admin-badge {
  background: #ffa726;
  color: white;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 10px;
  font-weight: bold;
}

.message-time {
  color: rgba(0, 0, 0, 0.5);
  font-size: 11px;
  white-space: nowrap;
}

.message-content {
  line-height: 1.4;
  font-size: 14px;
}

.message.system {
  background: #e9ecef;
  border-left: 4px solid #6c757d;
  margin: 12px auto;
  max-width: 90%;
  font-style: italic;
  color: #495057;
}

.message.own {
  background: linear-gradient(135deg, #4dabf7, #339af0);
  color: white;
  margin-left: auto;
  border-radius: 12px 12px 0 12px;
  margin-right: 0;
}

.message.own .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.message.admin {
  background: linear-gradient(135deg, #ffa726, #ff922b);
  color: white;
  border-radius: 12px 12px 12px 0;
  margin-left: 0;
  margin-right: auto;
}

.message.admin .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.message.broadcast {
  background: linear-gradient(135deg, #ff6b6b, #ff4757);
  color: white;
  text-align: center;
  max-width: 95%;
  margin: 12px auto;
  border-radius: 12px;
}

.message-broadcast {
  margin-top: 6px;
  font-size: 10px;
  opacity: 0.8;
  text-align: center;
}

.connection-event {
  margin-top: 6px;
  font-size: 11px;
  font-style: italic;
  text-align: center;
  padding: 4px;
  border-radius: 4px;
}

.connection-event.connected {
  background: rgba(32, 201, 151, 0.1);
  color: #20c997;
}

.connection-event.disconnected {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.chat-input-area {
  border-top: 1px solid #eee;
  background: white;
  padding: 16px;
}

.connection-error {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff3cd;
  color: #856404;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
  border: 1px solid #ffeaa7;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.error-icon {
  font-size: 20px;
}

.error-text {
  flex: 1;
}

.error-text p {
  margin: 0;
  font-size: 12px;
  opacity: 0.8;
}

.retry-btn {
  background: #856404;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.3s;
}

.retry-btn:hover {
  background: #6c5203;
}

.connection-connecting {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #e7f3ff;
  color: #0c63e4;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
  font-size: 13px;
}

.input-wrapper {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}

.message-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  outline: none;
  font-size: 14px;
  transition: all 0.3s;
  background: #f8f9fa;
}

.message-input:focus {
  border-color: #ff6b6b;
  background: white;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
}

.message-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.7;
}

.send-button {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  position: relative;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.sending-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.admin-commands {
  margin-top: 8px;
  text-align: center;
  color: #666;
  font-size: 11px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.admin-commands strong {
  color: #ff6b6b;
}

/* Адаптивность */
@media (max-width: 768px) {
  .chat-widget {
    bottom: 15px;
    right: 15px;
  }

  .chat-container {
    width: calc(100vw - 30px);
    max-width: 400px;
    height: 450px;
    bottom: 60px;
    right: 0;
  }

  .chat-toggle {
    width: 56px;
    height: 56px;
  }

  .toggle-icon {
    font-size: 22px;
  }
}

@media (max-width: 480px) {
  .chat-container {
    width: calc(100vw - 20px);
    height: 400px;
  }
  
  .chat-toggle {
    width: 52px;
    height: 52px;
  }
  
  .message {
    max-width: 90%;
  }
}
</style>