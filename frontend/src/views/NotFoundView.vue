<template>
    <div class="min-h-[calc(100vh-8rem)] flex items-center justify-center py-8">
        <div class="w-full max-w-xl mx-auto">
            <!-- Головна картка у стилі Дія -->
            <div
                class="bg-white rounded-3xl p-8 md:p-12 border border-gray-200/80 shadow-xs text-center relative overflow-hidden">
                <!-- Верхня декоративна смуга -->
                <div
                    class="absolute top-0 inset-x-0 h-1.5 bg-gradient-to-r from-diia-dark via-diia-accent to-diia-dark">
                </div>

                <!-- Цифровий індикатор -->
                <div class="text-7xl md:text-8xl font-black text-diia-dark tracking-tighter select-none font-mono my-2">
                    404
                </div>

                <!-- Заголовок -->
                <h1 class="text-2xl md:text-3xl font-bold text-diia-dark tracking-tight">
                    Сторінку не знайдено
                </h1>

                <!-- Опис із відображенням неіснуючого маршруту -->
                <p class="text-gray-500 text-sm md:text-base mt-3 max-w-md mx-auto leading-relaxed">
                    Запитувана адреса
                    <span v-if="attemptedPath"
                        class="inline-block font-mono text-xs px-2 py-0.5 rounded-lg bg-gray-100 text-gray-800 font-semibold border border-gray-200 mx-1">
                        {{ attemptedPath }}
                    </span>
                    не існує або цей розділ було прибрано.
                </p>

                <!-- Блок швидких дій -->
                <div class="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
                    <!--<router-link to="/tasks"
                        class="w-full sm:w-auto px-5 py-3 rounded-xl bg-diia-dark hover:bg-black text-white text-sm font-semibold transition flex items-center justify-center gap-2 shadow-xs cursor-pointer">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                        </svg>
                        <span>До реєстру задач</span>
                    </router-link>

                    <router-link to="/about"
                        class="w-full sm:w-auto px-5 py-3 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm font-semibold transition flex items-center justify-center gap-2 cursor-pointer">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                        <span>В аналітику</span>
                    </router-link>-->

                    <button type="button" @click="handleBack"
                        class="w-full sm:w-auto min-w-[220px] px-8 py-3.5 rounded-xl border border-gray-300 hover:bg-gray-100 text-gray-800 text-sm font-semibold transition flex items-center justify-center gap-2 cursor-pointer shadow-2xs">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        <span>Назад</span>
                    </button>
                </div>

                <!-- Рекомендовані доступні розділи -->
                <div class="mt-10 pt-6 border-t border-gray-100 text-left">
                    <div
                        class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 text-center sm:text-left">
                        Доступні розділи системи
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <router-link to="/tasks"
                            class="p-3 rounded-xl bg-gray-50 hover:bg-gray-100 border border-gray-200/60 transition group flex items-start gap-3">
                            <div
                                class="w-8 h-8 rounded-lg bg-diia-dark text-diia-accent flex items-center justify-center shrink-0">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                                </svg>
                            </div>
                            <div>
                                <div class="text-xs font-bold text-gray-900 group-hover:text-black">
                                    Реєстр задач
                                </div>
                                <div class="text-[11px] text-gray-500">
                                    Пошук, фільтрація та керування
                                </div>
                            </div>
                        </router-link>

                        <router-link to="/about"
                            class="p-3 rounded-xl bg-gray-50 hover:bg-gray-100 border border-gray-200/60 transition group flex items-start gap-3">
                            <div
                                class="w-8 h-8 rounded-lg bg-diia-dark text-diia-accent flex items-center justify-center shrink-0">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <div>
                                <div class="text-xs font-bold text-gray-900 group-hover:text-black">
                                    Про систему
                                </div>
                                <div class="text-[11px] text-gray-500">
                                    Інформація про систему та KPI
                                </div>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const attemptedPath = computed<string>(() => {
    return (route.query.from as string) || (route.path !== '/404' ? route.path : '')
})

const handleBack = () => {
    if (window.history.length > 1) {
        router.back()
    } else {
        router.push('/tasks')
    }
}
</script>
