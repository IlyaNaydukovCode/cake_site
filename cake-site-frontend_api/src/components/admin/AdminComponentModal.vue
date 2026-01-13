<template>
    <div class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ getTitle() }}</h2>
          <button @click="$emit('close')" class="close-btn">×</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label>Название:</label>
              <input v-model="form.name" type="text" class="form-input" required>
            </div>
            
            <div class="form-group">
              <label>Описание:</label>
              <textarea v-model="form.description" class="form-input" rows="3"></textarea>
            </div>
            
            <div class="form-group">
              <label>Цена за единицу (₽):</label>
              <input v-model.number="form.price_per_unit" type="number" step="0.01" class="form-input" required>
            </div>
            
            <div class="form-group">
              <label class="checkbox-label">
                <input v-model="form.is_available" type="checkbox">
                <span>Доступен для заказа</span>
              </label>
            </div>
            
            <div class="modal-footer">
              <button type="button" @click="$emit('close')" class="btn btn-secondary">
                Отмена
              </button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Сохранение...' : 'Сохранить' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminComponentModal',
    props: {
      component: {
        type: Object,
        default: null
      },
      type: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        form: {
          name: '',
          description: '',
          price_per_unit: 0,
          is_available: true
        },
        loading: false
      }
    },
    computed: {
      componentTypeText() {
        const types = {
          layer: 'корж',
          cream: 'крем',
          filling: 'начинка',
          decoration: 'украшение'
        }
        return types[this.type] || 'компонент'
      }
    },
    watch: {
      component: {
        immediate: true,
        handler(newVal) {
          if (newVal) {
            this.form = { ...newVal }
          } else {
            this.resetForm()
          }
        }
      }
    },
    methods: {
      getTitle() {
        return this.component 
          ? `Редактировать ${this.componentTypeText}`
          : `Добавить ${this.componentTypeText}`
      },
      
      resetForm() {
        this.form = {
          name: '',
          description: '',
          price_per_unit: 0,
          is_available: true
        }
      },
      
      handleSubmit() {
        this.loading = true
        
        const componentData = Object.fromEntries(
          Object.entries(this.form).filter(([_, v]) => v !== '' && v !== null)
        )
        
        this.$emit('save', componentData)
        this.loading = false
      }
    }
  }
  </script>