<template>
  <div class="profile">
    <h1>Личный кабинет</h1>
    
    <div class="profile-content">
      <div class="profile-card">
        <h2>Мои данные</h2>
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label class="form-label">Email</label>
            <input 
              v-model="form.email"
              type="email" 
              class="form-input"
              disabled
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Полное имя</label>
            <input 
              v-model="form.full_name"
              type="text" 
              class="form-input"
              required
            >
          </div>

          <div class="form-group">
            <label class="form-label">Телефон</label>
            <input 
              v-model="form.phone"
              type="tel" 
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label class="form-label">Адрес доставки</label>
            <textarea 
              v-model="form.address"
              class="form-input"
              rows="3"
            ></textarea>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
          </button>
        </form>
      </div>

      <div class="stats-card">
        <h2>Статистика</h2>
        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">Всего заказов:</span>
            <span class="stat-value">{{ ordersCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Активных заказов:</span>
            <span class="stat-value">{{ activeOrdersCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Зарегистрирован:</span>
            <span class="stat-value">{{ formatDate(userInfo.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { userService, ordersService } from '../services/api'

export default {
  name: 'ProfileView',
  data() {
    return {
      form: {
        email: '',
        full_name: '',
        phone: '',
        address: ''
      },
      ordersCount: 0,
      activeOrdersCount: 0,
      loading: false
    }
  },
  computed: {
    userInfo() {
      const authStore = useAuthStore()
      return authStore.userInfo
    }
  },
  async mounted() {
    await this.loadUserData()
    await this.loadOrdersStats()
  },
  methods: {
    async loadUserData() {
      const authStore = useAuthStore()
      if (!authStore.user) {
        await authStore.fetchUser()
      }
      
      if (authStore.user) {
        this.form = {
          email: authStore.user.email,
          full_name: authStore.user.full_name,
          phone: authStore.user.phone || '',
          address: authStore.user.address || ''
        }
      }
    },

    async loadOrdersStats() {
      try {
        const response = await ordersService.getMyOrders()
        const orders = response.data
        this.ordersCount = orders.length
        this.activeOrdersCount = orders.filter(order => 
          !['delivered', 'cancelled'].includes(order.status)
        ).length
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    async updateProfile() {
      this.loading = true
      try {
        const updateData = {
          full_name: this.form.full_name,
          phone: this.form.phone,
          address: this.form.address
        }
        
        await userService.updateProfile(updateData)
        const authStore = useAuthStore()
        await authStore.fetchUser()
        alert('Данные успешно обновлены!')
      } catch (error) {
        alert('Ошибка обновления: ' + error.response?.data?.detail)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.profile-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.profile-card,
.stats-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.profile-card h2,
.stats-card h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

.stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 5px;
}

.stat-label {
  color: #666;
}

.stat-value {
  font-weight: bold;
  color: #ff6b6b;
}

.form-input:disabled {
  background: #f5f5f5;
  color: #666;
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}
</style>