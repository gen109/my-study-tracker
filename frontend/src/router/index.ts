import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/registry',
      name: 'registry',
      component: () => import('@/views/TargetRegistryView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/score/:examId',
      name: 'score',
      component: () => import('@/views/ScoreInputView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/analysis/:examId',
      name: 'analysis',
      component: () => import('@/views/AnalysisView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/master',
      name: 'master',
      component: () => import('@/views/MasterView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

// ログイン前後のガード
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'login' }
  }
})

export default router
