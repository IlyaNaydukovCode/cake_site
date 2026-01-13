<template>
  <div class="login">
    <div class="login-container">
      <div class="login-card">
        <h2>Вход в аккаунт</h2>
        <form @submit.prevent="handleLogin">
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
            <label class="form-label">Пароль</label>
            <input 
              v-model="form.password"
              type="password" 
              class="form-input"
              required
            >
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Вход...' : 'Войти' }}
          </button>

          <p class="register-link">
            Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'LoginView',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      try {
        const authStore = useAuthStore()
        await authStore.login(this.form)
        this.$router.push('/')
      } catch (error) {
        alert('Ошибка входа: ' + (error.response?.data?.detail || 'Неверные данные'))
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.login-card h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #ff6b6b;
  text-decoration: none;
}
</style>