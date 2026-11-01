import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
    server: {
    proxy: {
      "/signup": "http://127.0.0.1:8000",
      "/login": "http://127.0.0.1:8000",
      "/courses": "http://127.0.0.1:8000",
      "/gpa": "http://127.0.0.1:8000",
      "/goal": "http://127.0.0.1:8000",
      "/final-grade": "http://127.0.0.1:8000",
    },
  },
})
