<template>
  <div class="min-h-screen bg-slate-950 text-white" :dir="resume?.language === 'ar' ? 'rtl' : 'ltr'">

    <!-- حالة التحميل -->
    <div v-if="loading" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="inline-block w-10 h-10 border-2 border-slate-700 border-t-teal-400 rounded-full animate-spin mb-4"></div>
        <p class="text-slate-500">جاري التحميل…</p>
      </div>
    </div>

    <!-- خطأ -->
    <div v-else-if="error" class="flex items-center justify-center min-h-screen px-4">
      <div class="text-center max-w-md">
        <p class="text-6xl mb-4">🔒</p>
        <h1 class="text-2xl font-bold mb-2">السيرة غير متاحة</h1>
        <p class="text-slate-400 text-sm">{{ error }}</p>
      </div>
    </div>

    <!-- السيرة -->
    <div v-else-if="resume" class="max-w-4xl mx-auto px-4 py-8">

      <!-- شريط علوي -->
      <div class="flex justify-between items-center mb-6 print:hidden">
        <router-link v-if="auth.isAuthenticated" to="/dashboard" class="text-sm text-slate-400 hover:text-white transition">
          ← لوحة التحكم
        </router-link>
        <span v-else></span>
        <div class="flex gap-2">
          <button v-if="!isPrivatePreview" @click="share" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm transition">
            🔗 مشاركة
          </button>
        <button @click="downloadPDF" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm transition">
  📄 PDF
