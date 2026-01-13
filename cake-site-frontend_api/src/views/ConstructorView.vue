<template>
  <div class="constructor">
    <h1>Конструктор тортов</h1>
    
    <div class="constructor-layout">
      <div class="components-section">
        <div class="tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="['tab-button', { active: activeTab === tab.id }]"
          >
            {{ tab.name }}
          </button>
        </div>
        
        <div class="tab-content">
          <!-- Коржи -->
          <div v-show="activeTab === 'layers'">
            <h3>Коржи</h3>
            <div 
              v-for="layer in components.layers" 
              :key="layer.id"
              class="component-item"
              @click="addLayer(layer)"
            >
              <div class="component-info">
                <span class="component-name">{{ layer.name }}</span>
                <span class="component-description">{{ layer.description || 'Без описания' }}</span>
              </div>
              <span class="component-price">{{ layer.price_per_unit }} ₽</span>
            </div>
          </div>
          
          <!-- Кремы -->
          <div v-show="activeTab === 'creams'">
            <h3>Кремы</h3>
            <div 
              v-for="cream in components.creams" 
              :key="cream.id"
              class="component-item"
              @click="addCream(cream)"
            >
              <div class="component-info">
                <span class="component-name">{{ cream.name }}</span>
                <span class="component-description">{{ cream.description || 'Без описания' }}</span>
              </div>
              <span class="component-price">{{ cream.price_per_unit }} ₽</span>
            </div>
          </div>
          
          <!-- Начинки -->
          <div v-show="activeTab === 'fillings'">
            <h3>Начинки</h3>
            <div 
              v-for="filling in components.fillings" 
              :key="filling.id"
              class="component-item"
              @click="addFilling(filling)"
            >
              <div class="component-info">
                <span class="component-name">{{ filling.name }}</span>
                <span class="component-description">{{ filling.description || 'Без описания' }}</span>
              </div>
              <span class="component-price">{{ filling.price_per_unit }} ₽</span>
            </div>
          </div>
          
          <!-- Украшения -->
          <div v-show="activeTab === 'decorations'">
            <h3>Украшения</h3>
            <div 
              v-for="decoration in components.decorations" 
              :key="decoration.id"
              class="component-item"
              @click="addDecoration(decoration)"
            >
              <div class="component-info">
                <span class="component-name">{{ decoration.name }}</span>
                <span class="component-description">{{ decoration.description || 'Без описания' }}</span>
              </div>
              <span class="component-price">{{ decoration.price_per_unit }} ₽</span>
            </div>
          </div>
        </div>
      </div>

      <div class="preview-section">
        <div class="cake-preview">
          <h3>Ваш торт</h3>
          <div class="preview-content">
            <div v-if="customCake.layers.length === 0 && customCake.creams.length === 0 && customCake.fillings.length === 0 && customCake.decorations.length === 0" 
                 class="empty-preview">
              Добавьте компоненты для создания торта
            </div>
            <div v-else>
              <!-- Коржи с управлением количеством -->
              <div class="preview-category">
                <h4>Коржи</h4>
                <div v-if="customCake.layers.length > 0">
                  <div 
                    v-for="(layer, index) in customCake.layers" 
                    :key="index"
                    class="preview-item"
                  >
                    <div class="preview-item-info">
                      <span class="preview-item-name">{{ layer.name }}</span>
                    </div>
                    <div class="quantity-controls">
                      <button 
                        @click.stop="decreaseLayerQuantity(layer.id)"
                        class="quantity-btn"
                        :disabled="layer.quantity <= 1"
                      >-</button>
                      <span class="quantity-value">{{ layer.quantity }}</span>
                      <button 
                        @click.stop="increaseLayerQuantity(layer.id)"
                        class="quantity-btn"
                      >+</button>
                      <button 
                        @click.stop="removeLayer(layer.id)"
                        class="remove-btn"
                        title="Удалить"
                      >×</button>
                    </div>
                  </div>
                </div>
                <div v-else class="no-items">
                  Коржи не добавлены
                </div>
              </div>
              
              <!-- Кремы с управлением количеством -->
              <div class="preview-category">
                <h4>Кремы</h4>
                <div v-if="customCake.creams.length > 0">
                  <div 
                    v-for="(cream, index) in customCake.creams" 
                    :key="index"
                    class="preview-item"
                  >
                    <div class="preview-item-info">
                      <span class="preview-item-name">{{ cream.name }}</span>
                    </div>
                    <div class="quantity-controls">
                      <button 
                        @click.stop="decreaseCreamQuantity(cream.id)"
                        class="quantity-btn"
                        :disabled="cream.quantity <= 1"
                      >-</button>
                      <span class="quantity-value">{{ cream.quantity }}</span>
                      <button 
                        @click.stop="increaseCreamQuantity(cream.id)"
                        class="quantity-btn"
                      >+</button>
                      <button 
                        @click.stop="removeCream(cream.id)"
                        class="remove-btn"
                        title="Удалить"
                      >×</button>
                    </div>
                  </div>
                </div>
                <div v-else class="no-items">
                  Кремы не добавлены
                </div>
              </div>
              
              <!-- Начинки с управлением количеством -->
              <div class="preview-category">
                <h4>Начинки</h4>
                <div v-if="customCake.fillings.length > 0">
                  <div 
                    v-for="(filling, index) in customCake.fillings" 
                    :key="index"
                    class="preview-item"
                  >
                    <div class="preview-item-info">
                      <span class="preview-item-name">{{ filling.name }}</span>
                    </div>
                    <div class="quantity-controls">
                      <button 
                        @click.stop="decreaseFillingQuantity(filling.id)"
                        class="quantity-btn"
                        :disabled="filling.quantity <= 1"
                      >-</button>
                      <span class="quantity-value">{{ filling.quantity }}</span>
                      <button 
                        @click.stop="increaseFillingQuantity(filling.id)"
                        class="quantity-btn"
                      >+</button>
                      <button 
                        @click.stop="removeFilling(filling.id)"
                        class="remove-btn"
                        title="Удалить"
                      >×</button>
                    </div>
                  </div>
                </div>
                <div v-else class="no-items">
                  Начинки не добавлены
                </div>
              </div>
              
              <!-- Украшения с управлением количеством -->
              <div class="preview-category">
                <h4>Украшения</h4>
                <div v-if="customCake.decorations.length > 0">
                  <div 
                    v-for="(decoration, index) in customCake.decorations" 
                    :key="index"
                    class="preview-item"
                  >
                    <div class="preview-item-info">
                      <span class="preview-item-name">{{ decoration.name }}</span>
                    </div>
                    <div class="quantity-controls">
                      <button 
                        @click.stop="decreaseDecorationQuantity(decoration.id)"
                        class="quantity-btn"
                        :disabled="decoration.quantity <= 1"
                      >-</button>
                      <span class="quantity-value">{{ decoration.quantity }}</span>
                      <button 
                        @click.stop="increaseDecorationQuantity(decoration.id)"
                        class="quantity-btn"
                      >+</button>
                      <button 
                        @click.stop="removeDecoration(decoration.id)"
                        class="remove-btn"
                        title="Удалить"
                      >×</button>
                    </div>
                  </div>
                </div>
                <div v-else class="no-items">
                  Украшения не добавлены
                </div>
              </div>
            </div>
          </div>
          
          <div class="price-calculation">
            Стоимость:
            <div class="price-item" v-if="calculatedPrice">
              <strong>Итого: {{ calculatedPrice.total_price }} ₽</strong>
            </div>
            <div class="price-item" v-if="calculatedPrice">
              Вес: {{ calculatedPrice.weight }} г
            </div>
            <div class="price-item" v-else>
              Добавьте коржи и крем для расчета стоимости
            </div>
          </div>

          <button 
            @click="openOrderModal" 
            class="btn btn-primary"
            :disabled="!canCreateCake"
          >
            Заказать торт
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для оформления заказа -->
    <div v-if="showOrderModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h2>Оформление заказа</h2>
          <button @click="showOrderModal = false" class="close-btn">×</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>Название торта:</label>
            <input 
              v-model="customCake.name"
              type="text" 
              class="form-input"
              placeholder="Введите название торта"
            >
          </div>
          
          <div class="form-group">
            <label>Количество:</label>
            <input 
              v-model.number="orderQuantity" 
              type="number" 
              min="1" 
              class="form-input"
            >
          </div>
          
          <div class="form-group">
            <label>Способ получения:</label>
            <select v-model="orderDeliveryType" class="form-input">
              <option value="pickup">Самовывоз</option>
              <option value="delivery">Доставка</option>
            </select>
          </div>

          <div v-if="orderDeliveryType === 'delivery'" class="delivery-details">
            <div class="form-group">
              <label>Адрес доставки:</label>
              <input 
                v-model="orderDeliveryAddress"
                type="text" 
                class="form-input"
                placeholder="Введите адрес доставки"
                required
              >
            </div>
            <div class="form-group">
              <label>Дата доставки:</label>
              <input 
                v-model="orderDeliveryDate"
                type="datetime-local" 
                class="form-input"
              >
            </div>
          </div>

          <div class="form-group">
            <label>Примечания:</label>
            <textarea 
              v-model="orderNotes"
              class="form-input"
              placeholder="Особые пожелания к заказу"
              rows="3"
            ></textarea>
          </div>

          <div class="price-summary">
            <div class="price-item">
              <strong>Стоимость за 1 торт: {{ calculatedPrice?.total_price || 0 }} ₽</strong>
            </div>
            <div class="price-item">
              <strong>Итого за {{ orderQuantity }} шт.: {{ (calculatedPrice?.total_price || 0) * orderQuantity }} ₽</strong>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showOrderModal = false" class="btn btn-secondary">
            Отмена
          </button>
          <button 
            @click="createOrder" 
            class="btn btn-primary"
            :disabled="creatingOrder || (orderDeliveryType === 'delivery' && !orderDeliveryAddress)"
          >
            {{ creatingOrder ? 'Создание заказа...' : 'Создать заказ' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { cakesService, constructorService, ordersService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'ConstructorView',
  data() {
    return {
      tabs: [
        { id: 'layers', name: 'Коржи' },
        { id: 'creams', name: 'Кремы' },
        { id: 'fillings', name: 'Начинки' },
        { id: 'decorations', name: 'Украшения' }
      ],
      activeTab: 'layers',
      components: {
        layers: [],
        creams: [],
        fillings: [],
        decorations: []
      },
      customCake: {
        name: 'Мой кастомный торт',
        layers: [],
        creams: [],      // Теперь это массив, а не selectedCream
        fillings: [],
        decorations: []
      },
      calculatedPrice: null,
      
      // Данные для заказа
      showOrderModal: false,
      orderQuantity: 1,
      orderDeliveryType: 'pickup',
      orderDeliveryAddress: '',
      orderDeliveryDate: '',
      orderNotes: '',
      creatingOrder: false
    }
  },
  computed: {
    canCreateCake() {
      return this.customCake.layers.length > 0 && this.customCake.creams.length > 0
    }
  },
  async mounted() {
    await this.loadComponents()
  },
  methods: {
    async loadComponents() {
      try {
        const response = await cakesService.getComponents()
        this.components = response.data
      } catch (error) {
        console.error('Ошибка загрузки компонентов:', error)
      }
    },

    // Методы для коржей
    addLayer(layer) {
      const existingLayer = this.customCake.layers.find(l => l.id === layer.id)
      if (existingLayer) {
        existingLayer.quantity++
      } else {
        this.customCake.layers.push({
          id: layer.id,
          name: layer.name,
          quantity: 1
        })
      }
      this.calculatePrice()
    },
    
    increaseLayerQuantity(layerId) {
      const layer = this.customCake.layers.find(l => l.id === layerId)
      if (layer) {
        layer.quantity++
        this.calculatePrice()
      }
    },
    
    decreaseLayerQuantity(layerId) {
      const layer = this.customCake.layers.find(l => l.id === layerId)
      if (layer && layer.quantity > 1) {
        layer.quantity--
        this.calculatePrice()
      }
    },
    
    removeLayer(layerId) {
      this.customCake.layers = this.customCake.layers.filter(l => l.id !== layerId)
      this.calculatePrice()
    },

    // Методы для кремов
    addCream(cream) {
      const existingCream = this.customCake.creams.find(c => c.id === cream.id)
      if (existingCream) {
        existingCream.quantity++
      } else {
        this.customCake.creams.push({
          id: cream.id,
          name: cream.name,
          quantity: 1
        })
      }
      this.calculatePrice()
    },
    
    increaseCreamQuantity(creamId) {
      const cream = this.customCake.creams.find(c => c.id === creamId)
      if (cream) {
        cream.quantity++
        this.calculatePrice()
      }
    },
    
    decreaseCreamQuantity(creamId) {
      const cream = this.customCake.creams.find(c => c.id === creamId)
      if (cream && cream.quantity > 1) {
        cream.quantity--
        this.calculatePrice()
      }
    },
    
    removeCream(creamId) {
      this.customCake.creams = this.customCake.creams.filter(c => c.id !== creamId)
      this.calculatePrice()
    },

    // Методы для начинок
    addFilling(filling) {
      const existingFilling = this.customCake.fillings.find(f => f.id === filling.id)
      if (existingFilling) {
        existingFilling.quantity++
      } else {
        this.customCake.fillings.push({
          id: filling.id,
          name: filling.name,
          quantity: 1
        })
      }
      this.calculatePrice()
    },
    
    increaseFillingQuantity(fillingId) {
      const filling = this.customCake.fillings.find(f => f.id === fillingId)
      if (filling) {
        filling.quantity++
        this.calculatePrice()
      }
    },
    
    decreaseFillingQuantity(fillingId) {
      const filling = this.customCake.fillings.find(f => f.id === fillingId)
      if (filling && filling.quantity > 1) {
        filling.quantity--
        this.calculatePrice()
      }
    },
    
    removeFilling(fillingId) {
      this.customCake.fillings = this.customCake.fillings.filter(f => f.id !== fillingId)
      this.calculatePrice()
    },

    // Методы для украшений
    addDecoration(decoration) {
      const existingDecoration = this.customCake.decorations.find(d => d.id === decoration.id)
      if (existingDecoration) {
        existingDecoration.quantity++
      } else {
        this.customCake.decorations.push({
          id: decoration.id,
          name: decoration.name,
          quantity: 1
        })
      }
      this.calculatePrice()
    },
    
    increaseDecorationQuantity(decorationId) {
      const decoration = this.customCake.decorations.find(d => d.id === decorationId)
      if (decoration) {
        decoration.quantity++
        this.calculatePrice()
      }
    },
    
    decreaseDecorationQuantity(decorationId) {
      const decoration = this.customCake.decorations.find(d => d.id === decorationId)
      if (decoration && decoration.quantity > 1) {
        decoration.quantity--
        this.calculatePrice()
      }
    },
    
    removeDecoration(decorationId) {
      this.customCake.decorations = this.customCake.decorations.filter(d => d.id !== decorationId)
      this.calculatePrice()
    },

    async calculatePrice() {
      if (this.customCake.layers.length === 0 || this.customCake.creams.length === 0) {
        this.calculatedPrice = null
        return
      }
      
      try {
        const cakeData = {
          name: this.customCake.name,
          layers: this.customCake.layers.map(layer => ({
            id: layer.id,
            quantity: layer.quantity
          })),
          creams: this.customCake.creams.map(cream => ({
            id: cream.id,
            quantity: cream.quantity
          })),
          fillings: this.customCake.fillings.map(filling => ({
            id: filling.id,
            quantity: filling.quantity
          })),
          decorations: this.customCake.decorations.map(decoration => ({
            id: decoration.id,
            quantity: decoration.quantity
          }))
        }
        
        const response = await constructorService.calculatePrice(cakeData)
        this.calculatedPrice = response.data
      } catch (error) {
        console.error('Ошибка расчета цены:', error)
        this.calculateMockPrice()
      }
    },

    calculateMockPrice() {
      if (this.customCake.layers.length === 0 || this.customCake.creams.length === 0) {
        this.calculatedPrice = null
        return
      }
      
      const layerPrice = this.customCake.layers.reduce((sum, layer) => {
        const component = this.components.layers.find(c => c.id === layer.id)
        return sum + (component?.price_per_unit || 300) * layer.quantity
      }, 0)
      
      const creamsPrice = this.customCake.creams.reduce((sum, cream) => {
        const component = this.components.creams.find(c => c.id === cream.id)
        return sum + (component?.price_per_unit || 200) * cream.quantity
      }, 0)
      
      const fillingsPrice = this.customCake.fillings.reduce((sum, filling) => {
        const component = this.components.fillings.find(c => c.id === filling.id)
        return sum + (component?.price_per_unit || 150) * filling.quantity
      }, 0)
      
      const decorationsPrice = this.customCake.decorations.reduce((sum, decoration) => {
        const component = this.components.decorations.find(c => c.id === decoration.id)
        return sum + (component?.price_per_unit || 120) * decoration.quantity
      }, 0)
      
      const total = layerPrice + creamsPrice + fillingsPrice + decorationsPrice
      const weight = this.customCake.layers.reduce((sum, layer) => sum + layer.quantity, 0) * 100 + 500
      
      this.calculatedPrice = {
        total_price: total,
        weight: weight
      }
    },

    openOrderModal() {
      const authStore = useAuthStore()
      
      // Проверяем авторизацию
      if (!authStore.isAuthenticated) {
        if (confirm('Для заказа необходимо войти в систему. Перейти на страницу входа?')) {
          this.$router.push('/login')
        }
        return
      }
      
      this.showOrderModal = true
    },

    async createOrder() {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        alert('Для создания заказа необходимо войти в систему')
        this.$router.push('/login')
        return
      }
      
      if (this.orderDeliveryType === 'delivery' && !this.orderDeliveryAddress.trim()) {
        alert('Пожалуйста, укажите адрес доставки')
        return
      }
      
      this.creatingOrder = true
      try {
        // 1. Сначала создаем кастомный торт
        const cakeData = {
          name: this.customCake.name || 'Мой кастомный торт',
          layers: this.customCake.layers.map(layer => ({
            id: layer.id,
            quantity: layer.quantity
          })),
          creams: this.customCake.creams.map(cream => ({
            id: cream.id,
            quantity: cream.quantity
          })),
          fillings: this.customCake.fillings.map(filling => ({
            id: filling.id,
            quantity: filling.quantity
          })),
          decorations: this.customCake.decorations.map(decoration => ({
            id: decoration.id,
            quantity: decoration.quantity
          }))
        }
        
        console.log('Создаем торт с данными:', JSON.stringify(cakeData, null, 2))
        const cakeResponse = await constructorService.createCustomCake(cakeData)
        const customCakeId = cakeResponse.data.id
        
        console.log('Торт создан, ID:', customCakeId)
        
        // 2. Создаем заказ с custom_cake_id
        const orderData = {
          custom_cake_id: customCakeId,
          quantity: this.orderQuantity,
          delivery_type: this.orderDeliveryType,
          delivery_address: this.orderDeliveryType === 'delivery' ? this.orderDeliveryAddress : null,
          delivery_date: this.orderDeliveryDate || null,
          customer_notes: this.orderNotes || `Кастомный торт: ${this.customCake.name}`
        }
        
        console.log('Создаем заказ с данными:', orderData)
        const orderResponse = await ordersService.create(orderData)
        
        alert(`Заказ успешно создан! Номер заказа: ${orderResponse.data.id}`)
        
        // Сброс формы
        this.showOrderModal = false
        this.customCake = {
          name: 'Мой кастомный торт',
          layers: [],
          creams: [],
          fillings: [],
          decorations: []
        }
        this.calculatedPrice = null
        this.orderQuantity = 1
        this.orderDeliveryType = 'pickup'
        this.orderDeliveryAddress = ''
        this.orderDeliveryDate = ''
        this.orderNotes = ''
        
        // Переход к заказам
        if (confirm('Перейти к списку ваших заказов?')) {
          this.$router.push('/orders')
        }
      } catch (error) {
        console.error('Ошибка создания заказа:', error)
        
        let errorMessage = 'Не удалось создать заказ'
        if (error.response) {
          if (error.response.data && error.response.data.detail) {
            errorMessage = error.response.data.detail
          } else if (error.response.data && typeof error.response.data === 'string') {
            errorMessage = error.response.data
          } else if (error.response.data && error.response.data.message) {
            errorMessage = error.response.data.message
          } else {
            errorMessage = `Ошибка сервера: ${error.response.status} ${error.response.statusText}`
          }
        } else if (error.request) {
          errorMessage = 'Нет ответа от сервера'
        } else {
          errorMessage = error.message
        }
        
        alert('Ошибка создания заказа: ' + errorMessage)
      } finally {
        this.creatingOrder = false
      }
    }
  }
}
</script>

<style scoped>
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
  margin: 1.5rem 0;
  padding: 1.25rem;
  background: #e7f3ff;
  border-radius: 10px;
  border-left: 4px solid #4dabf7;
}

