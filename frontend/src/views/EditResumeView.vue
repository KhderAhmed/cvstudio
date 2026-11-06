<template>
  <div class="min-h-screen bg-slate-950 text-white" dir="rtl">

    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="$router.push('/dashboard')" class="text-slate-400 hover:text-white transition">
            ← رجوع
          </button>
          <h1 class="text-lg font-bold">تحرير السيرة</h1>
        </div>
        <router-link :to="`/cv/${id}`"
          class="text-sm text-teal-400 hover:text-teal-300 transition">
          👁 معاينة
        </router-link>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 py-8" v-if="resume">

      <!-- تبويبات -->
      <div class="flex gap-2 mb-6 bg-slate-900 border border-slate-800 rounded-xl p-1.5 overflow-x-auto">
        <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
          class="px-4 py-2 rounded-lg text-sm font-bold whitespace-nowrap transition" :class="activeTab === tab.id
            ? 'bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950'
            : 'text-slate-400 hover:text-white'">
          {{ tab.icon }} {{ tab.label }}
        </button>
      </div>

      <!-- البيانات الأساسية -->
      <div v-if="activeTab === 'basic'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 class="text-base font-semibold text-teal-400 mb-4">البيانات الأساسية</h2>
        <form @submit.prevent="saveBasic" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="block text-sm text-slate-400 mb-1.5">الاسم الكامل *</label>
              <input v-model="resume.full_name" type="text" required
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">المسمى الوظيفي</label>
              <input v-model="resume.job_title" type="text"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">عنوان السيرة</label>
              <input v-model="resume.title" type="text"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm text-slate-400 mb-1.5">نبذة</label>
              <textarea v-model="resume.bio" rows="4"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none resize-vertical"></textarea>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">البريد</label>
              <input v-model="resume.email" type="email"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">الهاتف</label>
              <input v-model="resume.phone" type="tel"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">المدينة</label>
              <input v-model="resume.location" type="text"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">الموقع</label>
              <input v-model="resume.website" type="url"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">القالب</label>
              <select v-model="resume.template"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none">
                <option value="classic">كلاسيكي</option>
                <option value="modern">حديث</option>
                <option value="minimal">بسيط</option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1.5">اللغة</label>
              <select v-model="resume.language"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none">
                <option value="ar">العربية</option>
                <option value="en">English</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input v-model="resume.is_public" type="checkbox" class="w-4 h-4 rounded accent-teal-500" />
                <span class="text-sm text-slate-300">السيرة عامة</span>
              </label>
            </div>
          </div>
          <button type="submit" :disabled="saving"
            class="px-6 py-2.5 rounded-lg bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950 font-bold transition disabled:opacity-50">
            {{ saving ? 'جاري الحفظ…' : 'حفظ التغييرات' }}
          </button>
        </form>
      </div>

      <!-- الوسائط -->
      <div v-if="activeTab === 'media'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 class="text-base font-semibold text-teal-400 mb-4">الصور والوسائط</h2>

        <div class="space-y-6">

          <!-- الصورة الشخصية -->
          <div>
            <label class="block text-sm text-slate-400 mb-2">الصورة الشخصية</label>
            <div class="flex items-center gap-4">
              <div class="w-20 h-20 rounded-full bg-slate-800 border border-slate-700 overflow-hidden flex items-center justify-center text-2xl">
                <img v-if="resume.avatar" :src="resume.avatar" class="w-full h-full object-cover" />
                <span v-else>👤</span>
              </div>
              <div class="flex-1">
                <input type="file" accept="image/*" @change="uploadFile($event, 'avatar')"
                  class="block w-full text-sm text-slate-400 file:me-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-teal-500/10 file:text-teal-400 hover:file:bg-teal-500/20 file:cursor-pointer" />
                <p class="text-xs text-slate-500 mt-1">JPG أو PNG · الحد الأقصى 5MB</p>
              </div>
            </div>
          </div>

          <!-- صورة الغلاف -->
          <div>
            <label class="block text-sm text-slate-400 mb-2">صورة الغلاف</label>
            <div class="w-full h-32 rounded-lg bg-slate-800 border border-slate-700 overflow-hidden mb-2">
              <img v-if="resume.cover_image" :src="resume.cover_image" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-slate-500 text-sm">لا توجد صورة غلاف</div>
            </div>
            <input type="file" accept="image/*" @change="uploadFile($event, 'cover_image')"
              class="block w-full text-sm text-slate-400 file:me-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-teal-500/10 file:text-teal-400 hover:file:bg-teal-500/20 file:cursor-pointer" />
          </div>

          <!-- توليد صوت من النص -->
          <div class="p-4 bg-slate-800/50 border border-teal-500/30 rounded-lg">
            <h3 class="text-sm font-bold text-teal-400 mb-3">🎙️ توليد صوت من نص</h3>

            <div class="space-y-3">
              <textarea v-model="ttsText" rows="4" placeholder="الصق النص هنا… (عربي أو إنجليزي)"
                class="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none resize-vertical"></textarea>

              <div class="flex gap-2 flex-wrap">
                <button @click="generateTTS(false)" :disabled="!ttsText || generatingTTS"
                  class="px-4 py-2 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-sm transition disabled:opacity-50">
                  {{ generatingTTS ? '⏳ جاري التوليد…' : '🔊 توليد من النص' }}
                </button>

                <button @click="generateTTS(true)" :disabled="generatingTTS || !resume.bio"
                  class="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-sm transition disabled:opacity-50">
                  📝 استخدام النبذة
                </button>

                <button v-if="resume.audio_intro" @click="deleteAudio" :disabled="generatingTTS"
                  class="px-4 py-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 text-red-400 text-sm transition disabled:opacity-50">
                  🗑 حذف الصوت
                </button>
              </div>

              <p v-if="ttsMessage" class="text-xs text-teal-400">{{ ttsMessage }}</p>
            </div>
          </div>

          <!-- الصوت -->
          <div>
            <label class="block text-sm text-slate-400 mb-2">🎤 التعريف الصوتي</label>
            <audio v-if="resume.audio_intro" :src="resume.audio_intro" controls class="w-full mb-2"></audio>
            <input type="file" accept="audio/*" @change="uploadFile($event, 'audio_intro')"
              class="block w-full text-sm text-slate-400 file:me-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-teal-500/10 file:text-teal-400 hover:file:bg-teal-500/20 file:cursor-pointer" />
            <p class="text-xs text-slate-500 mt-1">MP3 أو WAV · الحد الأقصى 20MB</p>
          </div>

          <!-- الفيديو -->
          <div>
            <label class="block text-sm text-slate-400 mb-2">🎥 الفيديو التعريفي</label>
            <video v-if="resume.video_intro" :src="resume.video_intro" controls class="w-full mb-2 rounded-lg"></video>
            <input type="file" accept="video/*" @change="uploadFile($event, 'video_intro')"
              class="block w-full text-sm text-slate-400 file:me-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-teal-500/10 file:text-teal-400 hover:file:bg-teal-500/20 file:cursor-pointer" />
            <p class="text-xs text-slate-500 mt-1">MP4 · الحد الأقصى 50MB</p>

            <div class="mt-3">
              <label class="block text-sm text-slate-400 mb-1">أو رابط يوتيوب</label>
              <input v-model="resume.video_url" type="url" placeholder="https://youtube.com/watch?v=..."
                @blur="saveBasic"
                class="w-full px-4 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-white focus:border-teal-500 focus:outline-none" />
            </div>
          </div>

        </div>

        <!-- مؤشر الرفع -->
        <div v-if="uploading" class="mt-4 px-4 py-3 rounded-lg bg-teal-500/10 border border-teal-500/20 text-teal-400 text-sm">
          ⏳ جاري رفع {{ uploading }}… {{ uploadProgress }}%
        </div>

      </div>

      <!-- الخبرات -->
      <div v-if="activeTab === 'exp'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-base font-semibold text-teal-400">الخبرات</h2>
          <button @click="addExperience"
            class="px-3 py-1.5 rounded-lg bg-teal-500/10 text-teal-400 hover:bg-teal-500/20 text-sm font-medium transition">
            + إضافة
          </button>
        </div>

        <div v-if="experiences.length === 0" class="text-center py-8 text-slate-500 text-sm">
          لا توجد خبرات بعد
        </div>

        <div v-for="(exp, i) in experiences" :key="exp.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4 mb-3">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs text-slate-500">خبرة {{ i + 1 }}</span>
            <button @click="deleteExperience(exp.id)" class="text-red-400 hover:text-red-300 text-sm">✕</button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <input v-model="exp.role" type="text" placeholder="المسمى الوظيفي" @blur="updateExperience(exp)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <input v-model="exp.organization" type="text" placeholder="الجهة" @blur="updateExperience(exp)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <input v-model="exp.start_year" type="text" placeholder="من سنة" @blur="updateExperience(exp)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <input v-model="exp.end_year" type="text" placeholder="إلى سنة (أو الآن)" @blur="updateExperience(exp)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <textarea v-model="exp.description" rows="2" placeholder="الوصف" @blur="updateExperience(exp)"
              class="md:col-span-2 px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none resize-vertical"></textarea>
          </div>
        </div>
      </div>

      <!-- المهارات -->
      <div v-if="activeTab === 'skills'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-base font-semibold text-teal-400">المهارات</h2>
          <button @click="addSkill"
            class="px-3 py-1.5 rounded-lg bg-teal-500/10 text-teal-400 hover:bg-teal-500/20 text-sm font-medium transition">
            + إضافة
          </button>
        </div>

        <div v-if="skills.length === 0" class="text-center py-8 text-slate-500 text-sm">
          لا توجد مهارات بعد
        </div>

        <div v-for="(skill, i) in skills" :key="skill.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4 mb-3">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs text-slate-500">مهارة {{ i + 1 }}</span>
            <button @click="deleteSkill(skill.id)" class="text-red-400 hover:text-red-300 text-sm">✕</button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <input v-model="skill.name" type="text" placeholder="اسم المهارة" @blur="updateSkill(skill)"
              class="md:col-span-2 px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <input v-model.number="skill.level" type="number" min="0" max="100" placeholder="المستوى %" @blur="updateSkill(skill)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
          </div>
        </div>
      </div>

      <!-- الشهادات -->
      <div v-if="activeTab === 'certs'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-base font-semibold text-teal-400">الشهادات</h2>
          <button @click="addCertificate"
            class="px-3 py-1.5 rounded-lg bg-teal-500/10 text-teal-400 hover:bg-teal-500/20 text-sm font-medium transition">
            + إضافة
          </button>
        </div>

        <div v-if="certificates.length === 0" class="text-center py-8 text-slate-500 text-sm">
          لا توجد شهادات بعد
        </div>

        <div v-for="(cert, i) in certificates" :key="cert.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4 mb-3">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs text-slate-500">شهادة {{ i + 1 }}</span>
            <button @click="deleteCertificate(cert.id)" class="text-red-400 hover:text-red-300 text-sm">✕</button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <input v-model="cert.name" type="text" placeholder="اسم الشهادة" @blur="updateCertificate(cert)"
              class="md:col-span-2 px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <input v-model="cert.issuer" type="text" placeholder="الجهة المانحة" @blur="updateCertificate(cert)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <input v-model="cert.year" type="text" placeholder="السنة" @blur="updateCertificate(cert)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
          </div>
        </div>
      </div>

      <!-- الروابط -->
      <div v-if="activeTab === 'links'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-base font-semibold text-teal-400">الروابط</h2>
          <button @click="addLink"
            class="px-3 py-1.5 rounded-lg bg-teal-500/10 text-teal-400 hover:bg-teal-500/20 text-sm font-medium transition">
            + إضافة
          </button>
        </div>

        <div v-if="links.length === 0" class="text-center py-8 text-slate-500 text-sm">
          لا توجد روابط بعد
        </div>

        <div v-for="(link, i) in links" :key="link.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4 mb-3">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs text-slate-500">رابط {{ i + 1 }}</span>
            <button @click="deleteLink(link.id)" class="text-red-400 hover:text-red-300 text-sm">✕</button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <input v-model="link.label" type="text" placeholder="التسمية (مثل GitHub)" @blur="updateLink(link)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
            <input v-model="link.url" type="url" placeholder="https://..." @blur="updateLink(link)"
              class="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none" />
          </div>
        </div>
      </div>

      <!-- ATS Score -->
      <div v-if="activeTab === 'ats'" class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 class="text-base font-semibold text-teal-400 mb-4">🎯 تحليل ATS</h2>

        <p class="text-sm text-slate-400 mb-4">
          الصق الوصف الوظيفي (Job Description) وسنحسب درجة توافق سيرتك معه.
        </p>

        <textarea
          v-model="jobDescription"
          rows="8"
          placeholder="الصق الوصف الوظيفي هنا…&#10;&#10;مثال:&#10;We are looking for a Python Developer with experience in Django, REST APIs, PostgreSQL…"
          class="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white text-sm focus:border-teal-500 focus:outline-none resize-vertical mb-3"
        ></textarea>

        <button
          @click="analyzeATS"
          :disabled="!jobDescription || analyzingATS"
          class="px-6 py-2.5 rounded-lg bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950 font-bold text-sm transition disabled:opacity-50"
        >
          {{ analyzingATS ? '⏳ جاري التحليل…' : '🎯 تحليل السيرة' }}
        </button>

        <!-- النتيجة -->
        <div v-if="atsResult" class="mt-6 space-y-4">

          <!-- الدرجة -->
          <div class="text-center p-6 rounded-lg" :class="scoreColor">
            <p class="text-sm text-slate-400 mb-1">درجة التوافق</p>
            <p class="text-5xl font-bold">{{ atsResult.score }}<span class="text-2xl text-slate-500">/100</span></p>
            <p class="text-sm mt-2">{{ scoreLabel }}</p>
          </div>

          <!-- الكلمات المطابقة -->
          <div v-if="atsResult.matched_keywords?.length" class="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
            <h3 class="text-sm font-bold text-green-400 mb-2">
              ✅ كلمات مطابقة ({{ atsResult.matched_count }})
            </h3>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="kw in atsResult.matched_keywords" :key="kw"
                class="px-2 py-1 bg-green-500/20 text-green-300 rounded text-xs">
                {{ kw }}
              </span>
            </div>
          </div>

          <!-- الكلمات المفقودة -->
          <div v-if="atsResult.missing_keywords?.length" class="p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
            <h3 class="text-sm font-bold text-red-400 mb-2">
              ❌ كلمات مفقودة ({{ atsResult.missing_count }})
            </h3>
            <p class="text-xs text-slate-400 mb-2">أضف هذه الكلمات إلى سيرتك:</p>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="kw in atsResult.missing_keywords" :key="kw"
                class="px-2 py-1 bg-red-500/20 text-red-300 rounded text-xs">
                {{ kw }}
              </span>
            </div>
          </div>

          <!-- الاقتراحات -->
          <div v-if="atsResult.tips?.length" class="p-4 bg-sky-500/10 border border-sky-500/20 rounded-lg">
            <h3 class="text-sm font-bold text-sky-400 mb-2">💡 اقتراحات</h3>
            <ul class="text-sm text-slate-300 space-y-1">
              <li v-for="(tip, i) in atsResult.tips" :key="i">• {{ tip }}</li>
            </ul>
          </div>

        </div>
      </div>

      <!-- رسالة -->
      <div v-if="message" class="mt-4 px-4 py-3 rounded-lg text-sm" :class="messageType === 'error'
        ? 'bg-red-500/10 border border-red-500/20 text-red-400'
        : 'bg-green-500/10 border border-green-500/20 text-green-400'">
        {{ message }}
      </div>

    </main>

    <div v-else-if="loadError" class="text-center py-20">
      <p class="text-4xl mb-3">⚠️</p>
      <p class="text-slate-300 mb-4">{{ loadError }}</p>
      <button @click="$router.push('/dashboard')"
        class="px-5 py-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-medium transition">
        العودة للوحة التحكم
      </button>
    </div>

    <div v-else class="text-center py-20 text-slate-500">
      <div class="inline-block w-8 h-8 border-2 border-slate-700 border-t-teal-400 rounded-full animate-spin mb-3"></div>
      <p>جاري التحميل…</p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/client'
