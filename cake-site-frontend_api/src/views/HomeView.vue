<template>
  <div class="home">
    <div class="hero-section">
      <h1>Добро пожаловать в кондитерскую!</h1>
      <p>Закажите вкуснейшие торты или создайте свой уникальный</p>
      <div class="hero-buttons">
        <router-link to="/cakes" class="btn btn-primary">Смотреть каталог</router-link>
        <router-link to="/constructor" class="btn btn-secondary">Создать торт</router-link>
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <h3>🎂 Готовые торты</h3>
        <p>Выберите из нашего каталога готовых тортов</p>
      </div>
      <div class="feature-card">
        <h3>🔧 Конструктор</h3>
        <p>Создайте торт своей мечты с любыми начинками</p>
      </div>
      <div class="feature-card">
        <h3>🚚 Доставка</h3>
        <p>Быстрая доставка по городу или самовывоз</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  text-align: center;
}

.hero-section {
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  color: white;
  padding: 4rem 2rem;
  border-radius: 15px;
  margin-bottom: 3rem;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-secondary {
  background: transparent;
  border: 2px solid white;
  color: white;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: #ff6b6b;
}
</style>