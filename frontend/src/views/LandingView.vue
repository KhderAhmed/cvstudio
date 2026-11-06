<template>
  <div class="min-h-screen bg-slate-950 text-white" dir="rtl">

    <!-- ===== شريط علوي ===== -->
    <header class="fixed top-0 inset-x-0 z-50 border-b border-slate-800/50 bg-slate-950/80 backdrop-blur-lg">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-400 to-sky-500 flex items-center justify-center text-xl shadow-lg shadow-teal-500/20">
            🎨
          </div>
          <div>
            <h1 class="text-lg font-bold text-white">CV Studio</h1>
            <p class="text-xs text-slate-500 -mt-0.5">سيرتك الحيّة</p>
          </div>
        </div>

        <nav class="flex items-center gap-2">
          <router-link to="/login"
            class="px-4 py-2 text-sm text-slate-300 hover:text-white transition">
            دخول
          </router-link>
          <router-link to="/register"
            class="px-4 py-2 text-sm font-bold rounded-lg bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950 hover:from-teal-400 hover:to-sky-400 transition shadow-lg shadow-teal-500/20">
            ابدأ مجاناً
          </router-link>
        </nav>
      </div>
    </header>

    <!-- ===== Hero ===== -->
    <section class="relative pt-32 pb-20 px-6 overflow-hidden">
      <!-- خلفية -->
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute top-20 right-1/4 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl"></div>
        <div class="absolute top-40 left-1/4 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl"></div>
      </div>

      <div class="relative max-w-7xl mx-auto text-center">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-400 text-xs font-medium mb-6">
          <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
          منصة عربية لبناء السير الذاتية الذكية
        </div>

        <h2 class="text-4xl md:text-6xl font-bold mb-6 leading-tight">
          سيرتك ليست ورقة.
          <br>
          <span class="bg-gradient-to-r from-teal-400 via-sky-400 to-purple-400 bg-clip-text text-transparent">
            إنها تجربة حيّة.
          </span>
        </h2>

        <p class="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          ابنِ سيرتك الذاتية بتصميم احترافي، أضف صوتاً وفيديو،
          وتوافق مع أنظمة التوظيف الذكية (ATS) —
          كل ذلك في رابط واحد.
        </p>

        <div class="flex items-center justify-center gap-4 flex-wrap">
          <router-link to="/register"
            class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950 font-bold text-lg hover:from-teal-400 hover:to-sky-400 transition shadow-xl shadow-teal-500/30">
            ابدأ مجاناً →
          </router-link>
          <router-link to="/login"
            class="px-8 py-3.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-white font-bold text-lg transition">
            جرّب الآن
          </router-link>
        </div>

        <p class="text-xs text-slate-600 mt-6">
          ✅ بدون بطاقة ائتمانية  ·  ✅ مجاني تماماً  ·  ✅ بالعربية
        </p>
      </div>
    </section>

    <!-- ===== الميزات ===== -->
    <section class="px-6 py-20 border-t border-slate-800/50">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-14">
          <h3 class="text-3xl md:text-4xl font-bold mb-4">
            كل ما تحتاجه في مكان واحد
          </h3>
          <p class="text-slate-400 max-w-2xl mx-auto">
            أدوات متكاملة تساعدك على بناء سيرة ذاتية احترافية تُحدث فرقاً حقيقياً
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="feature in features" :key="feature.title"
            class="group bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-teal-500/50 transition-all hover:-translate-y-1">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-teal-500/20 to-sky-500/20 border border-teal-500/30 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition">
              {{ feature.icon }}
            </div>
            <h4 class="text-lg font-bold mb-2">{{ feature.title }}</h4>
            <p class="text-sm text-slate-400 leading-relaxed">{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== كيف يعمل ===== -->
    <section class="px-6 py-20 border-t border-slate-800/50 bg-slate-900/30">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-14">
          <h3 class="text-3xl md:text-4xl font-bold mb-4">كيف يعمل؟</h3>
          <p class="text-slate-400">ثلاث خطوات بسيطة</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="(step, i) in steps" :key="i"
            class="relative text-center">
            <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-teal-500 to-sky-500 flex items-center justify-center text-2xl font-bold text-slate-950 shadow-xl shadow-teal-500/30">
              {{ i + 1 }}
            </div>
            <h4 class="text-lg font-bold mb-2">{{ step.title }}</h4>
            <p class="text-sm text-slate-400">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== الأرقام ===== -->
    <section class="px-6 py-16 border-t border-slate-800/50">
      <div class="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
        <div v-for="stat in stats" :key="stat.label">
          <p class="text-3xl md:text-4xl font-bold bg-gradient-to-r from-teal-400 to-sky-400 bg-clip-text text-transparent">
            {{ stat.value }}
          </p>
          <p class="text-sm text-slate-500 mt-1">{{ stat.label }}</p>
        </div>
      </div>
    </section>

    <!-- ===== CTA ===== -->
    <section class="px-6 py-20 border-t border-slate-800/50">
      <div class="max-w-4xl mx-auto text-center bg-gradient-to-br from-slate-900 to-slate-900/50 border border-teal-500/20 rounded-3xl p-12 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-br from-teal-500/5 to-sky-500/5"></div>
        <div class="relative">
          <h3 class="text-3xl md:text-4xl font-bold mb-4">
            جاهز لبناء سيرتك؟
          </h3>
          <p class="text-slate-400 mb-8 max-w-xl mx-auto">
            انضم إلى من يستخدمون CV Studio لبناء سير ذاتية احترافية تفتح لهم أبواب الفرص.
          </p>
          <router-link to="/register"
            class="inline-block px-10 py-4 rounded-xl bg-gradient-to-r from-teal-500 to-sky-500 text-slate-950 font-bold text-lg hover:from-teal-400 hover:to-sky-400 transition shadow-2xl shadow-teal-500/30">
            ابدأ مجاناً الآن →
          </router-link>
        </div>
      </div>
    </section>

    <!-- ===== تذييل ===== -->
    <footer class="border-t border-slate-800/50 px-6 py-8">
      <div class="max-w-7xl mx-auto flex items-center justify-between flex-wrap gap-4">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-400 to-sky-500 flex items-center justify-center text-sm">
            🎨
          </div>
          <span class="text-sm text-slate-400">© {{ new Date().getFullYear() }} CV Studio</span>
        </div>
        <div class="flex items-center gap-6 text-sm text-slate-500">
          <a href="#" class="hover:text-teal-400 transition">الخصوصية</a>
          <a href="#" class="hover:text-teal-400 transition">الشروط</a>
          <a href="#" class="hover:text-teal-400 transition">تواصل</a>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
const features = [
  {
    icon: '📄',
    title: 'سيرة ذاتية حيّة',
    desc: 'لا مجرد PDF جامد — صفحة ويب تفاعلية تُحدَّث لحظياً وتُشارك برابط واحد.',
  },
  {
    icon: '🎙️',
    title: 'تحويل النص لصوت',
    desc: 'أضف تعریفاً صوتياً لسيرتك. دع صاحب العمل يسمعك، لا يقرؤك فقط.',
  },
  {
    icon: '🎥',
    title: 'فيديو تعريفي',
    desc: 'ارفع فيديو قصيراً يعرّف بك، أو أضف رابط يوتيوب. فرصك تتضاعف.',
  },
  {
    icon: '🎯',
    title: 'تحليل ATS',
    desc: 'احسب درجة توافق سيرتك مع الوظيفة قبل التقديم. أضف الكلمات المفتاحية المفقودة.',
  },
  {
    icon: '📑',
    title: 'تصدير PDF احترافي',
    desc: 'حمّل سيرتك كـ PDF نصي متوافق مع أنظمة التوظيف الذكية (ATS-Friendly).',
  },
  {
    icon: '🔗',
    title: 'رابط واحد لكل شيء',
    desc: 'شارك رابط سيرتك على LinkedIn، في البريد، أو في السيرة نفسها.',
  },
]

const steps = [
  { title: 'سجّل حسابك', desc: 'أقل من دقيقة، بدون بطاقة ائتمانية' },
  { title: 'املأ بياناتك', desc: 'خبرات، مهارات، شهادات، وصوتك' },
  { title: 'شارك سيرتك', desc: 'رابط دائم + PDF جاهز للتقديم' },
]

const stats = [
  { value: '100%', label: 'مجاني' },
  { value: 'ATS', label: 'متوافق' },
  { value: '🎙️', label: 'صوت + فيديو' },
  { value: '∞', label: 'تحديثات' },
]
</script>