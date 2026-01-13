<template>
  <div class="modal-overlay">
    <div class="modal wide-modal">
      <div class="modal-header">
        <h2>Детали заказа #{{ order.id }}</h2>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>
      
      <div class="modal-body">
        <div v-if="order" class="order-details">
          <!-- Основная информация -->
          <div class="detail-section">
            <h3>Основная информация</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <strong>Статус:</strong>
                <span :class="['status-badge', order.status]">
                  {{ getStatusText(order.status) }}
                </span>
              </div>
              <div class="detail-item">
                <strong>Дата заказа:</strong>
                {{ formatDate(order.order_date) }}
              </div>
              <div class="detail-item">
                <strong>Сумма:</strong>
                {{ order.total_amount }} ₽
              </div>
              <div class="detail-item">
                <strong>Количество:</strong>
                {{ order.quantity }} шт.
              </div>
              <div class="detail-item">
                <strong>Способ получения:</strong>
                {{ order.delivery_type === 'delivery' ? 'Доставка' : 'Самовывоз' }}
              </div>
              <div v-if="order.delivery_address" class="detail-item">
                <strong>Адрес доставки:</strong>
                {{ order.delivery_address }}
              </div>
              <div v-if="order.delivery_date" class="detail-item">
                <strong>Дата доставки:</strong>
                {{ formatDateTime(order.delivery_date) }}
              </div>
              <div v-if="order.customer_notes" class="detail-item full-width">
                <strong>Примечания клиента:</strong>
                {{ order.customer_notes }}
              </div>
            </div>
          </div>

          <!-- Информация о торте -->
          <div v-if="order.cake" class="detail-section">
            <h3>Готовый торт</h3>
            <div class="cake-info">
              <div class="cake-image" v-if="order.cake.image_url">
                <img :src="order.cake.image_url" :alt="order.cake.name">
              </div>
              <div class="cake-details">
                <h4>{{ order.cake.name }}</h4>
                <p>{{ order.cake.description }}</p>
                <div class="cake-specs">
                  <span>Цена: {{ order.cake.price }} ₽</span>
                  <span>Вес: {{ order.cake.weight }} г</span>
                </div>
                <div v-if="order.cake.ingredients" class="ingredients">
                  <strong>Ингредиенты:</strong> {{ order.cake.ingredients }}
                </div>
              </div>
            </div>
          </div>

          <div v-if="order.custom_cake" class="detail-section">
            <h3>Кастомный торт</h3>
            <div class="custom-cake-info">
              <h4>{{ order.custom_cake.name }}</h4>
              <p v-if="order.custom_cake.description">{{ order.custom_cake.description }}</p>
              <div class="cake-specs">
                <span>Итоговая цена: {{ order.custom_cake.total_price }} ₽</span>
              </div>
              
              <!-- Компоненты кастомного торта -->
              <div v-if="order.custom_cake.cake_layers" class="components">
                <h5>Коржи:</h5>
                <ul>
                  <li v-for="layer in order.custom_cake.cake_layers" :key="layer.id">
                    {{ layer.name }} ({{ layer.quantity }} шт.)
                  </li>
                </ul>
              </div>
              
              <div v-if="order.custom_cake.cream" class="components">
                <h5>Кремы:</h5>
                <ul>
                  <li v-for="cream in order.custom_cake.cream" :key="cream.id">
                    {{ cream.name }} ({{ cream.quantity }} шт.)
                  </li>
                </ul>
              </div>
              
              <div v-if="order.custom_cake.filling" class="components">
                <h5>Начинки:</h5>
                <ul>
                  <li v-for="filling in order.custom_cake.filling" :key="filling.id">
                    {{ filling.name }} ({{ filling.quantity }} шт.)
                  </li>
                </ul>
              </div>
              
              <div v-if="order.custom_cake.decorations" class="components">
                <h5>Украшения:</h5>
                <ul>
                  <li v-for="decoration in order.custom_cake.decorations" :key="decoration.id">
                    {{ decoration.name }} ({{ decoration.quantity }} шт.)
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Информация о пользователе -->
          <div class="detail-section">
            <h3>Информация о пользователе</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <strong>ID пользователя:</strong>
                {{ order.user_id }}
              </div>
              <!-- Можно добавить больше информации о пользователе, если доступна -->
            </div>
          </div>
        </div>
        
        <div v-else class="loading">
          Загрузка информации...
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="$emit('close')" class="btn btn-primary">
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderDetailsModal',
  props: {
    order: {
      type: Object,
      default: null
    }
  },
  methods: {
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
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU')
    },
    
    formatDateTime(dateTimeString) {
      return new Date(dateTimeString).toLocaleString('ru-RU')
    }
  }
}
</script>

<style scoped>
.wide-modal {
  max-width: 800px;
}

.order-details {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.detail-section {
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.detail-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #eee;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.cake-info {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.5rem;
  align-items: start;
}

.cake-image {
  width: 200px;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
}

.cake-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cake-details h4 {
  margin-top: 0;
  color: #333;
}

.cake-specs {
  display: flex;
  gap: 1rem;
  margin: 0.5rem 0;
}

.ingredients {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.custom-cake-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.components {
  margin-top: 0.5rem;
}

.components h5 {
  margin-bottom: 0.5rem;
  color: #555;
}

.components ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #666;
}

.components li {
  margin-bottom: 0.25rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
  display: inline-block;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.confirmed {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.in_progress {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.ready {
  background: #d4edda;
  color: #155724;
}

.status-badge.delivered {
  background: #d4edda;
  color: #155724;
}

.status-badge.cancelled {
  background: #f8d7da;
  color: #721c24;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>