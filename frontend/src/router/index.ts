import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import CrmLayout from '../layouts/CrmLayout.vue'
import LoginView from '../views/LoginView.vue'
import TasksView from '../views/TasksView.vue'
import AboutView from '../views/AboutView.vue'

const routes: RouteRecordRaw[] = [
    { path: '/login', name: 'Login', component: LoginView },
    {
        path: '/',
        component: CrmLayout,
        redirect: '/about',
        meta: { requiresAuth: true },
        children: [
            {
                path: 'about',
                name: 'About',
                component: AboutView
            },
            {
                path: 'tasks',
                name: 'Tasks',
                component: TasksView
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to) => {
    const token = localStorage.getItem('access_token')
    if (to.meta.requiresAuth && !token) {
        return '/login'
    }
    if (to.path === '/login' && token) {
        return '/tasks'
    }
})

export default router