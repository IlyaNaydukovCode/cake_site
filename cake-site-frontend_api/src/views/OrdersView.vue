<template>
  <div class="orders">
    <h1>Мои заказы</h1>
    
    <div v-if="loading" class="loading">Загрузка заказов...</div>
    
    <div v-else-if="orders.length === 0" class="no-orders">
      <p>У вас пока нет заказов</p>
      <router-link to="/cakes" class="btn btn-primary">
        Перейти к каталогу
      </router-link>
    </div>

    <div v-else class="orders-list">
      <div 
        v-for="order in orders" 
        :key="order.id" 
        class="order-card"
      >
        <div class="order-header">
          <h3>Заказ #{{ order.id }}</h3>
          <span :class="['status', order.status]">
            {{ getStatusText(order.status) }}
          </span>
        </div>
        
        <div class="order-details">
          <div class="order-info">
            <p><strong>Дата:</strong> {{ formatDate(order.order_date) }}</p>
            <p><strong>Сумма:</strong> {{ order.total_amount }} ₽</p>
            <p><strong>Способ получения:</strong> {{ getDeliveryText(order.delivery_type) }}</p>
            <p v-if="order.delivery_address">
              <strong>Адрес доставки:</strong> {{ order.delivery_address }}
            </p>
          </div>
          
          <div class="order-items">
            <div v-if="order.cake" class="order-item">
              <strong>Готовый торт:</strong> {{ order.cake.name }}
              <span>({{ order.quantity }} шт.)</span>
            </div>
            <div v-if="order.custom_cake" class="order-item">
              <strong>Кастомный торт:</strong> {{ order.custom_cake.name }}
              <span>({{ order.quantity }} шт.)</span>
            </div>
          </div>
        </div>

        <div class="order-actions">
          <button 
            v-if="order.status === 'pending'"
            @click="payOrder(order.id)"
            class="btn btn-primary"
          >
            Оплатить
          </button>
          <button 
            v-if="['pending', 'confirmed'].includes(order.status)"
            @click="cancelOrder(order.id)"
            class="btn btn-secondary"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ordersService } from '../services/api'

export default {
  name: 'OrdersView',
  data() {
    return {
      orders: [],
      loading: true
    }
  },
  async mounted() {
    await this.loadOrders()
  },
  methods: {
    async loadOrders() {
      try {
        const response = await ordersService.getMyOrders()
        this.orders = response.data
      } catch (error) {
        console.error('Ошибка загрузки заказов:', error)
      } finally {
        this.loading = false
      }
    },

    getStatusText(status) {
      const statusMap = {
        'pending': 'Ожидает оплаты',
        'confirmed': 'Подтвержден',
        'in_progress': 'В процессе',
        'ready': 'Готов',
        'delivered': 'Доставлен',
        'cancelled': 'Отменен'
      }
      return statusMap[status] || status
    },

    getDeliveryText(deliveryType) {
      return deliveryType === 'delivery' ? 'Доставка' : 'Самовывоз'
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    async payOrder(orderId) {
      try {
        const paymentData = {
          payment_method: 'card',
          amount: this.orders.find(o => o.id === orderId).total_amount
        }
        await ordersService.pay(orderId, paymentData)
        alert('Заказ оплачен!')
        await this.loadOrders() // Обновляем список
      } catch (error) {
        alert('Ошибка оплаты: ' + error.response?.data?.detail)
      }
    },

    async cancelOrder(orderId) {
      if (confirm('Вы уверены, что хотите отменить заказ?')) {
        try {
          const orders = this.orders.map(order => {
            if (order.id === orderId) {
              return { ...order, status: 'cancelled' }
            }
            return order
          })
          
          // Сохраняем в localStorage
          localStorage.setItem('orders', JSON.stringify(orders))
          this.orders = orders
          alert('Заказ отменен')
        } catch (error) {
          alert('Ошибка отмены заказа')
        }
      }
    }
  }
}
</script>

<style scoped>
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
}

.order-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status.pending {
  background: #fff3cd;
  color: #856404;
}

.status.confirmed {
  background: #d1ecf1;
  color: #0c5460;
}

.status.in_progress {
  background: #d1ecf1;
  color: #0c5460;
}

.status.ready {
  background: #d4edda;
  color: #155724;
}

.status.delivered {
  background: #d4edda;
  color: #155724;
}

.status.cancelled {
  background: #f8d7da;
  color: #721c24;
}

.order-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 1rem;
}

.order-info p {
  margin-bottom: 0.5rem;
}

.order-items {
  border-left: 2px solid #eee;
  padding-left: 1rem;
}

.order-item {
  margin-bottom: 0.5rem;
}

.order-actions {
  display: flex;
  gap: 1rem;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.no-orders {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.no-orders p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}
</style>