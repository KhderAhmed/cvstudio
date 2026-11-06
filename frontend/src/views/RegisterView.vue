<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center px-4" dir="rtl">
    <div class="w-full max-w-sm">

      <div class="text-center mb-8">
        <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-teal-400 to-sky-500 flex items-center justify-center text-3xl">
          🎨
        </div>
        <h1 class="text-2xl font-bold text-white">CV Studio</h1>
        <p class="text-slate-400 text-sm mt-1">أنشئ حسابك المجاني</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h2 class="text-lg font-bold text-white mb-4">تسجيل جديد</h2>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-sm text-slate-400 mb-1.5">اسم المستخدم *</label>
            <input v-model="username" type="text" required minlength="3"
              class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
          </div>

          <div>
            <label class="block text-sm text-slate-400 mb-1.5">البريد الإلكتروني</label>
            <input v-model="email" type="email"
              class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
          </div>

          <div>
            <label class="block text-sm text-slate-400 mb-1.5">الاسم الأول</label>
            <input v-model="firstName" type="text"
              class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
          </div>

          <div>
            <label class="block text-sm text-slate-400 mb-1.5">اسم العائلة</label>
            <input v-model="lastName" type="text"
              class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
          </div>

          <div>
            <label class="block text-sm text-slate-400 mb-1.5">كلمة المرور *</label>
            <input v-model="password" type="password" required minlength="8"
              class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            <p class="text-xs text-slate-500 mt-1">8 أحرف على الأقل</p>
          </div>

          <p v-if="error" class="text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">
            {{ error }}
          </p>

          <button type="submit" :disabled="loading"
            class="w-full py-2.5 rounded-lg bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950 font-bold transition disabled:opacity-50">
            {{ loading ? 'جاري التسجيل…' : 'إنشاء الحساب' }}
          </button>
        </form>

        <div class="mt-4 text-center text-sm text-slate-400">
          لديك حساب؟
          <router-link to="/login" class="text-teal-400 hover:text-teal-300">
            تسجيل الدخول
          </router-link>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const username = ref('')
const email = ref('')
const firstName = ref('')
const lastName = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await axios.post('/api/auth/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
    })
    router.push('/login')
  } catch (err) {
    const data = err.response?.data
    if (data) {
      const firstError = Object.values(data)[0]
      error.value = Array.isArray(firstError) ? firstError[0] : firstError
    } else {
      error.value = 'تعذّر التسجيل'
    }
  } finally {
    loading.value = false
  }
}
</script>