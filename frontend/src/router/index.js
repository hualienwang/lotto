import { createRouter, createWebHistory } from 'vue-router'
import LatestResult from '../views/LatestResult.vue'
import History from '../views/History.vue'
import Prediction from '../views/Prediction.vue'
import Statistics from '../views/Statistics.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'LatestResult',
    component: LatestResult
  },
  {
    path: '/history',
    name: 'History',
    component: History
  },
  {
    path: '/prediction',
    name: 'Prediction',
    component: Prediction
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
