<template>
  <div id="app">
    <!-- Навигация -->
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-logo">
          🎂 Кондитерская
        </router-link>
        
        <div class="nav-links">
          <router-link to="/cakes">Торты</router-link>
          <router-link to="/constructor">Конструктор</router-link>
          
          <template v-if="authStore.isAuthenticated">
            <router-link to="/orders">Мои заказы</router-link>
            <router-link to="/profile">Профиль</router-link>
            
            <!-- Ссылка на админ-панель для админов -->
            <router-link 
              v-if="authStore.user?.is_admin" 
              to="/admin" 
              class="admin-link"
            >
              ⚙️ Админ
            </router-link>
            
            <button @click="handleLogout" class="logout-btn">Выйти</button>
          </template>
          
          <template v-else>
            <router-link to="/login">Войти</router-link>
            <router-link to="/register">Регистрация</router-link>
          </template>
        </div>
      </div>
    </nav>

    <!-- Основной контент -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Чат-виджет (только для авторизованных пользователей) -->
    <ChatWidget v-if="authStore.isAuthenticated" />

    <!-- Футер -->
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 Кондитерская. Все права защищены.</p>
        <p class="footer-contact">
          Телефон: +7 (XXX) XXX-XX-XX | 
          Email: info@confectionery.ru
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import ChatWidget from './components/ChatWidget.vue'

export default {
  name: 'App',
  components: {
    ChatWidget
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()

    // Скрываем навигацию на страницах логина/регистрации
    const showNavigation = computed(() => {
      return !['Login', 'Register'].includes(route.name)
    })

    const handleLogout = () => {
      authStore.logout()
      router.push('/')
    }

    // Проверяем токен при загрузке приложения
    const initializeApp = async () => {
      if (authStore.token) {
        try {
          await authStore.fetchUser()
        } catch (error) {
          console.error('Ошибка инициализации пользователя:', error)
          // Если токен невалиден, разлогиниваем
          if (error.response?.status === 401) {
            authStore.logout()
          }
        }
      }
    }

    // Вызываем инициализацию
    initializeApp()

    return {
      authStore,
      handleLogout,
      showNavigation
    }
  }
}
</script>

<style>
/* Все стили остаются без изменений */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f9f9f9;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Навигация */
.navbar {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  padding: 1rem 0;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.3s ease;
}

.nav-logo:hover {
  transform: scale(1.05);
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-links a:not(.admin-link):hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

/* Стиль для ссылки админа */
.admin-link {
  color: #ffd700 !important;
  font-weight: bold;
  background: rgba(255, 215, 0, 0.15);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 2px solid rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
}

.admin-link:hover {
  background: rgba(255, 215, 0, 0.25);
  border-color: rgba(255, 215, 0, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
}

/* Кнопка выхода */
.logout-btn {
  background: transparent;
  border: 2px solid white;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Основной контент */
.main-content {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 2rem auto;
  padding: 0 2rem;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Футер */
.footer {
  background: linear-gradient(135deg, #333 0%, #444 100%);
  color: white;
  padding: 2rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.footer-contact {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Общие стили для кнопок */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
  border: none;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

/* Карточки */
.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #eee;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

/* Формы */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fff;
}

.form-input:focus {
  outline: none;
  border-color: #ff6b6b;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
}

.form-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

/* Утилитарные классы */
.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

.p-1 { padding: 0.5rem; }
.p-2 { padding: 1rem; }
.p-3 { padding: 1.5rem; }
.p-4 { padding: 2rem; }

/* Адаптивность */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
    padding: 0 1rem;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .nav-links a {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }

  .main-content {
    padding: 0 1rem;
    margin: 1rem auto;
  }

  .nav-logo {
    font-size: 1.5rem;
  }

  .btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .nav-links {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-links a,
  .logout-btn {
    width: 100%;
    text-align: center;
  }

  .main-content {
    padding: 0 0.75rem;
  }
}

/* Анимации */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

/* Кастомный скроллбар */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #ff6b6b;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #ff5252;
}
</style>