import { apiError } from '@/api/errors'

const route = useRoute()
const id = route.params.id

const resume = ref(null)
const experiences = ref([])
const skills = ref([])
const certificates = ref([])
const links = ref([])

const activeTab = ref('basic')
const saving = ref(false)
const uploading = ref('')
const uploadProgress = ref(0)
const loadError = ref('')
const message = ref('')
const messageType = ref('success')

// الحدود متوافقة مع إعدادات الخادم (50MB كحد أقصى للطلب)
const UPLOAD_LIMITS = {
  avatar: { label: 'الصورة الشخصية', maxMB: 5 },
  cover_image: { label: 'صورة الغلاف', maxMB: 5 },
  audio_intro: { label: 'الصوت', maxMB: 20 },
  video_intro: { label: 'الفيديو', maxMB: 50 },
}

// TTS
const ttsText = ref('')
const generatingTTS = ref(false)
const ttsMessage = ref('')

// ATS
const jobDescription = ref('')
const analyzingATS = ref(false)
const atsResult = ref(null)

const scoreColor = computed(() => {
  const s = atsResult.value?.score || 0
  if (s >= 80) return 'bg-green-500/10 border border-green-500/30'
  if (s >= 60) return 'bg-sky-500/10 border border-sky-500/30'
  if (s >= 40) return 'bg-yellow-500/10 border border-yellow-500/30'
  return 'bg-red-500/10 border border-red-500/30'
})

