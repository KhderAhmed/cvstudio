import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// عنوان الباك إند أثناء التطوير. يمكن تغييره: VITE_API_PROXY=http://backend:8000 npm run dev
const backend = process.env.VITE_API_PROXY || 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': backend,
      // الصور والصوت والفيديو المرفوعة (بدونها تظهر 404 أثناء التطوير)
      '/media': backend,
    },
  },
})
