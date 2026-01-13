<template>
  <div class="admin-dashboard">
    <h1>Административная панель</h1>
    
    <div class="admin-nav">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['nav-btn', { active: activeTab === tab.id }]"
      >
        {{ tab.name }}
      </button>
    </div>

    <div class="admin-content">
      <!-- Панель управления тортами -->
      <div v-if="activeTab === 'cakes'" class="tab-pane">
        <div class="section-header">
          <h2>Управление тортами</h2>
          <button @click="openCakeModal" class="btn btn-primary">
            + Добавить торт
          </button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Цена</th>
                <th>Вес</th>
                <th>Доступен</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cake in adminCakes" :key="cake.id">
                <td>{{ cake.id }}</td>
                <td>{{ cake.name }}</td>
                <td>{{ cake.price }} ₽</td>
                <td>{{ cake.weight }} г</td>
                <td>
                  <span :class="['status-badge', cake.is_available ? 'available' : 'unavailable']">
                    {{ cake.is_available ? 'Да' : 'Нет' }}
                  </span>
                </td>
                <td>
                  <button @click="editCake(cake)" class="btn-sm btn-edit">✏️</button>
                  <button @click="deleteCake(cake.id)" class="btn-sm btn-delete">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Панель управления компонентами -->
      <div v-if="activeTab === 'components'" class="tab-pane">
        <div class="components-tabs">
          <button 
            v-for="compTab in componentTabs" 
            :key="compTab.id"
            @click="activeComponentTab = compTab.id"
            :class="['comp-tab-btn', { active: activeComponentTab === compTab.id }]"
          >
            {{ compTab.name }}
          </button>
        </div>

        <div class="components-section">
          <!-- Коржи -->
          <div v-if="activeComponentTab === 'layers'">
            <div class="section-header">
              <h3>Коржи</h3>
              <button @click="openComponentModal('layer')" class="btn btn-primary">
                + Добавить корж
              </button>
            </div>
            <ComponentTable 
              :components="layers"
              :type="'layer'"
              @edit="editComponent"
              @delete="deleteComponent"
              @toggleAvailability="toggleComponentAvailability"
            />
          </div>

          <!-- Кремы -->
          <div v-if="activeComponentTab === 'creams'">
            <div class="section-header">
              <h3>Кремы</h3>
              <button @click="openComponentModal('cream')" class="btn btn-primary">
                + Добавить крем
              </button>
            </div>
            <ComponentTable 
              :components="creams"
              :type="'cream'"
              @edit="editComponent"
              @delete="deleteComponent"
              @toggleAvailability="toggleComponentAvailability"
            />
          </div>

          <!-- Начинки -->
          <div v-if="activeComponentTab === 'fillings'">
            <div class="section-header">
              <h3>Начинки</h3>
              <button @click="openComponentModal('filling')" class="btn btn-primary">
                + Добавить начинку
              </button>
            </div>
            <ComponentTable 
              :components="fillings"
              :type="'filling'"
              @edit="editComponent"
              @delete="deleteComponent"
              @toggleAvailability="toggleComponentAvailability"
            />
          </div>

          <!-- Украшения -->
          <div v-if="activeComponentTab === 'decorations'">
            <div class="section-header">
              <h3>Украшения</h3>
              <button @click="openComponentModal('decoration')" class="btn btn-primary">
                + Добавить украшение
              </button>
            </div>
            <ComponentTable 
              :components="decorations"
              :type="'decoration'"
              @edit="editComponent"
              @delete="deleteComponent"
              @toggleAvailability="toggleComponentAvailability"
            />
          </div>
        </div>
      </div>

      <!-- Панель управления заказами -->
      <div v-if="activeTab === 'orders'" class="tab-pane">
        <div class="section-header">
          <h2>Управление заказами</h2>
          <div class="stats">
            <div class="stat-card">
              <div class="stat-value">{{ stats.total_orders || 0 }}</div>
              <div class="stat-label">Всего заказов</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ stats.total_revenue || 0 }} ₽</div>
              <div class="stat-label">Общая выручка</div>
            </div>
          </div>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Пользователь</th>
                <th>Дата</th>
                <th>Сумма</th>
                <th>Статус</th>
                <th>Тип</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>ID: {{ order.user_id }}</td>
                <td>{{ formatDate(order.order_date) }}</td>
                <td>{{ order.total_amount }} ₽</td>
                <td>
                  <select 
                    :value="order.status" 
                    @change="updateOrderStatus(order.id, $event.target.value)"
                    class="status-select"
                  >
                    <option value="pending">Ожидает оплаты</option>
                    <option value="confirmed">Подтвержден</option>
                    <option value="in_progress">В процессе</option>
                    <option value="ready">Готов</option>
                    <option value="delivered">Доставлен</option>
                    <option value="cancelled">Отменен</option>
                  </select>
                </td>
                <td>{{ order.delivery_type === 'delivery' ? 'Доставка' : 'Самовывоз' }}</td>
                <td>
                  <button @click="viewOrderDetails(order)" class="btn-sm btn-view">👁️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Панель управления пользователями -->
      <div v-if="activeTab === 'users'" class="tab-pane">
        <div class="section-header">
          <h2>Управление пользователями</h2>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Email</th>
                <th>Имя</th>
                <th>Телефон</th>
                <th>Админ</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.full_name }}</td>
                <td>{{ user.phone || '-' }}</td>
                <td>
                  <span :class="['status-badge', user.is_admin ? 'admin' : 'user']">
                    {{ user.is_admin ? 'Да' : 'Нет' }}
                  </span>
                </td>
                <td>
                  <button 
                    @click="toggleAdmin(user.id, !user.is_admin)"
                    :class="['btn-sm', user.is_admin ? 'btn-remove-admin' : 'btn-make-admin']"
                  >
                    {{ user.is_admin ? 'Снять админа' : 'Сделать админом' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Модальное окно для торта -->
    <div v-if="showCakeModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editingCake ? 'Редактировать торт' : 'Добавить торт' }}</h3>
          <button @click="closeCakeModal" class="modal-close">×</button>
        </div>
        
        <form @submit.prevent="saveCakeForm" class="modal-form">
          <div class="form-group">
            <label>Название *</label>
            <input v-model="cakeForm.name" type="text" required>
          </div>
          
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="cakeForm.description"></textarea>
          </div>
          
          <div class="form-group">
            <label>Цена (₽) *</label>
            <input v-model="cakeForm.price" type="number" step="0.01" min="0" required>
          </div>
          
          <div class="form-group">
            <label>Вес (г)</label>
            <input v-model="cakeForm.weight" type="number" min="0">
          </div>
          
          <div class="form-group">
            <label>Ингредиенты</label>
            <textarea v-model="cakeForm.ingredients"></textarea>
          </div>
          
          <div class="form-group">
            <label>URL изображения</label>
            <input v-model="cakeForm.image_url" type="text" placeholder="https://example.com/image.jpg">
          </div>
          
          <div v-if="editingCake" class="form-group">
            <label>
              <input v-model="cakeForm.is_available" type="checkbox">
              Доступен для заказа
            </label>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeCakeModal" class="btn btn-secondary">
              Отмена
            </button>
            <button type="submit" class="btn btn-primary">
              {{ editingCake ? 'Обновить' : 'Создать' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Модальное окно для компонента -->
    <AdminComponentModal 
      v-if="showComponentModal"
      :component="editingComponent"
      :type="componentType"
      @save="saveComponent"
      @close="closeComponentModal"
    />

    <!-- Модальное окно деталей заказа -->
    <OrderDetailsModal 
      v-if="showOrderModal"
      :order="selectedOrder"
      @close="closeOrderModal"
    />
  </div>
</template>

<script>
import { adminService } from '../services/api'
import { useAuthStore } from '../stores/auth'
import AdminComponentModal from '../components/admin/AdminComponentModal.vue'
import OrderDetailsModal from '../components/admin/OrderDetailsModal.vue'
import ComponentTable from '../components/admin/ComponentTable.vue'

export default {
  name: 'AdminDashboard',
  components: {
    // УДАЛЕНО: AdminCakeModal,
    AdminComponentModal,
    OrderDetailsModal,
    ComponentTable
  },
  data() {
    return {
      tabs: [
        { id: 'cakes', name: 'Торты' },
        { id: 'components', name: 'Компоненты' },
        { id: 'orders', name: 'Заказы' },
        { id: 'users', name: 'Пользователи' }
      ],
      componentTabs: [
        { id: 'layers', name: 'Коржи' },
        { id: 'creams', name: 'Кремы' },
        { id: 'fillings', name: 'Начинки' },
        { id: 'decorations', name: 'Украшения' }
      ],
      activeTab: 'cakes',
      activeComponentTab: 'layers',
      
      // Данные
      adminCakes: [],
      layers: [],
      creams: [],
      fillings: [],
      decorations: [],
      orders: [],
      users: [],
      stats: {},
      
      // Модальные окна
      showCakeModal: false,
      showComponentModal: false,
      showOrderModal: false,
      
      editingCake: null,
      editingComponent: null,
      componentType: '',
      selectedOrder: null,
      
      loading: false,
      
      // ДОБАВЛЕНО: Данные для формы торта
      cakeForm: {
        name: '',
        description: '',
        price: 0,
        weight: null,
        ingredients: '',
        image_url: '',
        is_available: true
      },
    }
  },
  computed: {
    isAdmin() {
      const authStore = useAuthStore()
      return authStore.user?.is_admin || false
    }
  },
  async mounted() {
    await this.checkAdminAccess()
    await this.loadData()
  },
  watch: {
    activeTab(newTab) {
      if (newTab === 'cakes') this.loadCakes()
      if (newTab === 'orders') {
        this.loadOrders()
        this.loadStats()
      }
      if (newTab === 'users') this.loadUsers()
    },
    activeComponentTab(newTab) {
      this.loadComponents(newTab)
    }
  },
  methods: {
    async checkAdminAccess() {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        this.$router.push('/login')
        return
      }
      
      if (!this.isAdmin) {
        alert('У вас нет прав доступа к админ-панели')
        this.$router.push('/')
      }
    },
    
    async loadData() {
      await this.loadCakes()
      await this.loadComponents('layers')
      await this.loadStats()
    },
    
    async loadCakes() {
      try {
        const response = await adminService.getAllCakesAdmin()
        this.adminCakes = response.data
      } catch (error) {
        console.error('Ошибка загрузки тортов:', error)
      }
    },
    
    async loadComponents(type) {
      try {
        let response
        switch(type) {
          case 'layers':
            response = await adminService.getAllLayersAdmin()
            this.layers = response.data
            break
          case 'creams':
            response = await adminService.getAllCreamsAdmin()
            this.creams = response.data
            break
          case 'fillings':
            response = await adminService.getAllFillingsAdmin()
            this.fillings = response.data
            break
          case 'decorations':
            response = await adminService.getAllDecorationsAdmin()
            this.decorations = response.data
            break
        }
      } catch (error) {
        console.error(`Ошибка загрузки ${type}:`, error)
      }
    },
    
    async loadOrders() {
      try {
        const response = await adminService.getAllOrdersAdmin()
        this.orders = response.data
      } catch (error) {
        console.error('Ошибка загрузки заказов:', error)
      }
    },
    
    async loadUsers() {
      try {
        const response = await adminService.getAllUsers()
        this.users = response.data
      } catch (error) {
        console.error('Ошибка загрузки пользователей:', error)
      }
    },
    
    async loadStats() {
      try {
        const response = await adminService.getOrderStats()
        this.stats = response.data
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU')
    },
    
    // Управление тортами (ОБНОВЛЕНО)
    openCakeModal() {
      this.editingCake = null
      this.resetCakeForm()
      this.showCakeModal = true
    },
    
    editCake(cake) {
      this.editingCake = { ...cake }
      // Заполняем форму данными торта
      this.cakeForm = {
        name: cake.name,
        description: cake.description || '',
        price: cake.price,
        weight: cake.weight || null,
        ingredients: cake.ingredients || '',
        image_url: cake.image_url || '',
        is_available: cake.is_available !== undefined ? cake.is_available : true
      }
      this.cakeImageFile = null
      this.showCakeModal = true
    },
    
    resetCakeForm() {
      this.cakeForm = {
        name: '',
        description: '',
        price: 0,
        weight: null,
        ingredients: '',
        image_url: '',
        is_available: true
      }
    },
    
    async saveCakeForm() {
      try {
        const formData = new FormData()
        
        formData.append('name', this.cakeForm.name)
        formData.append('price', parseFloat(this.cakeForm.price))
        
        if (this.cakeForm.description) {
          formData.append('description', this.cakeForm.description)
        }
        
        if (this.cakeForm.weight) {
          formData.append('weight', parseFloat(this.cakeForm.weight))
        }
        
        if (this.cakeForm.ingredients) {
          formData.append('ingredients', this.cakeForm.ingredients)
        }
        
        if (this.cakeForm.image_url) {
          formData.append('image_url', this.cakeForm.image_url)
        }
        
        if (this.editingCake?.id) {
          formData.append('is_available', this.cakeForm.is_available)
        }
        
        if (this.editingCake?.id) {
          await adminService.updateCakeFormData(this.editingCake.id, formData)
        } else {
          await adminService.createCakeFormData(formData)
        }
        
        await this.loadCakes()
        this.closeCakeModal()
      } catch (error) {
        alert('Ошибка сохранения торта: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    async deleteCake(cakeId) {
      if (!confirm('Вы уверены, что хотите удалить торт?')) return
      
      try {
        await adminService.deleteCake(cakeId)
        await this.loadCakes()
      } catch (error) {
        alert('Ошибка удаления торта: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    closeCakeModal() {
      this.showCakeModal = false
      this.editingCake = null
      this.resetCakeForm()
    },
    
    // Управление компонентами (без изменений)
    openComponentModal(type) {
      this.componentType = type
      this.editingComponent = null
      this.showComponentModal = true
    },
    
    editComponent(component) {
      this.editingComponent = { ...component }
      this.showComponentModal = true
    },
    
    async saveComponent(componentData) {
      try {
        let response
        
        switch(this.componentType) {
          case 'layer':
            if (componentData.id) {
              response = await adminService.updateLayer(componentData.id, componentData)
            } else {
              response = await adminService.createLayer(componentData)
            }
            break
          case 'cream':
            if (componentData.id) {
              response = await adminService.updateCream(componentData.id, componentData)
            } else {
              response = await adminService.createCream(componentData)
            }
            break
          case 'filling':
            if (componentData.id) {
              response = await adminService.updateFilling(componentData.id, componentData)
            } else {
              response = await adminService.createFilling(componentData)
            }
            break
          case 'decoration':
            if (componentData.id) {
              response = await adminService.updateDecoration(componentData.id, componentData)
            } else {
              response = await adminService.createDecoration(componentData)
            }
            break
        }
        
        await this.loadComponents(this.activeComponentTab)
        this.closeComponentModal()
      } catch (error) {
        alert('Ошибка сохранения компонента: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    async deleteComponent(componentId) {
      if (!confirm('Вы уверены, что хотите удалить компонент?')) return
      
      try {
        switch(this.activeComponentTab) {
          case 'layers':
            await adminService.deleteLayer(componentId)
            break
          case 'creams':
            await adminService.deleteCream(componentId)
            break
          case 'fillings':
            await adminService.deleteFilling(componentId)
            break
          case 'decorations':
            await adminService.deleteDecoration(componentId)
            break
        }
        
        await this.loadComponents(this.activeComponentTab)
      } catch (error) {
        alert('Ошибка удаления компонента: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    async toggleComponentAvailability(componentId, makeAvailable) {
      try {
        const updateData = { is_available: makeAvailable }
        
        switch(this.activeComponentTab) {
          case 'layers':
            await adminService.updateLayer(componentId, updateData)
            break
          case 'creams':
            await adminService.updateCream(componentId, updateData)
            break
          case 'fillings':
            await adminService.updateFilling(componentId, updateData)
            break
          case 'decorations':
            await adminService.updateDecoration(componentId, updateData)
            break
        }
        
        // Обновляем локальное состояние
        await this.loadComponents(this.activeComponentTab)
        
      } catch (error) {
        console.error('Ошибка обновления доступности:', error)
        alert('Ошибка: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    closeComponentModal() {
      this.showComponentModal = false
      this.editingComponent = null
      this.componentType = ''
    },
    
    // Управление заказами (без изменений)
    async updateOrderStatus(orderId, status) {
      try {
        await adminService.updateOrderStatus(orderId, status)
        alert('Статус заказа обновлен')
        await this.loadOrders()
      } catch (error) {
        alert('Ошибка обновления статуса: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    viewOrderDetails(order) {
      this.selectedOrder = order
      this.showOrderModal = true
    },
    
    closeOrderModal() {
      this.showOrderModal = false
      this.selectedOrder = null
    },
    
    // Управление пользователями (без изменений)
    async toggleAdmin(userId, makeAdmin) {
      const action = makeAdmin ? 'назначить администратором' : 'снять права администратора'
      if (!confirm(`Вы уверены, что хотите ${action} этого пользователя?`)) return
      
      try {
        await adminService.makeAdmin(userId, makeAdmin)
        await this.loadUsers()
        alert(`Права пользователя успешно ${makeAdmin ? 'выданы' : 'отозваны'}`)
      } catch (error) {
        alert('Ошибка изменения прав: ' + (error.response?.data?.detail || error.message))
      }
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.admin-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.nav-btn {
  padding: 0.75rem 1.5rem;
  background: #f5f5f5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: #e9ecef;
}

.nav-btn.active {
  background: #ff6b6b;
  color: white;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  margin: 0;
  color: #333;
}

.stats {
  display: flex;
  gap: 1rem;
}

.stat-card {
  padding: 1rem 1.5rem;
  background: #e7f3ff;
  border-radius: 8px;
  text-align: center;
  min-width: 150px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ff6b6b;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.table-container {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #eee;
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.data-table tr:hover {
  background: #f9f9f9;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-badge.available {
  background: #d4edda;
  color: #155724;
}

.status-badge.unavailable {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.admin {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.user {
  background: #fff3cd;
  color: #856404;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 0.25rem;
  font-size: 0.9rem;
}

.btn-edit {
  background: #4dabf7;
  color: white;
}

.btn-delete {
  background: #ff4757;
  color: white;
}

.btn-view {
  background: #20c997;
  color: white;
}

.btn-make-admin {
  background: #4dabf7;
  color: white;
}

.btn-remove-admin {
  background: #ffa726;
  color: white;
}

.status-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.components-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.comp-tab-btn {
  padding: 0.5rem 1rem;
  background: #f5f5f5;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.comp-tab-btn:hover {
  background: #e9ecef;
}

.comp-tab-btn.active {
  background: #ff6b6b;
  color: white;
}

.components-section {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* ДОБАВЛЕНО: Стили для модального окна торта */
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

.modal-content {
  background: white;
  border-radius: 10px;
  width: 500px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.modal-close:hover {
  color: #333;
}

.modal-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.form-group input[type="checkbox"] {
  margin-right: 0.5rem;
}

.image-upload input[type="file"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-primary {
  background: #ff6b6b;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-primary:hover {
  background: #ff5252;
}

.btn-secondary:hover {
  background: #5a6268;
}
</style>