const scoreLabel = computed(() => {
  const s = atsResult.value?.score || 0
  if (s >= 80) return '🎉 ممتاز — سيرتك متوافقة جداً'
  if (s >= 60) return '👍 جيدة — تحتاج تحسيناً بسيطاً'
  if (s >= 40) return '⚠️ متوسطة — أضف كلمات مفتاحية'
  return '🔴 ضعيفة — راجع سيرتك'
})

const tabs = [
  { id: 'basic', label: 'الأساسية', icon: '👤' },
  { id: 'media', label: 'الوسائط', icon: '🎬' },
  { id: 'exp', label: 'الخبرات', icon: '💼' },
  { id: 'skills', label: 'المهارات', icon: '⚡' },
  { id: 'certs', label: 'الشهادات', icon: '🏅' },
  { id: 'links', label: 'الروابط', icon: '🔗' },
  { id: 'ats', label: 'ATS', icon: '🎯' },
]

let msgTimer = null
function showMsg(msg, type = 'success') {
  message.value = msg
  messageType.value = type
  clearTimeout(msgTimer)
  msgTimer = setTimeout(() => { message.value = '' }, 4000)
}
onBeforeUnmount(() => clearTimeout(msgTimer))

async function load() {
  try {
    const { data } = await api.get(`/resumes/${id}/`)
    resume.value = data
    experiences.value = data.experiences || []
    skills.value = data.skills || []
    certificates.value = data.certificates || []
    links.value = data.links || []
  } catch (err) {
    console.error('LOAD ERROR:', err.response?.data)
    loadError.value = err.response?.status === 404
      ? 'السيرة غير موجودة'
      : 'تعذّر تحميل السيرة'
  }
}