</button>
          <button @click="print" class="px-3 py-1.5 rounded-lg bg-teal-500 text-slate-950 font-bold text-sm transition">
            🖨 طباعة
          </button>
        </div>
      </div>

      <p v-if="isPrivatePreview"
         class="mb-4 px-4 py-2 rounded-lg bg-yellow-500/10 border border-yellow-500/20 text-yellow-300 text-sm print:hidden">
        🔒 هذه السيرة خاصة، لا يراها غيرك حتى تجعلها عامة.
      </p>

      <!-- بطاقة السيرة -->
      <article class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">

        <!-- الغلاف -->
        <div class="relative h-44 bg-gradient-to-r from-teal-500 via-sky-500 to-indigo-500">
          <img v-if="resume.cover_image" :src="resume.cover_image" class="w-full h-full object-cover" />
        </div>

        <!-- الرأس -->
        <div class="px-8 pb-8 -mt-16 relative">
          <div class="flex items-end gap-6 flex-wrap">
            <div class="w-28 h-28 rounded-full border-4 border-slate-900 bg-slate-800 overflow-hidden flex items-center justify-center text-4xl shadow-xl">
              <img v-if="resume.avatar" :src="resume.avatar" class="w-full h-full object-cover" />
              <span v-else>👤</span>
            </div>
            <div class="flex-1 min-w-0 pb-2">
              <h1 class="text-3xl font-bold mb-1">{{ resume.full_name }}</h1>
              <p v-if="resume.job_title" class="text-teal-400 font-medium text-lg mb-3">
                {{ resume.job_title }}
              </p>
              <div class="flex flex-wrap gap-4 text-sm text-slate-400">
                <span v-if="resume.email">📧 {{ resume.email }}</span>
                <span v-if="resume.phone">📱 {{ resume.phone }}</span>
                <span v-if="resume.location">📍 {{ resume.location }}</span>
                <a v-if="resume.website" :href="resume.website" target="_blank" rel="noopener noreferrer" class="text-sky-400 hover:text-sky-300">
                  🔗 {{ resume.website }}
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- المحتوى -->
        <div class="px-8 pb-8 space-y-10">

          <!-- نبذة -->
          <section v-if="resume.bio">
            <h2 class="text-sm font-bold text-teal-400 ltr:uppercase ltr:tracking-wider mb-3 pb-2 border-b border-slate-800">
              نبذة
            </h2>
            <p class="text-slate-300 leading-relaxed whitespace-pre-line">{{ resume.bio }}</p>
          </section>

          <!-- الصوت -->
          <section v-if="resume.audio_intro">
            <h2 class="text-sm font-bold text-teal-400 ltr:uppercase ltr:tracking-wider mb-3 pb-2 border-b border-slate-800">
              🎤 التعريف الصوتي
            </h2>
            <audio :src="resume.audio_intro" controls class="w-full"></audio>
          </section>

          <!-- الفيديو -->
          <section v-if="resume.video_intro || resume.video_url">
            <h2 class="text-sm font-bold text-teal-400 ltr:uppercase ltr:tracking-wider mb-3 pb-2 border-b border-slate-800">
              🎥 الفيديو التعريفي
            </h2>
            <video v-if="resume.video_intro" :src="resume.video_intro" controls class="w-full rounded-xl"></video>
            <div v-else-if="youtubeId" class="aspect-video rounded-xl overflow-hidden">
              <iframe class="w-full h-full" :src="`https://www.youtube.com/embed/${youtubeId}`"
                      title="الفيديو التعريفي" frameborder="0" allowfullscreen></iframe>
            </div>
            <a v-else :href="resume.video_url" target="_blank" rel="noopener noreferrer"
               class="inline-block px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm">
              مشاهدة الفيديو ↗
            </a>
          </section>

          <!-- الخبرات -->
          <section v-if="resume.experiences?.length">
            <h2 class="text-sm font-bold text-teal-400 ltr:uppercase ltr:tracking-wider mb-4 pb-2 border-b border-slate-800">
              💼 الخبرات
            </h2>
            <div class="relative pe-6 border-e-2 border-slate-800 space-y-6">
              <div v-for="exp in resume.experiences" :key="exp.id" class="relative">
                <div class="absolute -end-[31px] top-2 w-3 h-3 rounded-full bg-teal-400 ring-4 ring-slate-900"></div>
                <h3 class="font-bold text-lg">{{ exp.role }}</h3>
                <p class="text-sm text-slate-400 mb-2">
                  {{ exp.organization }}
                  <span v-if="exp.start_year || exp.end_year">
                    · {{ exp.start_year }} — {{ exp.end_year }}
                  </span>
                </p>
                <p v-if="exp.description" class="text-sm text-slate-300 leading-relaxed whitespace-pre-line">
                  {{ exp.description }}
                </p>
              </div>
            </div>
          </section>

          <!-- المهارات -->
          <section v-if="resume.skills?.length">
            <h2 class="text-sm font-bold text-teal-400 ltr:uppercase ltr:tracking-wider mb-4 pb-2 border-b border-slate-800">
              ⚡ المهارات
            </h2>
            <div class="space-y-3">
              <div v-for="skill in resume.skills" :key="skill.id">
                <div class="flex justify-between text-sm mb-1">
                  <span class="font-medium">{{ skill.name }}</span>
                  <span class="text-slate-500">{{ skill.level }}%</span>
                </div>
                <div class="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-teal-500 to-sky-500 rounded-full transition-all duration-700"
                       :style="{ width: skill.level + '%' }"></div>
                </div>
              </div>
            </div>
          </section>

          <!-- الشهادات -->
          <section v-if="resume.certificates?.length">
            <h2 class="text-sm font-bold text-teal-400 ltr:uppercase ltr:tracking-wider mb-4 pb-2 border-b border-slate-800">
              🏅 الشهادات
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="cert in resume.certificates" :key="cert.id"
                   class="bg-slate-800/50 border border-slate-800 rounded-lg p-4 flex items-start gap-3">
                <span class="text-2xl">🏅</span>
                <div class="flex-1 min-w-0">
                  <h3 class="font-bold text-sm">{{ cert.name }}</h3>
                  <p class="text-xs text-slate-400">
                    {{ cert.issuer }}
                    <span v-if="cert.year"> · {{ cert.year }}</span>
                  </p>
                  <a v-if="cert.verify_url" :href="cert.verify_url" target="_blank" rel="noopener noreferrer"
                     class="text-xs text-sky-400 hover:text-sky-300 mt-1 inline-block">
                    تحقق ↗
                  </a>
                </div>
              </div>
            </div>
          </section>

          <!-- الروابط -->
          <section v-if="resume.links?.length">
            <h2 class="text-sm font-bold text-teal-400 ltr:uppercase ltr:tracking-wider mb-4 pb-2 border-b border-slate-800">
              🔗 روابط
            </h2>
            <div class="flex flex-wrap gap-2">
              <a v-for="link in resume.links" :key="link.id"
                 :href="link.url" target="_blank" rel="noopener noreferrer"
                 class="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm transition">
                {{ link.label }} ↗
              </a>
            </div>
          </section>

        </div>

        <!-- تذييل -->
        <div class="px-8 py-4 border-t border-slate-800 text-center text-xs text-slate-500 print:hidden">
          تم إنشاء هذه السيرة عبر
          <router-link to="/" class="text-teal-400 hover:text-teal-300">CV Studio</router-link>
        </div>

      </article>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { copyText } from '@/utils/clipboard'

