<template>
  <div class="component-table">
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Описание</th>
            <th>Цена</th>
            <th>Доступен</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="component in components" :key="component.id">
            <td>{{ component.id }}</td>
            <td>
              <strong>{{ component.name }}</strong>
            </td>
            <td class="description-cell">
              {{ component.description ? component.description.substring(0, 50) + '...' : '—' }}
            </td>
            <td>{{ component.price_per_unit }} ₽</td>
            <td>
              <span :class="['status-badge', component.is_available ? 'available' : 'unavailable']">
                {{ component.is_available ? 'Да' : 'Нет' }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button @click="$emit('edit', component)" class="btn-sm btn-edit" title="Редактировать">
                  ✏️
                </button>
                <button @click="$emit('delete', component.id)" class="btn-sm btn-delete" title="Удалить">
                  🗑️
                </button>
                <button 
                  @click="$emit('toggleAvailability', component.id, !component.is_available)"
                  :class="['btn-sm', component.is_available ? 'btn-disable' : 'btn-enable']"
                  :title="component.is_available ? 'Сделать недоступным' : 'Сделать доступным'"
                >
                  {{ component.is_available ? '🚫' : '✅' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ComponentTable',
  props: {
    components: {
      type: Array,
      default: () => []
    },
    type: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.component-table {
  width: 100%;
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
  table-layout: fixed;
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
  vertical-align: middle;
}

.data-table tr:hover {
  background: #f9f9f9;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.description-cell {
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
  display: inline-block;
  min-width: 50px;
  text-align: center;
}

.status-badge.available {
  background: #d4edda;
  color: #155724;
}

.status-badge.unavailable {
  background: #f8d7da;
  color: #721c24;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: nowrap;
}

.btn-sm {
  padding: 0.4rem 0.6rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  min-height: 36px;
}

.btn-sm:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.btn-edit {
  background: #4dabf7;
  color: white;
}

.btn-edit:hover {
  background: #3b9ae6;
}

.btn-delete {
  background: #ff4757;
  color: white;
}

.btn-delete:hover {
  background: #ff3742;
}

.btn-disable {
  background: #ffa726;
  color: white;
}

.btn-disable:hover {
  background: #ff9800;
}

.btn-enable {
  background: #20c997;
  color: white;
}

.btn-enable:hover {
  background: #1ab386;
}

/* Стили для заголовков колонок */
.data-table th:nth-child(1) { width: 80px; }  /* ID */
.data-table th:nth-child(2) { width: 180px; } /* Название */
.data-table th:nth-child(3) { width: 250px; } /* Описание */
.data-table th:nth-child(4) { width: 120px; } /* Цена */
.data-table th:nth-child(5) { width: 120px; } /* Доступен */
.data-table th:nth-child(6) { width: 180px; } /* Действия */

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .table-container {
    overflow-x: auto;
  }
  
  .data-table {
    min-width: 700px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .btn-sm {
    width: 100%;
    margin-bottom: 0.25rem;
  }
}
</style>