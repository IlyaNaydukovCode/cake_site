<template>
  <div class="register">
    <div class="register-container">
      <div class="register-card">
        <h2>Регистрация</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label class="form-label">Email</label>
            <input 
              v-model="form.email"
              type="email" 
              class="form-input"
              required
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
            <label class="form-label">Адрес</label>
            <input 
              v-model="form.address"
              type="text" 
              class="form-input"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Пароль</label>
            <input 
              v-model="form.password"
              type="password" 
              class="form-input"
              required
            >
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>

          <p class="login-link">
            Уже есть аккаунт? <router-link to="/login">Войти</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'RegisterView',
  data() {
    return {
      form: {
        email: '',
        full_name: '',
        phone: '',
        address: '',
        password: ''
      },
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      try {
        const authStore = useAuthStore()
        await authStore.register(this.form)
        alert('Регистрация успешна! Теперь войдите в аккаунт.')
        this.$router.push('/login')
      } catch (error) {
        alert('Ошибка регистрации: ' + (error.response?.data?.detail || 'Попробуйте еще раз'))
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.register-container {
  width: 100%;
  max-width: 400px;
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.register-card h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
}

.login-link a {
  color: #ff6b6b;
  text-decoration: none;
}
</style>