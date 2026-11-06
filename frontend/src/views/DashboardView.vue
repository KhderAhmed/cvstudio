<template>
  <div class="min-h-screen bg-slate-950 text-white" dir="rtl">

    <!-- الشريط العلوي -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div
            class="w-9 h-9 rounded-lg bg-gradient-to-br from-teal-400 to-sky-500 flex items-center justify-center text-lg">
            🎨
          </div>
          <h1 class="text-lg font-bold">لوحة التحكم</h1>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-sm text-slate-400">{{ auth.username }}</span>
          <button @click="handleLogout" class="text-sm text-slate-400 hover:text-red-400 transition">
            خروج
          </button><router-link
  v-if="auth.user?.is_staff"
  :to="{ name: 'admin-dashboard' }"
  class="text-sm text-purple-400 hover:text-purple-300 transition"
>
  🛡️ الإدارة
</router-link>
<router-link to="/dashboard/analytics"
  class="text-sm text-sky-400 hover:text-sky-300 transition">
  📈 الإحصائيات
</router-link>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">

      <!-- إحصائيات -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p class="text-xs text-slate-500 mb-1">إجمالي السير</p>
          <p class="text-2xl font-bold text-teal-400">{{ resumes.length }}</p>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p class="text-xs text-slate-500 mb-1">السير العامة</p>
          <p class="text-2xl font-bold text-green-400">{{ publicCount }}</p>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p class="text-xs text-slate-500 mb-1">الخاصة</p>
          <p class="text-2xl font-bold text-slate-400">{{ privateCount }}</p>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p class="text-xs text-slate-500 mb-1">آخر تحديث</p>
          <p class="text-sm font-bold text-sky-400">{{ lastUpdate }}</p>
        </div>
      </div>

      <!-- العنوان + زر -->
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-base font-semibold text-slate-300">سيري الذاتية</h2>
        <button @click="createResume"
          class="px-4 py-2 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-sm transition">
          + سيرة جديدة
        </button>
      </div>

      <!-- تحميل -->
      <div v-if="loading" class="text-center py-20 text-slate-500">
        <div class="inline-block w-8 h-8 border-2 border-slate-700 border-t-teal-400 rounded-full animate-spin mb-3">
        </div>
        <p>جاري التحميل…</p>
      </div>

      <!-- فارغة -->
      <div v-else-if="resumes.length === 0" class="text-center py-20 border border-dashed border-slate-800 rounded-xl">
        <p class="text-4xl mb-3">📄</p>
        <p class="text-slate-400 mb-4">لا توجد سير ذاتية بعد</p>
        <button @click="createResume"
          class="px-5 py-2.5 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold transition">
          أنشئ سيرتك الأولى
        </button>
      </div>

      <!-- شبكة السير -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="resume in resumes" :key="resume.id"
          class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-teal-500/50 transition">
          <div class="flex items-start justify-between mb-3">
            <div class="w-12 h-12 rounded-full bg-slate-800 overflow-hidden flex items-center justify-center text-xl">
              <img v-if="resume.avatar" :src="resume.avatar" class="w-full h-full object-cover" />
              <span v-else>👤</span>
            </div>
            <span class="text-xs px-2 py-1 rounded-full"
              :class="resume.is_public ? 'bg-green-500/10 text-green-400' : 'bg-slate-800 text-slate-500'">
              {{ resume.is_public ? 'عامة' : 'خاصة' }}
            </span>
          </div>

          <h3 class="font-bold text-lg mb-1">{{ resume.full_name }}</h3>
          <p class="text-sm text-teal-400 mb-3">{{ resume.job_title || '—' }}</p>

          <div class="flex items-center gap-2 text-xs text-slate-500 mb-4">
            <span>📄 {{ resume.template }}</span>
            <span>·</span>
            <span>🌐 {{ resume.language }}</span>
          </div>

          <div class="flex gap-2">
            <button @click="$router.push(`/dashboard/edit/${resume.id}`)"
              class="flex-1 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-medium transition">
              تحرير
            </button>
          <button
  @click="$router.push(`/cv/${resume.id}`)"
  class="flex-1 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-medium transition"
>
  معاينة
</button>
            <button
  @click="copyLink(resume)"
  class="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm transition"
  title="نسخ الرابط"
>
  🔗
</button>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/client'
import { copyText } from '@/utils/clipboard'

const router = useRouter()
const auth = useAuthStore()
const resumes = ref([])
const loading = ref(true)

const publicCount = computed(() => resumes.value.filter(r => r.is_public).length)
const privateCount = computed(() => resumes.value.filter(r => !r.is_public).length)
const lastUpdate = computed(() => {
  if (!resumes.value.length) return '—'
  return resumes.value[0].updated_at?.slice(0, 10) || '—'
})

async function loadResumes() {
  loading.value = true
  try {
    const { data } = await api.get('/resumes/')
    resumes.value = data
  } catch (err) {
    console.error('failed to load resumes', err)
  } finally {
    loading.value = false
  }
}

async function copyLink(resume) {
  const url = `${window.location.origin}/cv/${resume.id}`
  const ok = await copyText(url)
  if (!ok) {
    alert('تعذّر نسخ الرابط')
  } else if (!resume.is_public) {
    alert('تم نسخ الرابط، لكن السيرة خاصة ولن يراها غيرك حتى تجعلها عامة')
  } else {
    alert('تم نسخ الرابط ✅')
  }
}

function createResume() {
  router.push('/dashboard/new')
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}


onMounted(() => {
  loadResumes()
  if (!auth.user) auth.fetchUser()
})
</script>