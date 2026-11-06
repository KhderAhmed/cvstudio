<template>
  <div class="min-h-screen bg-slate-950 text-white" dir="rtl">

    <!-- الشريط العلوي -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button
            @click="$router.push('/dashboard')"
            class="text-slate-400 hover:text-white transition"
          >
            ← رجوع
          </button>
          <h1 class="text-lg font-bold">إنشاء سيرة جديدة</h1>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-6 py-8">

      <form @submit.prevent="handleSubmit" class="space-y-6">

        <!-- البيانات الأساسية -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 class="text-base font-semibold text-teal-400 mb-4">البيانات الأساسية</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div class="md:col-span-2">
              <label class="block text-sm text-slate-400 mb-1.5">الاسم الكامل *</label>
              <input
                v-model="form.full_name"
                type="text"
                required
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
                placeholder="أحمد محمد"
              />
            </div>

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">المسمى الوظيفي</label>
              <input
                v-model="form.job_title"
                type="text"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
                placeholder="مطور ويب"
              />
            </div>

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">عنوان السيرة</label>
              <input
                v-model="form.title"
                type="text"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
                placeholder="سيرتي الذاتية"
              />
            </div>

            <div class="md:col-span-2">
              <label class="block text-sm text-slate-400 mb-1.5">نبذة تعريفية</label>
              <textarea
                v-model="form.bio"
                rows="4"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition resize-vertical"
                placeholder="اكتب نبذة قصيرة عنك…"
              ></textarea>
            </div>

          </div>
        </div>

        <!-- التواصل -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 class="text-base font-semibold text-teal-400 mb-4">معلومات التواصل</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">البريد الإلكتروني</label>
              <input
                v-model="form.email"
                type="email"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
                placeholder="you@mail.com"
              />
            </div>

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">الهاتف</label>
              <input
                v-model="form.phone"
                type="tel"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
                placeholder="+966..."
              />
            </div>

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">المدينة</label>
              <input
                v-model="form.location"
                type="text"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
                placeholder="الرياض"
              />
            </div>

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">الموقع</label>
              <input
                v-model="form.website"
                type="url"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
                placeholder="https://..."
              />
            </div>

          </div>
        </div>

        <!-- التصميم واللغة -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 class="text-base font-semibold text-teal-400 mb-4">التصميم واللغة</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">القالب</label>
              <select
                v-model="form.template"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
              >
                <option value="classic">كلاسيكي</option>
                <option value="modern">حديث</option>
                <option value="minimal">بسيط</option>
              </select>
            </div>

            <div>
              <label class="block text-sm text-slate-400 mb-1.5">اللغة</label>
              <select
                v-model="form.language"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none transition"
              >
                <option value="ar">العربية</option>
                <option value="en">English</option>
              </select>
            </div>

            <div class="md:col-span-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  v-model="form.is_public"
                  type="checkbox"
                  class="w-4 h-4 rounded accent-teal-500"
                />
                <span class="text-sm text-slate-300">السيرة عامة (يمكن لأي شخص مشاهدتها)</span>
              </label>
            </div>

          </div>
        </div>

        <!-- خطأ -->
        <div
          v-if="error"
          class="bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3 text-red-400 text-sm"
        >
          {{ error }}
        </div>

        <!-- الأزرار -->
        <div class="flex gap-3">
          <button
            type="button"
            @click="$router.push('/dashboard')"
            class="px-5 py-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium transition"
          >
            إلغاء
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 px-5 py-2.5 rounded-lg bg-gradient-to-r from-teal-500 to-sky-500 hover:from-teal-400 hover:to-sky-400 text-slate-950 font-bold transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'جاري الحفظ…' : 'حفظ السيرة' }}
          </button>
        </div>

      </form>

    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/client'
import { apiError } from '@/api/errors'

const router = useRouter()

const form = ref({
  full_name: '',
  job_title: '',
  title: 'سيرتي الذاتية',
  bio: '',
  email: '',
  phone: '',
  location: '',
  website: '',
  template: 'modern',
  language: 'ar',
  is_public: true,
})

const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    await api.post('/resumes/', form.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = apiError(err, 'تعذّر حفظ السيرة')
  } finally {
    loading.value = false
  }
}
</script>