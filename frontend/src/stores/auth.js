import { defineStore } from 'pinia'
import api from '@/api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    access: localStorage.getItem('access') || '',
    refresh: localStorage.getItem('refresh') || '',
    username: localStorage.getItem('username') || '',
    user: null,
    loading: false,
    error: '',
  }),

  getters: {
    isAuthenticated: (state) => !!state.access,
  },

  actions: {
    async login(username, password) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await api.post('/token/', { username, password })
        this.access = data.access
        this.refresh = data.refresh
        this.username = username

        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        localStorage.setItem('username', username)

        await this.fetchUser()
        return true
      } catch (err) {
        this.error = err.response?.status === 401
          ? 'اسم المستخدم أو كلمة المرور غير صحيحة'
          : 'تعذّر الاتصال بالخادم، حاول مرة أخرى'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchUser() {
      try {
        const { data } = await api.get('/users/me/')
        this.user = data
      } catch (err) {
        console.warn('could not fetch user', err)
      }
    },

    logout() {
      this.access = ''
      this.refresh = ''
      this.username = ''
      this.user = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('username')
    },
  },
})
