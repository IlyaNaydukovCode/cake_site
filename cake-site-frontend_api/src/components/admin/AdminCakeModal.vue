<template>
    <div class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingCake ? 'Редактировать торт' : 'Добавить торт' }}</h2>
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
            
            <div class="form-row">
              <div class="form-group">
                <label>Цена (₽):</label>
                <input v-model.number="form.price" type="number" step="0.01" class="form-input" required>
              </div>
              
              <div class="form-group">
                <label>Вес (г):</label>
                <input v-model.number="form.weight" type="number" class="form-input">
              </div>
            </div>
            
            <div class="form-group">
              <label>URL изображения:</label>
              <input v-model="form.image_url" type="url" class="form-input">
            </div>
            
            <div class="form-group">
              <label>Ингредиенты:</label>
              <textarea v-model="form.ingredients" class="form-input" rows="2"></textarea>
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
    name: 'AdminCakeModal',
    props: {
      cake: {
        type: Object,
        default: null
      }
    },
    data() {
      return {
        form: {
          name: '',
          description: '',
          price: 0,
          weight: 0,
          image_url: '',
          ingredients: '',
          is_available: true
        },
        loading: false
      }
    },
    watch: {
      cake: {
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
      resetForm() {
        this.form = {
          name: '',
          description: '',
          price: 0,
          weight: 0,
          image_url: '',
          ingredients: '',
          is_available: true
        }
      },
      
      handleSubmit() {
        this.loading = true
        
        // Удаляем пустые поля
        const cakeData = Object.fromEntries(
          Object.entries(this.form).filter(([_, v]) => v !== '' && v !== null)
        )
        
        this.$emit('save', cakeData)
        this.loading = false
      }
    }
  }
  </script>
  
  <style scoped>
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
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #eee;
  }
  
  .modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.8rem;
    cursor: pointer;
    color: #666;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  
  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
  }
  
  .modal-footer {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1.5rem;
  }
  </style>