const route = useRoute()
const auth = useAuthStore()
const id = route.params.id

const resume = ref(null)
const loading = ref(true)
const error = ref('')
const isPrivatePreview = ref(false) // صاحب السيرة يعاين سيرة خاصة

const youtubeId = computed(() => {
  const url = resume.value?.video_url
  if (!url) return null
  const m = url.match(/(?:youtube\.com\/watch\?(?:.*&)?v=|youtu\.be\/|youtube\.com\/embed\/)([\w-]{11})/)
  return m ? m[1] : null
})

async function loadOwnPrivate() {
  try {
    const { data } = await api.get(`/resumes/${id}/`)
    return data
  } catch {
    return null
  }
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    // المسار العام (بدون توكن). هذا ما يُسجّل المشاهدة في الإحصائيات
    const { data } = await api.get(`/public/resumes/${id}/`)
    resume.value = data
  } catch (err) {
    if (err.response?.status === 404) {
      // قد تكون سيرة خاصة لصاحبها المسجّل
      const own = auth.isAuthenticated ? await loadOwnPrivate() : null
      if (own) {
        resume.value = own
        isPrivatePreview.value = true
      } else {
        error.value = 'السيرة غير موجودة أو غير عامة'
      }
    } else {
      error.value = 'تعذّر تحميل السيرة'
    }
  } finally {
    loading.value = false
  }

  if (resume.value?.full_name) {
    document.title = `${resume.value.full_name} | CV Studio`
  }
}

function print() {
  window.print()
}

async function downloadPDF() {
  if (!isPrivatePreview.value) {
    window.open(`/api/public/resumes/${id}/pdf/`, '_blank')
    return
  }
  // السيرة الخاصة تحتاج توكن، فنجلب الملف عبر axios ثم نحفظه
  try {
    const { data } = await api.get(`/resumes/${id}/pdf/`, { responseType: 'blob' })
    const url = URL.createObjectURL(data)
    const a = document.createElement('a')
    a.href = url
    a.download = `${resume.value.full_name || 'resume'}-CV.pdf`
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  } catch {
    alert('تعذّر تصدير PDF')
  }
}

async function share() {
  const url = window.location.href
  if (navigator.share) {
    try {
      await navigator.share({
        title: resume.value.full_name,
        text: 'سيرتي الذاتية',
        url,
      })
    } catch (e) { /* ألغى المستخدم */ }
    return
  }
  alert((await copyText(url)) ? 'تم نسخ الرابط ✅' : 'تعذّر نسخ الرابط')
}

onMounted(load)
</script>

<style>
@media print {
  body { background: white !important; color: black !important; }
  .print\:hidden { display: none !important; }
  article {
    box-shadow: none !important;
    border: none !important;
    background: white !important;
  }
  article * { color: black !important; }
  article h2 { color: #0d9488 !important; border-color: #e5e7eb !important; }
  .h-2 { background: #e5e7eb !important; }
}
</style>