import { createRouter, createWebHistory } from 'vue-router'
import ProjectList from '@/components/ProjectList.vue'
import TaskView from '@/components/TaskView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'projects',
      component: ProjectList,
    },
    {
      path: '/projects/:projectId',
      name: 'tasks',
      component: TaskView,
      props: true,
    },
  ],
})

export default router
