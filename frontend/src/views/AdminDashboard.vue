<template>
  <div class="min-h-screen bg-slate-950 text-white" dir="rtl">

    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="$router.push('/dashboard')" class="text-slate-400 hover:text-white transition">
            ← رجوع
          </button>
          <h1 class="text-lg font-bold">🛡️ لوحة الإدارة</h1>
        </div>
        <button @click="handleLogout" class="text-sm text-slate-400 hover:text-red-400 transition">
          خروج
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8" v-if="!loading">

      <!-- تبويبات -->
      <div class="flex gap-2 mb-6 bg-slate-900 border border-slate-800 rounded-xl p-1.5">
        <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
          class="flex-1 px-4 py-2 rounded-lg text-sm font-bold transition"
          :class="activeTab === tab.id
            ? 'bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950'
            : 'text-slate-400 hover:text-white'">
          {{ tab.icon }} {{ tab.label }}
        </button>
      </div>

      <!-- نظرة عامة -->
      <div v-if="activeTab === 'overview'">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <p class="text-xs text-slate-500 mb-1">إجمالي المستخدمين</p>
            <p class="text-3xl font-bold text-teal-400">{{ stats?.total_users || 0 }}</p>
          </div>
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <p class="text-xs text-slate-500 mb-1">المستخدمون النشطون</p>
            <p class="text-3xl font-bold text-green-400">{{ stats?.active_users || 0 }}</p>
          </div>
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <p class="text-xs text-slate-500 mb-1">إجمالي السير</p>
            <p class="text-3xl font-bold text-sky-400">{{ stats?.total_resumes || 0 }}</p>
          </div>
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <p class="text-xs text-slate-500 mb-1">السير العامة</p>
            <p class="text-3xl font-bold text-purple-400">{{ stats?.public_resumes || 0 }}</p>
          </div>
        </div>

        <!-- آخر المستخدمين -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
          <h2 class="text-base font-semibold text-teal-400 mb-4">آخر المستخدمين</h2>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-slate-400 border-b border-slate-800">
                  <th class="text-right py-2 px-3">المستخدم</th>
                  <th class="text-right py-2 px-3">البريد</th>
                  <th class="text-right py-2 px-3">الخطة</th>
                  <th class="text-right py-2 px-3">التاريخ</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="u in stats?.recent_users" :key="u.id"
                  class="border-b border-slate-800/50 hover:bg-slate-800/30">
                  <td class="py-2 px-3 font-medium">{{ u.username }}</td>
                  <td class="py-2 px-3 text-slate-400">{{ u.email || '—' }}</td>
                  <td class="py-2 px-3">
                    <span class="text-xs px-2 py-0.5 rounded bg-slate-700">{{ u.plan }}</span>
                  </td>
                  <td class="py-2 px-3 text-slate-500 text-xs">
                    {{ u.created_at?.slice(0, 10) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- آخر السير -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 class="text-base font-semibold text-teal-400 mb-4">آخر السير</h2>
          <div v-if="stats?.recent_resumes?.length" class="space-y-2">
            <div v-for="r in stats.recent_resumes" :key="r.id"
              class="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
              <div>
                <p class="font-medium">{{ r.full_name }}</p>
                <p class="text-xs text-slate-500">{{ r.job_title || '—' }} · {{ r.user__username }}</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-xs px-2 py-0.5 rounded"
                  :class="r.is_public ? 'bg-green-500/20 text-green-400' : 'bg-slate-700 text-slate-400'">
                  {{ r.is_public ? 'عامة' : 'خاصة' }}
                </span>
                <a :href="`/cv/${r.id}`" target="_blank" rel="noopener noreferrer"
                  class="text-xs text-sky-400 hover:text-sky-300">
                  عرض ↗
                </a>
              </div>
            </div>
          </div>
          <p v-else class="text-slate-500 text-sm text-center py-4">لا توجد سير بعد</p>
        </div>
      </div>

      <!-- المستخدمون -->
      <div v-if="activeTab === 'users'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 class="text-base font-semibold text-teal-400 mb-4">كل المستخدمين ({{ users.length }})</h2>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-slate-400 border-b border-slate-800">
                <th class="text-right py-2 px-3">#</th>
                <th class="text-right py-2 px-3">المستخدم</th>
                <th class="text-right py-2 px-3">البريد</th>
                <th class="text-right py-2 px-3">الخطة</th>
                <th class="text-right py-2 px-3">دور</th>
                <th class="text-right py-2 px-3">الحالة</th>
                <th class="text-right py-2 px-3">إجراء</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in users" :key="u.id"
                class="border-b border-slate-800/50 hover:bg-slate-800/30">
                <td class="py-2 px-3 text-slate-500">{{ u.id }}</td>
                <td class="py-2 px-3 font-medium">{{ u.username }}</td>
                <td class="py-2 px-3 text-slate-400 text-xs">{{ u.email || '—' }}</td>
                <td class="py-2 px-3">
                  <span class="text-xs px-2 py-0.5 rounded bg-slate-700">{{ u.plan }}</span>
                </td>
                <td class="py-2 px-3">
                  <span v-if="u.is_staff" class="text-xs px-2 py-0.5 rounded bg-purple-500/20 text-purple-400">
                    مدير
                  </span>
                  <span v-else class="text-xs text-slate-500">مستخدم</span>
                </td>
                <td class="py-2 px-3">
                  <span class="text-xs px-2 py-0.5 rounded"
                    :class="u.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'">
                    {{ u.is_active ? 'نشط' : 'معطل' }}
                  </span>
                </td>
                <td class="py-2 px-3">
                  <button @click="toggleUser(u)"
                    class="text-xs px-3 py-1 rounded transition"
                    :class="u.is_active
                      ? 'bg-red-500/20 hover:bg-red-500/30 text-red-400'
                      : 'bg-green-500/20 hover:bg-green-500/30 text-green-400'">
                    {{ u.is_active ? 'تعطيل' : 'تفعيل' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- السير -->
      <div v-if="activeTab === 'resumes'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 class="text-base font-semibold text-teal-400 mb-4">كل السير ({{ resumes.length }})</h2>
        <div class="space-y-2">
          <div v-for="r in resumes" :key="r.id"
            class="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg hover:bg-slate-800 transition">
            <div class="flex-1">
              <p class="font-medium">{{ r.full_name }}</p>
              <p class="text-xs text-slate-500">
                {{ r.job_title || '—' }} · المستخدم: {{ r.username }} · {{ r.updated_at?.slice(0, 10) }}
              </p>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs px-2 py-0.5 rounded"
                :class="r.is_public ? 'bg-green-500/20 text-green-400' : 'bg-slate-700 text-slate-400'">
                {{ r.is_public ? 'عامة' : 'خاصة' }}
              </span>
              <a :href="`/cv/${r.id}`" target="_blank" rel="noopener noreferrer"
                class="text-xs text-sky-400 hover:text-sky-300">عرض ↗</a>
              <button @click="deleteResume(r)"
                class="text-xs px-3 py-1 rounded bg-red-500/20 hover:bg-red-500/30 text-red-400">
                حذف
              </button>
            </div>
          </div>
        </div>
      </div>

    </main>

    <div v-else class="text-center py-20 text-slate-500">
      <div class="inline-block w-8 h-8 border-2 border-slate-700 border-t-teal-400 rounded-full animate-spin mb-3"></div>
      <p>جاري التحميل…</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/client'

const router = useRouter()
const auth = useAuthStore()

const stats = ref(null)
const users = ref([])
const resumes = ref([])
const loading = ref(true)
const activeTab = ref('overview')

const tabs = [
  { id: 'overview', label: 'نظرة عامة', icon: '📊' },
  { id: 'users', label: 'المستخدمون', icon: '👥' },
  { id: 'resumes', label: 'السير', icon: '📄' },
]

async function loadStats() {
  try {
    const { data } = await api.get('/admin/stats/')
    stats.value = data
  } catch (err) {
    if (err.response?.status === 403) {
      router.push('/dashboard')
    }
    console.error('STATS ERROR:', err.response?.data)
  }
}

async function loadUsers() {
  try {
    const { data } = await api.get('/admin/users/')
    users.value = data
  } catch (err) {
    console.error('USERS ERROR:', err.response?.data)
  }
}

async function loadResumes() {
  try {
    const { data } = await api.get('/admin/resumes/')
    resumes.value = data
  } catch (err) {
    console.error('RESUMES ERROR:', err.response?.data)
  }
}

async function toggleUser(u) {
  try {
    const { data } = await api.patch(`/admin/users/${u.id}/toggle/`)
    u.is_active = data.is_active
  } catch (err) {
    alert(err.response?.data?.detail || 'تعذّر')
  }
}

async function deleteResume(r) {
  if (!confirm(`حذف سيرة "${r.full_name}"؟`)) return
  try {
    await api.delete(`/admin/resumes/${r.id}/delete/`)
    resumes.value = resumes.value.filter(x => x.id !== r.id)
  } catch (err) {
    alert('تعذّر الحذف')
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

onMounted(async () => {
  await Promise.all([loadStats(), loadUsers(), loadResumes()])
  loading.value = false
})
</script>