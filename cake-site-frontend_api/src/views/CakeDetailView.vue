<template>
  <div class="cake-detail">
    <div v-if="loading" class="loading">Загрузка...</div>
    
    <div v-else-if="cake" class="cake-detail-content">
      <div class="cake-images">
        <img v-if="cake.image_url" :src="cake.image_url" :alt="cake.name" class="main-image">
        <div v-else class="image-placeholder">🎂</div>
      </div>
      
      <div class="cake-info">
        <h1>{{ cake.name }}</h1>
        <p class="description">{{ cake.description }}</p>
        
        <div class="details">
          <div class="detail-item">
            <strong>Цена:</strong> {{ cake.price }} ₽
          </div>
          <div class="detail-item">
            <strong>Вес:</strong> {{ cake.weight }} г
          </div>
          <div class="detail-item" v-if="cake.ingredients">
            <strong>Ингредиенты:</strong> {{ cake.ingredients }}
          </div>
        </div>

        <div class="order-section">
          <div class="quantity-selector">
            <label>Количество:</label>
            <input 
              v-model.number="quantity" 
              type="number" 
              min="1" 
              class="quantity-input"
            >
          </div>
          
          <div class="delivery-options">
            <label>Способ получения:</label>
            <select v-model="deliveryType" class="delivery-select">
              <option value="pickup">Самовывоз</option>
              <option value="delivery">Доставка</option>
            </select>
          </div>

          <button 
            @click="addToOrder" 
            class="btn btn-primary order-btn"
            :disabled="addingToOrder"
          >
            {{ addingToOrder ? 'Добавление...' : `Добавить в заказ - ${totalPrice} ₽` }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { cakesService } from '../services/api'
import { ordersService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'CakeDetailView',
  data() {
    return {
      cake: null,
      loading: true,
      quantity: 1,
      deliveryType: 'pickup',
      addingToOrder: false
    }
  },
  computed: {
    totalPrice() {
      return this.cake ? this.cake.price * this.quantity : 0
    }
  },
  async mounted() {
    await this.loadCake()
  },
  methods: {
    async loadCake() {
      try {
        const cakeId = this.$route.params.id
        const response = await cakesService.getById(cakeId)
        this.cake = response.data
      } catch (error) {
        console.error('Ошибка загрузки торта:', error)
        alert('Торт не найден')
        this.$router.push('/cakes')
      } finally {
        this.loading = false
      }
    },
    
    async addToOrder() {
      const authStore = useAuthStore()
      
      // Проверяем авторизацию
      if (!authStore.isAuthenticated) {
        if (confirm('Для заказа необходимо войти в систему. Перейти на страницу входа?')) {
          this.$router.push('/login')
        }
        return
      }
      
      this.addingToOrder = true
      try {
        const orderData = {
          cake_id: this.cake.id,
          quantity: this.quantity,
          delivery_type: this.deliveryType,
          // Опциональные поля
          customer_notes: `Заказ торта "${this.cake.name}"`,
          // Если deliveryType === 'delivery', нужно добавить адрес
          // delivery_address: this.deliveryAddress,
          // delivery_date: this.deliveryDate
        }
        
        await ordersService.create(orderData)
        alert(`Торт "${this.cake.name}" успешно добавлен в заказ!`)
        
        // Можно также перейти на страницу заказов
        if (confirm('Перейти к моим заказам?')) {
          this.$router.push('/orders')
        }
      } catch (error) {
        console.error('Ошибка создания заказа:', error)
        alert(`Ошибка: ${error.response?.data?.detail || 'Не удалось создать заказ'}`)
      } finally {
        this.addingToOrder = false
      }
    }
  }
}
</script>

<style scoped>
.cake-detail-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  max-width: 1000px;
  margin: 0 auto;
}

.cake-images {
  background: #f5f5f5;
  border-radius: 10px;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 10px;
}

.image-placeholder {
  font-size: 8rem;
  color: #ddd;
}

.cake-info h1 {
  color: #333;
  margin-bottom: 1rem;
}

.description {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.details {
  margin-bottom: 2rem;
}

.detail-item {
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.order-section {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 10px;
}

.quantity-selector,
.delivery-options {
  margin-bottom: 1rem;
}

.quantity-input,
.delivery-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-left: 1rem;
}

.quantity-input {
  width: 80px;
}

.order-btn {
  width: 100%;
  font-size: 1.1rem;
  padding: 1rem;
}

.order-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  padding: 2rem;
}
</style>