.price-summary .price-item {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.price-summary .price-item:last-child {
  margin-bottom: 0;
  font-size: 1.2rem;
  color: #333;
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
  min-height: 80px;
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

/* Остальные стили остаются без изменений */
.constructor-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.components-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-button {
  flex: 1;
  padding: 0.75rem;
  background: #f8f9fa;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.tab-button:hover {
  background: #e9ecef;
}

.tab-button.active {
  background: #ff6b6b;
  color: white;
}

.tab-content {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  min-height: 400px;
}

.tab-content h3 {
  margin-bottom: 1rem;
  color: #ff6b6b;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.component-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin-bottom: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 4px solid transparent;
}

.component-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.component-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.component-name {
  font-weight: 500;
  color: #333;
}

.component-description {
  font-size: 0.9rem;
  color: #666;
}

.component-price {
  font-weight: 600;
  color: #ff6b6b;
  font-size: 1.1rem;
}

.preview-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  height: fit-content;
}

.cake-preview h3 {
  margin-bottom: 1.5rem;
  color: #333;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.preview-content {
  min-height: 400px;
  border: 2px dashed #ddd;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.empty-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 350px;
  color: #666;
  font-style: italic;
  font-size: 1.1rem;
}

.preview-category {
  margin-bottom: 1.5rem;
}

.preview-category h4 {
  margin-bottom: 0.75rem;
  color: #555;
  font-size: 1.1rem;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #ff6b6b;
}

.preview-item-info {
  flex: 1;
}

.preview-item-name {
  font-weight: 500;
  color: #333;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity-btn {
  width: 30px;
  height: 30px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quantity-btn:hover:not(:disabled) {
  background: #f0f0f0;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-value {
  min-width: 20px;
  text-align: center;
  font-weight: 500;
}

.remove-btn {
  width: 30px;
  height: 30px;
  border: none;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.5rem;
}

.remove-btn:hover {
  background: #ff3742;
}

.no-items {
  color: #888;
  font-style: italic;
  padding: 0.5rem;
  text-align: center;
  background: #f8f9fa;
  border-radius: 5px;
}

.price-calculation {
  margin: 1.5rem 0;
  padding: 1.25rem;
  background: #e7f3ff;
  border-radius: 10px;
  border-left: 4px solid #4dabf7;
}

.price-calculation .price-item {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.price-calculation .price-item:last-child {
  margin-bottom: 0;
}
</style>