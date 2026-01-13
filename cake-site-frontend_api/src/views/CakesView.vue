<template>
  <div class="cakes">
    <h1>Каталог тортов</h1>
    
    <div class="cakes-grid">
      <div 
        v-for="cake in cakes" 
        :key="cake.id" 
        class="cake-card"
      >
        <div class="cake-image" @click="$router.push(`/cakes/${cake.id}`)">
          <img v-if="cake.image_url" :src="cake.image_url" :alt="cake.name">
          <div v-else class="cake-placeholder">🎂</div>
        </div>
        <div class="cake-info">
          <h3 @click="$router.push(`/cakes/${cake.id}`)" class="cake-title">{{ cake.name }}</h3>
          <p class="cake-description">{{ cake.description }}</p>
          <div class="cake-details">
            <span class="cake-price">{{ cake.price }} ₽</span>
            <span class="cake-weight">{{ cake.weight }} г</span>
          </div>
          <button class="btn btn-primary" @click.stop="openOrderModal(cake)">
            Заказать
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для быстрого заказа -->
    <div v-if="showOrderModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h2>Заказ торта "{{ selectedCake?.name }}"</h2>
          <button @click="showOrderModal = false" class="close-btn">×</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>Количество:</label>
            <input 
              v-model.number="quantity" 
              type="number" 
              min="1" 
              class="form-input"
              @keypress="preventMinus"
            >
          </div>
          
          <div class="form-group">
            <label>Способ получения:</label>
            <select v-model="deliveryType" class="form-input">
              <option value="pickup">Самовывоз</option>
              <option value="delivery">Доставка</option>
            </select>
          </div>

          <div v-if="deliveryType === 'delivery'" class="delivery-details">
            <div class="form-group">
              <label>Адрес доставки:</label>
              <input 
                v-model="deliveryAddress"
                type="text" 
                class="form-input"
                placeholder="Введите адрес доставки"
                required
              >
            </div>
            <div class="form-group">
              <label>Дата доставки:</label>
              <input 
                v-model="deliveryDate"
                type="datetime-local" 
                class="form-input"
              >
            </div>
          </div>

          <div class="form-group">
            <label>Примечания:</label>
            <textarea 
              v-model="customerNotes"
              class="form-input"
              placeholder="Особые пожелания к заказу"
              rows="2"
            ></textarea>
          </div>

          <div class="price-summary">
            <strong>Итого: {{ (selectedCake?.price || 0) * quantity }} ₽</strong>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showOrderModal = false" class="btn btn-secondary">
            Отмена
          </button>
          <button 
            @click="addToOrder" 
            class="btn btn-primary"
            :disabled="addingToOrder || (deliveryType === 'delivery' && !deliveryAddress)"
          >
            {{ addingToOrder ? 'Оформление...' : 'Оформить заказ' }}
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
  name: 'CakesView',
  data() {
    return {
      cakes: [],
      showOrderModal: false,
      selectedCake: null,
      quantity: 1,
      deliveryType: 'pickup',
      deliveryAddress: '',
      deliveryDate: '',
      customerNotes: '',
      addingToOrder: false
    }
  },
  async mounted() {
    await this.loadCakes()
  },
  methods: {
    async loadCakes() {
      try {
        const response = await cakesService.getAll()
        this.cakes = response.data
      } catch (error) {
        console.error('Ошибка загрузки тортов:', error)
      }
    },
    
    openOrderModal(cake) {
      const authStore = useAuthStore()
      
      // Проверяем авторизацию
      if (!authStore.isAuthenticated) {
        if (confirm('Для заказа необходимо войти в систему. Перейти на страницу входа?')) {
          this.$router.push('/login')
        }
        return
      }
      
      this.selectedCake = cake
      this.quantity = 1
      this.deliveryType = 'pickup'
      this.deliveryAddress = ''
      this.deliveryDate = ''
      this.customerNotes = ''
      this.addingToOrder = false
      this.showOrderModal = true
    },
    
    preventMinus(e) {
      if (e.key === '-' || e.key === 'e' || e.key === 'E') {
        e.preventDefault()
      }
    },
    
    async addToOrder() {
      if (!this.selectedCake) return
      
      // Проверяем обязательные поля для доставки
      if (this.deliveryType === 'delivery' && !this.deliveryAddress.trim()) {
        alert('Пожалуйста, укажите адрес доставки')
        return
      }
      
      this.addingToOrder = true
      try {
        const orderData = {
          cake_id: this.selectedCake.id,
          quantity: this.quantity,
          delivery_type: this.deliveryType,
          delivery_address: this.deliveryType === 'delivery' ? this.deliveryAddress : null,
          delivery_date: this.deliveryDate || null,
          customer_notes: this.customerNotes || `Заказ торта "${this.selectedCake.name}"`
        }
        
        const response = await ordersService.create(orderData)
        alert(`Заказ успешно создан! Номер заказа: ${response.data.id}`)
        this.showOrderModal = false
        
        // Сбрасываем поля
        this.selectedCake = null
        this.quantity = 1
        this.deliveryAddress = ''
        this.deliveryDate = ''
        this.customerNotes = ''
        
        // Предлагаем перейти к заказам
        if (confirm('Хотите перейти к списку ваших заказов?')) {
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
.cakes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.cake-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.cake-card:hover {
  transform: translateY(-5px);
}

.cake-image {
  height: 200px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.cake-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cake-placeholder {
  font-size: 4rem;
}

.cake-info {
  padding: 1.5rem;
}

.cake-title {
  margin-bottom: 0.5rem;
  color: #333;
  cursor: pointer;
  transition: color 0.2s;
}

.cake-title:hover {
  color: #ff6b6b;
}

.cake-description {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  line-height: 1.4;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cake-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.cake-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ff6b6b;
}

.cake-weight {
  color: #666;
  font-size: 0.9rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #ff5252;
}

/* Стили для модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
  border-radius: 10px 10px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #666;
  line-height: 1;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  background: #eee;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #eee;
  justify-content: flex-end;
  background: #f8f9fa;
  border-radius: 0 0 10px 10px;
}

.delivery-details {
  margin: 1rem 0;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 5px;
  border: 1px solid #eee;
}

.price-summary {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #e7f3ff;
  border-radius: 5px;
  text-align: center;
  font-size: 1.2rem;
  border: 1px solid #c5e1ff;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #ff6b6b;
  box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.1);
}

textarea.form-input {
  resize: vertical;
  min-height: 60px;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary {
  background: #ff6b6b;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #ff5252;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>