async function saveBasic() {
  saving.value = true
  try {
    const payload = {
      title: resume.value.title,
      full_name: resume.value.full_name,
      job_title: resume.value.job_title,
      bio: resume.value.bio,
      email: resume.value.email,
      phone: resume.value.phone,
      location: resume.value.location,
      website: resume.value.website,
      template: resume.value.template,
      language: resume.value.language,
      is_public: resume.value.is_public,
      video_url: resume.value.video_url || '',
    }
    await api.patch(`/resumes/${id}/`, payload)
    showMsg('تم الحفظ ✅')
  } catch (err) {
    console.error('SAVE ERROR:', err.response?.data)
    showMsg('تعذّر الحفظ: ' + apiError(err), 'error')
  } finally {
    saving.value = false
  }
}

async function uploadFile(event, fieldName) {
  const file = event.target.files[0]
  if (!file) return

  const cfg = UPLOAD_LIMITS[fieldName]
  if (file.size > cfg.maxMB * 1024 * 1024) {
    showMsg(`حجم ${cfg.label} أكبر من ${cfg.maxMB}MB`, 'error')
    event.target.value = ''
    return
  }

  uploading.value = cfg.label
  uploadProgress.value = 0

  const formData = new FormData()
  formData.append(fieldName, file)

  try {
    // الترويسة صريحة لأن العميل الافتراضي JSON، ولولاها يتحول FormData إلى JSON
    const { data } = await api.patch(`/resumes/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        if (e.total) uploadProgress.value = Math.round((e.loaded / e.total) * 100)
      },
    })
    // نحدّث الحقل المرفوع فقط حتى لا نمسح تعديلات لم تُحفظ بعد في باقي الحقول
    resume.value[fieldName] = data[fieldName]
    showMsg('تم رفع الملف ✅')
  } catch (err) {
    console.error('UPLOAD ERROR:', err.response?.data)
    showMsg(
      err.response?.status === 413
        ? 'الملف أكبر من الحد المسموح'
        : 'تعذّر الرفع: ' + apiError(err),
      'error'
    )
  } finally {
    uploading.value = ''
    event.target.value = ''
  }
}

// ============ TTS ============
async function generateTTS(useBio) {
  if (!useBio && !ttsText.value.trim()) {
    showMsg('اكتب نصاً أولاً', 'error')
    return
  }
  if (useBio && !resume.value?.bio) {
    showMsg('النبذة فارغة', 'error')
    return
  }
  generatingTTS.value = true
  ttsMessage.value = ''
  try {
    const { data } = await api.post(`/resumes/${id}/tts/`, {
      text: useBio ? '' : ttsText.value,
      use_bio: useBio,
    })
    resume.value.audio_intro = data.audio_url
    ttsMessage.value = `✅ تم توليد ${data.characters} حرفاً`
    showMsg('تم توليد الصوت ✅')
  } catch (err) {
    console.error('TTS ERROR:', err.response?.data)
    showMsg('تعذّر توليد الصوت: ' + apiError(err), 'error')
  } finally {
    generatingTTS.value = false
  }
}

async function deleteAudio() {
  if (!confirm('حذف الملف الصوتي؟')) return
  try {
    await api.patch(`/resumes/${id}/`, { audio_intro: null })
    resume.value.audio_intro = null
    showMsg('تم حذف الصوت', 'success')
  } catch (err) {
    showMsg('تعذّر الحذف: ' + apiError(err), 'error')
  }
}

// ============ ATS ============
async function analyzeATS() {
  if (!jobDescription.value.trim()) {
    showMsg('الصق الوصف الوظيفي أولاً', 'error')
    return
  }
  analyzingATS.value = true
  atsResult.value = null
  try {
    const { data } = await api.post(`/resumes/${id}/ats/`, {
      job_description: jobDescription.value,
    })
    if (data.error) {
      // الخادم يرجع 200 مع error عندما لا يجد كلمات مفتاحية في الوصف
      showMsg(data.error, 'error')
      return
    }
    atsResult.value = data
    showMsg('تم التحليل ✅')
  } catch (err) {
    console.error('ATS ERROR:', err.response?.status, err.response?.data)
    showMsg('تعذّر التحليل: ' + apiError(err), 'error')
  } finally {
    analyzingATS.value = false
  }
}

// ============ عناصر السيرة (خبرات / مهارات / شهادات / روابط) ============
async function addItem(endpoint, list, payload) {
  if (!resume.value?.id) {
    showMsg('السيرة لم تُحمّل بعد', 'error')
    return
  }
  try {
    const { data } = await api.post(endpoint, {
      resume: Number(resume.value.id),
      order: list.value.length, // ترتيب ثابت للعناصر الجديدة
      ...payload,
    })
    list.value.push(data)
    showMsg('تمت الإضافة ✅')
  } catch (err) {
    console.error('ADD ERROR:', endpoint, err.response?.status, err.response?.data)
    showMsg('تعذّرت الإضافة: ' + apiError(err), 'error')
  }
}

async function updateItem(endpoint, item, fields) {
  try {
    const payload = Object.fromEntries(fields.map((f) => [f, item[f]]))
    await api.patch(`${endpoint}${item.id}/`, payload)
  } catch (err) {
    console.error('UPDATE ERROR:', endpoint, err.response?.data)
    showMsg('تعذّر التحديث: ' + apiError(err), 'error')
  }
}

async function deleteItem(endpoint, list, itemId, question) {
  if (!confirm(question)) return
  try {
    await api.delete(`${endpoint}${itemId}/`)
    list.value = list.value.filter((x) => x.id !== itemId)
    showMsg('تم الحذف', 'success')
  } catch (err) {
    showMsg('تعذّر الحذف: ' + apiError(err), 'error')
  }
}

const addExperience = () => addItem('/experiences/', experiences, {
  role: 'خبرة جديدة', organization: '', start_year: '', end_year: '', description: '',
})
const updateExperience = (exp) => updateItem('/experiences/', exp,
  ['role', 'organization', 'start_year', 'end_year', 'description'])
const deleteExperience = (eid) => deleteItem('/experiences/', experiences, eid, 'حذف هذه الخبرة؟')

const addSkill = () => addItem('/skills/', skills, { name: 'مهارة جديدة', level: 80 })
const updateSkill = (skill) => updateItem('/skills/', skill, ['name', 'level'])
const deleteSkill = (sid) => deleteItem('/skills/', skills, sid, 'حذف هذه المهارة؟')

const addCertificate = () => addItem('/certificates/', certificates, {
  name: 'شهادة جديدة', issuer: '', year: '',
})
const updateCertificate = (cert) => updateItem('/certificates/', cert, ['name', 'issuer', 'year'])
const deleteCertificate = (cid) => deleteItem('/certificates/', certificates, cid, 'حذف هذه الشهادة؟')

const addLink = () => addItem('/links/', links, { label: 'رابط جديد', url: 'https://example.com' })
const updateLink = (link) => updateItem('/links/', link, ['label', 'url'])
const deleteLink = (lid) => deleteItem('/links/', links, lid, 'حذف هذا الرابط؟')

onMounted(load)
</script>