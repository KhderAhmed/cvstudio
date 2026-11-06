import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const APP_NAME = 'CV Studio'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('@/views/LandingView.vue'),
      meta: { guest: true, title: APP_NAME },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { guest: true, title: 'تسجيل الدخول' },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { guest: true, title: 'تسجيل جديد' },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true, title: 'لوحة التحكم' },
    },
    {
      path: '/dashboard/new',
      name: 'resume-create',
      component: () => import('@/views/CreateResumeView.vue'),
      meta: { requiresAuth: true, title: 'سيرة جديدة' },
    },
    {
      path: '/dashboard/edit/:id',
      name: 'resume-edit',
      component: () => import('@/views/EditResumeView.vue'),
      meta: { requiresAuth: true, title: 'تحرير السيرة' },
    },
    {
      path: '/dashboard/analytics',
      name: 'analytics',
      component: () => import('@/views/AnalyticsView.vue'),
      meta: { requiresAuth: true, title: 'الإحصائيات' },
    },
    {
      // صفحة عامة: العنوان يحدده PublicResumeView باسم صاحب السيرة
      path: '/cv/:id',
      name: 'resume-public',
      component: () => import('@/views/PublicResumeView.vue'),
    },
    {
      // ملاحظة: لوحة إدارة Django موجودة على /django-admin/ حتى لا تتعارض مع هذا المسار
      path: '/admin',
      alias: '/admin/',
      name: 'admin-dashboard',
      component: () => import('@/views/AdminDashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, title: 'الإدارة' },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
      meta: { title: 'الصفحة غير موجودة' },
    },
  ],
})

// حماية المسارات
router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.guest && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }

  // تحقق من الصلاحيات
  if (to.meta.requiresAdmin) {
    if (!auth.user) {
      await auth.fetchUser()
    }
    if (!auth.user?.is_staff) {
      return { name: 'dashboard' }
    }
  }

  return true
})

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title === APP_NAME ? APP_NAME : `${to.meta.title} | ${APP_NAME}`
  }
})

export default router
