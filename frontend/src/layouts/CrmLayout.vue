<template>
    <div class="min-h-screen flex bg-diia-light">
        <!-- Бокова панель у стилі Дія -->
        <aside class="w-72 bg-diia-dark text-white flex flex-col justify-between shrink-0">
            <div>
                <!-- Логотип -->
                <router-link to="/about">
                    <div class="p-6 border-b border-white/10 flex items-center gap-4">
                        <div
                            class="w-11 h-11 rounded-xl bg-white text-black flex items-center justify-center font-bold text-xl tracking-tighter">
                            Дія
                        </div>
                        <div>
                            <div class="font-bold text-base tracking-tight">ТРЕМБІТА</div>
                            <div class="text-xs text-gray-400">Управління задачами</div>
                        </div>
                    </div>
                </router-link>

                <!-- Динамічне меню з JSON-конфігу -->
                <nav class="p-4 space-y-1.5">

                    <!-- Пошук по пунктах меню -->
                    <div class="relative mb-2">
                        <span
                            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </span>
                        <input v-model="searchQuery" type="text" placeholder="Пошук у меню..."
                            class="w-full bg-white/5 border border-white/10 rounded-xl pl-9 pr-8 py-2 text-xs text-white placeholder-gray-400 focus:outline-none focus:bg-white/10 focus:border-white/20 transition" />
                        <button v-if="searchQuery" type="button" @click="searchQuery = ''"
                            class="absolute inset-y-0 right-0 pr-2.5 flex items-center text-gray-400 hover:text-white transition focus:outline-none"
                            title="Очистити">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <router-link v-for="item in filteredNavItems" :key="item.id" :to="item.route"
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

                    <div v-if="filteredNavItems.length === 0" class="px-3 py-4 text-xs text-center text-gray-400">
                        Розділ не знайдено
                    </div>
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

        <main class="flex-1 p-8 overflow-y-scroll [scrollbar-gutter:stable]">
            <router-view />
        </main>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import rawNavItems from '../config/navigation.json'
import type { NavItem } from '../types/config'

const navItems = rawNavItems as NavItem[]
const searchQuery = ref<string>('')

const filteredNavItems = computed<NavItem[]>(() => {
    const query = searchQuery.value.trim().toLowerCase()
    if (!query) {
        return navItems
    }
    return navItems.filter((item) => item.title.toLowerCase().includes(query))
})
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