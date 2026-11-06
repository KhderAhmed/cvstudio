import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// مسارات المصادقة: لا نحاول تجديد التوكن عند فشلها
const AUTH_URLS = ['/token/', '/token/refresh/', '/auth/register/']

function clearSession() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('username')
}

// تجديد واحد فقط حتى لو فشلت عدة طلبات معاً
let refreshPromise = null

async function refreshAccessToken() {
  const refresh = localStorage.getItem('refresh')
  if (!refresh) throw new Error('no refresh token')

  // axios العادي (بدون interceptors) حتى لا ندخل في حلقة
  const { data } = await axios.post('/api/token/refresh/', { refresh })
  localStorage.setItem('access', data.access)
  if (data.refresh) localStorage.setItem('refresh', data.refresh)
  return data.access
}

// إضافة التوكن تلقائياً (عدا مسارات السير العامة)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token && !config.url?.startsWith('/public/')) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    const status = error.response?.status
    const hadToken = !!localStorage.getItem('access')

    const shouldRefresh =
      status === 401 &&
      original &&
      !original._retry &&
      hadToken &&
      !AUTH_URLS.some((u) => original.url?.startsWith(u))

    if (!shouldRefresh) return Promise.reject(error)

    original._retry = true
    try {
      refreshPromise ??= refreshAccessToken().finally(() => {
        refreshPromise = null
      })
      const access = await refreshPromise
      original.headers.Authorization = `Bearer ${access}`
      return api(original)
    } catch {
      // فشل التجديد (انتهت صلاحية الجلسة) → تسجيل خروج
      clearSession()
      if (!window.location.pathname.startsWith('/login')) {
        const here = window.location.pathname + window.location.search
        window.location.href = `/login?redirect=${encodeURIComponent(here)}`
      }
      return Promise.reject(error)
    }
  }
)

export default api
