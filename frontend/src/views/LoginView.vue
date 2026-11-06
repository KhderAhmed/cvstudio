<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center px-4" dir="rtl">
    <div class="w-full max-w-sm">

      <!-- الشعار -->
      <div class="text-center mb-8">
        <div
          class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-teal-400 to-sky-500 flex items-center justify-center text-3xl">
          🎨
        </div>
        <h1 class="text-2xl font-bold text-white">CV Studio</h1>
        <p class="text-slate-400 text-sm mt-1">سيرتك الحيّة في رابط واحد</p>
      </div>

      <!-- النموذج -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h2 class="text-lg font-bold text-white mb-4">تسجيل الدخول</h2>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm text-slate-400 mb-1.5">اسم المستخدم</label>
            <input v-model="username" type="text" required autofocus
              class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-teal-500 focus:outline-none transition"
              placeholder="admin" />
          </div>

          <div>
            <label class="block text-sm text-slate-400 mb-1.5">كلمة المرور</label>
            <input v-model="password" type="password" required
              class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-teal-500 focus:outline-none transition"
              placeholder="••••••••" />
          </div>

          <p v-if="auth.error" class="text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">
            {{ auth.error }}
          </p>

          <button type="submit" :disabled="auth.loading"
            class="w-full py-2.5 rounded-lg bg-gradient-to-r from-teal-500 to-sky-500 hover:from-teal-400 hover:to-sky-400 text-slate-950 font-bold transition disabled:opacity-50 disabled:cursor-not-allowed">
            {{ auth.loading ? 'جاري الدخول…' : 'دخول' }}
          </button>
          <div class="text-center text-sm text-slate-400 mt-4">
            ليس لديك حساب؟
            <router-link to="/register" class="text-teal-400 hover:text-teal-300">
              سجّل الآن
            </router-link>
          </div>
        </form>
      </div>

      <p class="text-center text-xs text-slate-600 mt-6">
        © {{ new Date().getFullYear() }} CV Studio
      </p>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const password = ref('')

async function handleLogin() {
  const ok = await auth.login(username.value, password.value)
  if (ok) {
    router.push(route.query.redirect || '/dashboard')
  }
}
</script>