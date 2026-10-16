import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import CrmLayout from '../layouts/CrmLayout.vue'
import LoginView from '../views/LoginView.vue'
import RegistryView from '../views/RegistryView.vue'
import AboutView from '../views/AboutView.vue'
import NotFoundView from '../views/NotFoundView.vue'

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
                component: AboutView,
            },
            {
                path: 'tasks',
                name: 'Tasks',
                component: RegistryView,
            },
            {
                path: '404',
                name: 'NotFound',
                component: NotFoundView,
            },
        ],
    },
    // Перевірка на наявність роуту: усі невідомі адреси перенаправляються на 404
    {
        path: '/:pathMatch(.*)*',
        name: 'CatchAll',
        redirect: (to) => {
            const token = localStorage.getItem('access_token')
            if (!token) {
                return '/login'
            }
            return { path: '/404', query: { from: to.fullPath } }
        },
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