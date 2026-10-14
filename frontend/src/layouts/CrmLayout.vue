<template>
    <div class="min-h-screen flex bg-diia-light">
        <!-- Бокова панель у стилі Дія -->
        <aside class="w-72 bg-diia-dark text-white flex flex-col justify-between shrink-0">
            <div>
                <!-- Логотип -->
                <div class="p-6 border-b border-white/10 flex items-center gap-4">
                    <div
                        class="w-11 h-11 rounded-xl bg-white text-black flex items-center justify-center font-bold text-xl tracking-tighter">
                        Дія
                    </div>
                    <div>
                        <div class="font-bold text-base tracking-tight">ТРЕМБІТА</div>
                        <div class="text-xs text-gray-400">Управління реєстрами</div>
                    </div>
                </div>

                <!-- Динамічне меню з JSON-конфігу -->
                <nav class="p-4 space-y-1.5">
                    <div class="px-3 py-2 text-[11px] font-semibold uppercase tracking-wider text-gray-400">
                        Навігація (Low-Code)
                    </div>
                    <router-link v-for="item in navItems" :key="item.id" :to="item.route"
                        class="flex items-center justify-between px-4 py-3 rounded-xl text-sm font-medium transition-all"
                        :class="$route.path.startsWith(item.route)
                            ? 'bg-diia-accent text-black font-semibold'
                            : 'text-gray-300 hover:bg-white/10 hover:text-white'">
                        <div class="flex items-center gap-3">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                            </svg>
                            <span>{{ item.title }}</span>
                        </div>
                    </router-link>
                </nav>
            </div>

            <!-- Профіль користувача та вихід -->
            <div class="p-4 border-t border-white/10 bg-black/20">
                <div class="flex items-center justify-between">
                    <div class="truncate pr-2">
                        <div class="text-xs text-gray-400">Авторизовано як:</div>
                        <div class="text-sm font-medium truncate">{{ authStore.user?.email || 'Завантаження...' }}</div>
                    </div>
                    <button @click="handleLogout"
                        class="px-3 py-2 rounded-lg bg-white/10 hover:bg-red-500/20 hover:text-red-300 text-xs font-medium transition">
                        Вийти
                    </button>
                </div>
            </div>
        </aside>

        <!-- Основний контент -->
        <main class="flex-1 p-8 overflow-y-auto">
            <router-view />
        </main>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import rawNavItems from '../config/navigation.json'
import type { NavItem } from '../types/config'

const navItems = rawNavItems as NavItem[]
const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
    if (!authStore.user) {
        authStore.fetchUser()
    }
})

const handleLogout = async (): Promise<void> => {
    await authStore.logout()
    router.push('/login')
}
</script>