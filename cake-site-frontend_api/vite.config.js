// cake-site-frontend/vite.config.js
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  return {
    plugins: [vue()],
    // Для разработки через Docker
    server: {
      host: true, // слушаем все интерфейсы
      port: 3000,
      strictPort: true,
      // В Docker нам не нужен proxy, т.к. nginx будет проксировать
    },
    // Для production сборки
    build: {
      outDir: 'dist',
      sourcemap: mode === 'development'
    }
  }
})