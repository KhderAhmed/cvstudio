<template>
  <div class="min-h-screen bg-slate-950 text-white" dir="rtl">

    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="$router.push('/dashboard')" class="text-slate-400 hover:text-white transition">
            ← رجوع
          </button>
          <h1 class="text-lg font-bold">📈 الإحصائيات</h1>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8" v-if="!loading">

      <!-- إحصائيات عامة -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <p class="text-xs text-slate-500 mb-1">إجمالي المشاهدات</p>
          <p class="text-4xl font-bold text-teal-400">{{ userStats.total_views || 0 }}</p>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <p class="text-xs text-slate-500 mb-1">آخر 7 أيام</p>
          <p class="text-4xl font-bold text-sky-400">{{ userStats.views_last_7_days || 0 }}</p>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <p class="text-xs text-slate-500 mb-1">عدد السير</p>
          <p class="text-4xl font-bold text-purple-400">{{ userStats.total_resumes || 0 }}</p>
        </div>
      </div>

      <!-- اختيار السيرة -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
        <label class="block text-sm text-slate-400 mb-2">اختر سيرة لعرض تفاصيلها</label>
        <select v-model="selectedResume"
          @change="loadResumeAnalytics"
          class="w-full max-w-md px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none">
          <option :value="null">— اختر —</option>
          <option v-for="r in userStats.per_resume" :key="r.id" :value="r.id">
            {{ r.full_name }} ({{ r.views_count }} مشاهدة)
          </option>
        </select>
      </div>

      <!-- تفاصيل سيرة -->
      <div v-if="selectedResume && resumeStats">
        
        <!-- إحصائيات -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <p class="text-xs text-slate-500 mb-1">إجمالي المشاهدات</p>
            <p class="text-3xl font-bold text-teal-400">{{ resumeStats.total_views }}</p>
          </div>
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <p class="text-xs text-slate-500 mb-1">آخر 7 أيام</p>
            <p class="text-3xl font-bold text-sky-400">{{ resumeStats.views_last_7_days }}</p>
          </div>
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <p class="text-xs text-slate-500 mb-1">آخر 30 يوم</p>
            <p class="text-3xl font-bold text-purple-400">{{ resumeStats.views_last_30_days }}</p>
          </div>
        </div>

        <!-- الرسم البياني -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
          <h2 class="text-base font-semibold text-teal-400 mb-4">📊 المشاهدات (آخر 14 يوم)</h2>
          <div v-if="resumeStats.daily_views?.length" class="relative h-64">
            <canvas ref="chartCanvas"></canvas>
          </div>
          <p v-else class="text-center py-8 text-slate-500">لا توجد بيانات بعد</p>
        </div>

        <!-- الأجهزة -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 class="text-base font-semibold text-teal-400 mb-4">📱 حسب الجهاز</h2>
            <div v-if="resumeStats.device_stats?.length" class="space-y-3">
              <div v-for="d in resumeStats.device_stats" :key="d.device" class="flex items-center justify-between">
                <span class="text-sm">
                  {{ d.device === 'mobile' ? '📱 هاتف' : d.device === 'tablet' ? '📱 جهاز لوحي' : '💻 كمبيوتر' }}
                </span>
                <span class="font-bold text-teal-400">{{ d.count }}</span>
              </div>
            </div>
            <p v-else class="text-center py-4 text-slate-500 text-sm">لا توجد بيانات</p>
          </div>

          <!-- آخر المشاهدات -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 class="text-base font-semibold text-teal-400 mb-4">🕐 آخر المشاهدات</h2>
            <div v-if="resumeStats.recent_views?.length" class="space-y-2 max-h-64 overflow-y-auto">
              <div v-for="(v, i) in resumeStats.recent_views" :key="i"
                class="flex items-center justify-between text-sm py-2 border-b border-slate-800/50">
                <span class="text-slate-400">{{ formatDate(v.viewed_at) }}</span>
                <span v-if="v.referrer" class="text-xs text-slate-500 truncate max-w-[40%]" dir="ltr">
                  {{ referrerHost(v.referrer) }}
                </span>
                <span class="text-xs px-2 py-0.5 rounded bg-slate-800">
                  {{ v.device === 'mobile' ? '📱' : v.device === 'tablet' ? '📱' : '💻' }}
                </span>
              </div>
            </div>
            <p v-else class="text-center py-4 text-slate-500 text-sm">لا توجد بيانات</p>
          </div>
        </div>

      </div>

      <div v-else-if="!selectedResume" class="text-center py-20 text-slate-500">
        <p class="text-4xl mb-3">📊</p>
        <p>اختر سيرة من القائمة أعلاه لعرض تفاصيلها</p>
      </div>

    </main>

    <div v-else class="text-center py-20 text-slate-500">
      <div class="inline-block w-8 h-8 border-2 border-slate-700 border-t-teal-400 rounded-full animate-spin mb-3"></div>
      <p>جاري التحميل…</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import {
  Chart, LineController, LineElement, PointElement,
  LinearScale, CategoryScale, Filler, Tooltip,
} from 'chart.js'
import api from '@/api/client'

// نسجّل فقط ما نحتاجه (يصغّر حجم الحزمة)
Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Filler, Tooltip)

const loading = ref(true)
const userStats = ref({})
const resumeStats = ref(null)
const selectedResume = ref(null)
const chartCanvas = ref(null)
let chartInstance = null

async function loadUserStats() {
  try {
    const { data } = await api.get('/analytics/me/')
    userStats.value = data
  } catch (err) {
    console.error('USER STATS ERROR:', err.response?.data)
  }
}

async function loadResumeAnalytics() {
  if (!selectedResume.value) {
    resumeStats.value = null
    chartInstance?.destroy()
    chartInstance = null
    return
  }
  try {
    const { data } = await api.get(`/analytics/resumes/${selectedResume.value}/`)
    resumeStats.value = data

    await nextTick()
    drawChart()
  } catch (err) {
    console.error('RESUME STATS ERROR:', err.response?.data)
  }
}

function drawChart() {
  if (!chartCanvas.value || !resumeStats.value?.daily_views) return

  if (chartInstance) chartInstance.destroy()

  const labels = resumeStats.value.daily_views.map(d => d.date)
  const values = resumeStats.value.daily_views.map(d => d.count)

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'المشاهدات',
        data: values,
        borderColor: '#2dd4bf',
        backgroundColor: 'rgba(45, 212, 191, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#2dd4bf',
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: '#8aa0b3', stepSize: 1 },
          grid: { color: 'rgba(36, 51, 66, 0.5)' },
        },
        x: {
          ticks: { color: '#8aa0b3' },
          grid: { display: false },
        },
      },
    },
  })
}

function referrerHost(url) {
  try {
    return new URL(url).host
  } catch {
    return url
  }
}

function formatDate(iso) {
  const d = new Date(iso)
  return d.toLocaleString('ar', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onBeforeUnmount(() => {
  chartInstance?.destroy()
})

onMounted(async () => {
  await loadUserStats()
  loading.value = false
})
</script>