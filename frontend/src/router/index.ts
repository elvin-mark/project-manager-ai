import { createRouter, createWebHistory } from 'vue-router'
import ProjectList from '@/components/ProjectList.vue'
import TaskView from '@/components/TaskView.vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'projects',
      component: ProjectList,
      meta: { requiresAuth: true },
    },
    {
      path: '/projects/:projectId',
      name: 'tasks',
      component: TaskView,
      props: true,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('access_token');
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login');
  } else if ((to.name === 'login' || to.name === 'register') && loggedIn) {
    next('/');
  } else {
    next();
  }
});

export default router