import { defineStore } from 'pinia'
import { authService } from '../services/api'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('currentUser') || 'null'),
    token: localStorage.getItem('token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isAuthenticated: !!localStorage.getItem('token'),
    tokenExpiry: localStorage.getItem('token_expiry') || null,
    loading: false,
    error: null
  }),

  getters: {
    userInfo: (state) => state.user,
    
    // Проверяем валидность токена
    hasValidToken: (state) => {
      if (!state.token) return false
      
      try {
        // Если есть время истечения, проверяем его
        if (state.tokenExpiry) {
          const now = Date.now()
          return now < parseInt(state.tokenExpiry)
        }
        
        // Пытаемся декодировать JWT для получения exp
        const parts = state.token.split('.')
        if (parts.length === 3) {
          try {
            const payload = JSON.parse(atob(parts[1]))
            const expiry = payload.exp * 1000 // конвертируем секунды в миллисекунды
            return Date.now() < expiry
          } catch (e) {
            console.warn('Не удалось декодировать JWT:', e)
            return true // Предполагаем валидность если не можем проверить
          }
        }
        
        return true // Если токен есть, но не JWT
      } catch {
        return false
      }
    },
    
    // Для отображения в UI
    isAdmin: (state) => state.user?.is_admin || false,
    userName: (state) => state.user?.full_name || 'Пользователь',
    userEmail: (state) => state.user?.email || ''
  },

  actions: {
    async login(credentials) {
      try {
        this.loading = true
        this.error = null
        
        const response = await authService.login(credentials)
        const { access_token, refresh_token } = response.data
        
        // Сохраняем токены
        this.setTokens(access_token, refresh_token)
        
        // Загружаем данные пользователя
        await this.fetchUser()
        
        this.isAuthenticated = true
        this.loading = false
        
        return response
      } catch (error) {
        this.loading = false
        this.error = error.response?.data?.detail || 'Ошибка входа'
        throw error
      }
    },

    async register(userData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await authService.register(userData)
        this.loading = false
        
        return response
      } catch (error) {
        this.loading = false
        this.error = error.response?.data?.detail || 'Ошибка регистрации'
        throw error
      }
    },

    async fetchUser() {
      try {
        const response = await authService.getMe()
        this.user = response.data
        this.saveUserToStorage(response.data)
        return response.data
      } catch (error) {
        console.error('Ошибка загрузки пользователя:', error)
        
        // Если ошибка авторизации, пытаемся обновить токен
        if (error.response?.status === 401 && this.refreshToken) {
          try {
            await this.refreshAuthToken()
            return await this.fetchUser() // Повторяем запрос
          } catch (refreshError) {
            this.logout()
            throw error
          }
        }
        
        throw error
      }
    },

    async refreshAuthToken() {
      if (!this.refreshToken) {
        this.logout()
        throw new Error('Refresh token отсутствует')
      }
      
      try {
        const response = await authService.refreshToken(this.refreshToken)
        const { access_token, refresh_token } = response.data
        
        this.setTokens(access_token, refresh_token)
        
        return access_token
      } catch (error) {
        console.error('Ошибка обновления токена:', error)
        this.logout()
        throw error
      }
    },

    // Гарантирует валидный токен (обновляет если нужно)
    async ensureValidToken() {
      if (!this.token) {
        throw new Error('Токен отсутствует')
      }
      
      // Если токен скоро истечет (менее 5 минут) или уже невалиден
      if (!this.hasValidToken) {
        if (this.refreshToken) {
          try {
            await this.refreshAuthToken()
          } catch (error) {
            throw new Error('Не удалось обновить токен: ' + error.message)
          }
        } else {
          throw new Error('Токен невалиден и отсутствует refresh token')
        }
      }
      
      return this.token
    },

    // Установка токенов с вычислением времени истечения
    setTokens(accessToken, refreshToken) {
      this.token = accessToken
      this.refreshToken = refreshToken
      
      localStorage.setItem('token', accessToken)
      localStorage.setItem('refresh_token', refreshToken)
      
      // Пытаемся вычислить время истечения токена
      try {
        const parts = accessToken.split('.')
        if (parts.length === 3) {
          const payload = JSON.parse(atob(parts[1]))
          if (payload.exp) {
            const expiryTime = payload.exp * 1000
            this.tokenExpiry = expiryTime.toString()
            localStorage.setItem('token_expiry', expiryTime.toString())
          }
        }
      } catch (e) {
        console.warn('Не удалось установить время истечения токена:', e)
      }
    },

    // Сохранение пользователя в хранилище
    saveUserToStorage(userData) {
      this.user = userData
      localStorage.setItem('currentUser', JSON.stringify(userData))
    },

    logout() {
      // Очищаем состояние
      this.user = null
      this.token = null
      this.refreshToken = null
      this.isAuthenticated = false
      this.tokenExpiry = null
      this.error = null
      
      // Очищаем localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('currentUser')
      localStorage.removeItem('token_expiry')
      
      // Перенаправляем на главную
      if (router && router.currentRoute.value.path !== '/') {
        router.push('/')
      }
    },

    // Обновление профиля пользователя
    async updateProfile(profileData) {
      try {
        const response = await authService.updateProfile(profileData)
        if (response.data) {
          this.user = { ...this.user, ...response.data }
          this.saveUserToStorage(this.user)
        }
        return response
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка обновления профиля'
        throw error
      }
    },

    // Сброс ошибок
    clearError() {
      this.error = null
    },

    // Проверка авторизации при загрузке приложения
    async checkAuth() {
      if (!this.token) return false
      
      if (this.hasValidToken) {
        try {
          await this.fetchUser()
          return true
        } catch (error) {
          console.warn('Пользователь не авторизован:', error)
          this.logout()
          return false
        }
      } else if (this.refreshToken) {
        try {
          await this.refreshAuthToken()
          await this.fetchUser()
          return true
        } catch (error) {
          console.warn('Не удалось обновить токен:', error)
          this.logout()
          return false
        }
      } else {
        this.logout()
        return false
      }
    }
  },

  // При создании стора проверяем авторизацию
  onInit() {
    if (this.token) {
      this.checkAuth().catch(console.error)
    }
  }
})