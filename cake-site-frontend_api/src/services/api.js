import axios from 'axios'
import { useAuthStore } from '../stores/auth'


const API_URL = 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})


apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()
    
    if (error.response?.status === 401 && !originalRequest._retry && authStore.refreshToken) {
      originalRequest._retry = true
      
      try {
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: authStore.refreshToken
        })
        
        const { access_token, refresh_token } = response.data
        authStore.token = access_token
        authStore.refreshToken = refresh_token
        localStorage.setItem('token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return apiClient(originalRequest)
      } catch (refreshError) {

        authStore.logout()
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export const authService = {
  login: async (credentials) => {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    
    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response
  },

  register: async (userData) => {
    return await apiClient.post('/auth/register', userData)
  },

  refreshToken: async (refreshToken) => {
    return await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken
    })
  },

  getMe: async () => {
    return await apiClient.get('/users/')
  }
}

export const cakesService = {
  getAll: async () => {
    return await apiClient.get('/cakes/')
  },

  getById: async (id) => {
    return await apiClient.get(`/cakes/${id}`)
  },

  getComponents: async () => {
    return await apiClient.get('/cakes/components/all')
  }
}

export const constructorService = {
  createCustomCake: async (cakeData) => {
    const formattedData = {
      name: cakeData.name || 'Мой кастомный торт',
      layers: cakeData.layers || [],
      creams: cakeData.creams || [],
      fillings: cakeData.fillings || [],
      decorations: cakeData.decorations || []
    }
    return await apiClient.post('/constructor/create', formattedData)
  },

  calculatePrice: async (cakeData) => {
    const formattedData = {
      layers: cakeData.layers || [],
      cream_id: cakeData.creams || [],
      fillings: cakeData.fillings || [],
      decorations: cakeData.decorations || []
    }
    return await apiClient.post('/constructor/calculate-price', formattedData)
  }
}

export const ordersService = {
  create: async (orderData) => {
    return await apiClient.post('/orders/', orderData)
  },

  getMyOrders: async () => {
    return await apiClient.get('/orders/my-orders')
  },

  pay: async (orderId, paymentData) => {
    return await apiClient.post(`/orders/${orderId}/pay`, paymentData)
  }
}

export const userService = {
  updateProfile: async (userData) => {
    return await apiClient.put('/users/', userData)
  }
}


// Добавляем после существующих сервисов

export const adminService = {
  // Управление пользователями
  getAllUsers: async () => {
    return await apiClient.get('/admin/users')
  },

  makeAdmin: async (userId, isAdmin) => {
    return await apiClient.post(`/admin/users/${userId}/make-admin`, {
      is_admin: isAdmin
    })
  },

  // Управление тортами
  getAllCakesAdmin: async () => {
    return await apiClient.get('/admin/cakes')
  },

  createCakeFormData: async (formData) => {
    return await apiClient.post('/admin/cakes/formdata', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  updateCakeFormData: async (cakeId, formData) => {
    return await apiClient.put(`/admin/cakes/${cakeId}/formdata`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  createCake: async (cakeData) => {
    return await apiClient.post('/admin/cakes', cakeData)
  },

  updateCake: async (cakeId, cakeData) => {
    return await apiClient.put(`/admin/cakes/${cakeId}`, cakeData)
  },

  deleteCake: async (cakeId) => {
    return await apiClient.delete(`/admin/cakes/${cakeId}`)
  },

  // Управление коржами
  getAllLayersAdmin: async () => {
    return await apiClient.get('/admin/cake-layers')
  },

  createLayer: async (layerData) => {
    return await apiClient.post('/admin/cake-layers', layerData)
  },

  updateLayer: async (layerId, layerData) => {
    return await apiClient.put(`/admin/cake-layers/${layerId}`, layerData)
  },

  deleteLayer: async (layerId) => {
    return await apiClient.delete(`/admin/cake-layers/${layerId}`)
  },

  // Управление кремами
  getAllCreamsAdmin: async () => {
    return await apiClient.get('/admin/creams')
  },

  createCream: async (creamData) => {
    return await apiClient.post('/admin/creams', creamData)
  },

  updateCream: async (creamId, creamData) => {
    return await apiClient.put(`/admin/creams/${creamId}`, creamData)
  },

  deleteCream: async (creamId) => {
    return await apiClient.delete(`/admin/creams/${creamId}`)
  },

  // Управление начинками
  getAllFillingsAdmin: async () => {
    return await apiClient.get('/admin/fillings')
  },

  createFilling: async (fillingData) => {
    return await apiClient.post('/admin/fillings', fillingData)
  },

  updateFilling: async (fillingId, fillingData) => {
    return await apiClient.put(`/admin/fillings/${fillingId}`, fillingData)
  },

  deleteFilling: async (fillingId) => {
    return await apiClient.delete(`/admin/fillings/${fillingId}`)
  },

  // Управление украшениями
  getAllDecorationsAdmin: async () => {
    return await apiClient.get('/admin/decorations')
  },

  createDecoration: async (decorationData) => {
    return await apiClient.post('/admin/decorations', decorationData)
  },

  updateDecoration: async (decorationId, decorationData) => {
    return await apiClient.put(`/admin/decorations/${decorationId}`, decorationData)
  },

  deleteDecoration: async (decorationId) => {
    return await apiClient.delete(`/admin/decorations/${decorationId}`)
  },

  // Управление заказами
  getAllOrdersAdmin: async (skip = 0, limit = 100) => {
    return await apiClient.get('/admin/orders', {
      params: { skip, limit }
    })
  },

  getOrderByIdAdmin: async (orderId) => {
    return await apiClient.get(`/admin/orders/${orderId}`)
  },

  updateOrderStatus: async (orderId, status) => {
    return await apiClient.put(`/admin/orders/${orderId}/status`, {
      status: status
    })
  },

  getOrderStats: async () => {
    return await apiClient.get('/admin/orders/stats')
  }
}


