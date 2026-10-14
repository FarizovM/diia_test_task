<template>
    <div class="space-y-6 max-w-7xl mx-auto pb-12">
        <!-- Головна картка привітання та огляду проекту -->
        <div class="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-sm relative overflow-hidden">
            <div
                class="absolute top-0 right-0 w-96 h-96 bg-diia-accent/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20">
            </div>

            <div class="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                <div>
                    <div
                        class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-black text-white text-xs font-semibold tracking-wide uppercase mb-3">
                        <span class="w-2 h-2 rounded-full bg-diia-accent animate-pulse"></span>
                        Трембіта CRM • Дія
                    </div>
                    <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">
                        Панель моніторингу та огляд системи
                    </h1>
                    <p class="text-gray-600 text-sm mt-2 max-w-2xl leading-relaxed">
                        Централізований моніторинг завдань та інформація про архітектуру комплексу.
                        Інтерфейс побудовано за концепцією Low-Code реєстрів (JSON-driven UI) у візуальному стилі Дія.
                    </p>

                    <div v-if="authStore.user" class="mt-4 flex items-center gap-2 text-xs text-gray-500">
                        <span class="font-medium text-gray-700">
                            Користувач: {{ authStore.user.first_name }} {{ authStore.user.last_name }}
                        </span>
                        <span>•</span>
                        <span>{{ authStore.user.email }}</span>
                    </div>
                </div>

                <div class="flex flex-wrap items-center gap-3 shrink-0">
                    <button @click="fetchStats" :disabled="loading"
                        class="px-4 py-2.5 rounded-xl border border-gray-300 text-xs font-semibold text-gray-700 hover:bg-gray-50 transition flex items-center gap-2 disabled:opacity-50"
                        title="Оновити статистику">
                        <svg class="w-4 h-4 text-gray-500" :class="{ 'animate-spin': loading }" fill="none"
                            stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Оновити
                    </button>
                    <router-link to="/tasks"
                        class="px-5 py-2.5 rounded-xl bg-black text-white text-xs font-semibold hover:bg-gray-800 transition flex items-center gap-2 shadow-sm">
                        Реєстр задач
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M14 5l7 7m0 0l-7 7m7-7H3" />
                        </svg>
                    </router-link>
                </div>
            </div>
        </div>

        <!-- Повідомлення про помилку -->
        <div v-if="error"
            class="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center justify-between">
            <div class="flex items-center gap-3">
                <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span>{{ error }}</span>
            </div>
            <button @click="fetchStats" class="text-xs font-semibold underline hover:text-red-900">Спробувати
                знову</button>
        </div>

        <!-- Перемикач режиму відображення статистики -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <h2 class="text-xl font-bold text-gray-900">Показники ефективності</h2>

            <div class="inline-flex p-1 bg-gray-200/70 rounded-2xl text-xs font-semibold text-gray-600">
                <button @click="activeTab = 'compare'" class="px-4 py-2 rounded-xl transition-all"
                    :class="activeTab === 'compare' ? 'bg-white text-black shadow-sm' : 'hover:text-black'">
                    Порівняння
                </button>
                <button @click="activeTab = 'all'" class="px-4 py-2 rounded-xl transition-all"
                    :class="activeTab === 'all' ? 'bg-white text-black shadow-sm' : 'hover:text-black'">
                    Загальна система
                </button>
                <button @click="activeTab = 'me'" class="px-4 py-2 rounded-xl transition-all"
                    :class="activeTab === 'me' ? 'bg-white text-black shadow-sm' : 'hover:text-black'">
                    Мої задачі
                </button>
            </div>
        </div>

        <!-- Скелетон завантаження -->
        <div v-if="loading && !statsAll" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div v-for="n in 6" :key="n"
                class="bg-white rounded-2xl p-5 border border-gray-200 animate-pulse space-y-3">
                <div class="h-3 bg-gray-200 rounded w-16"></div>
                <div class="h-8 bg-gray-200 rounded w-12"></div>
                <div class="h-3 bg-gray-100 rounded w-24"></div>
            </div>
        </div>

        <!-- Карточки ключових метрик (KPI) -->
        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <!-- Всього -->
            <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow transition">
                <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span class="font-medium">Всього задач</span>
                    <span class="w-2.5 h-2.5 rounded-full bg-black"></span>
                </div>
                <div class="text-2xl font-bold text-gray-900">
                    {{ displayStats?.total ?? 0 }}
                </div>
                <div class="mt-2 text-[11px] text-gray-500">
                    <span v-if="activeTab === 'compare'">
                        Моїх: <strong class="text-black">{{ statsMe?.total ?? 0 }}</strong> із {{ statsAll?.total ?? 0
                        }}
                    </span>
                    <span v-else>Усі зареєстровані</span>
                </div>
            </div>

            <!-- В процесі -->
            <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow transition">
                <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span class="font-medium">В процесі</span>
                    <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                </div>
                <div class="text-2xl font-bold text-blue-600">
                    {{ displayStats?.in_progress ?? 0 }}
                </div>
                <div class="mt-2 text-[11px] text-gray-500">
                    <span v-if="activeTab === 'compare'">
                        Моїх: <strong class="text-black">{{ statsMe?.in_progress ?? 0 }}</strong>
                    </span>
                    <span v-else>Активно розробляються</span>
                </div>
            </div>

            <!-- QA -->
            <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow transition">
                <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span class="font-medium">На QA</span>
                    <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                </div>
                <div class="text-2xl font-bold text-amber-600">
                    {{ displayStats?.qa ?? 0 }}
                </div>
                <div class="mt-2 text-[11px] text-gray-500">
                    <span v-if="activeTab === 'compare'">
                        Моїх: <strong class="text-black">{{ statsMe?.qa ?? 0 }}</strong>
                    </span>
                    <span v-else>Тестування / Перевірка</span>
                </div>
            </div>

            <!-- Виконано -->
            <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow transition">
                <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span class="font-medium">Виконано</span>
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                </div>
                <div class="text-2xl font-bold text-emerald-600">
                    {{ displayStats?.done ?? 0 }}
                </div>
                <div class="mt-2 text-[11px] text-gray-500">
                    <span v-if="activeTab === 'compare'">
                        Моїх: <strong class="text-black">{{ statsMe?.done ?? 0 }}</strong>
                    </span>
                    <span v-else>Успішно завершено</span>
                </div>
            </div>

            <!-- Заблоковано -->
            <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow transition">
                <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span class="font-medium">Заблоковано</span>
                    <span class="w-2.5 h-2.5 rounded-full bg-red-500"></span>
                </div>
                <div class="text-2xl font-bold text-red-600">
                    {{ displayStats?.flagged ?? 0 }}
                </div>
                <div class="mt-2 text-[11px] text-gray-500">
                    <span v-if="activeTab === 'compare'">
                        Моїх: <strong class="text-black">{{ statsMe?.flagged ?? 0 }}</strong>
                    </span>
                    <span v-else>Потребують уваги</span>
                </div>
            </div>

            <!-- Прострочено -->
            <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow transition">
                <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span class="font-medium">Прострочено</span>
                    <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
                </div>
                <div class="text-2xl font-bold text-rose-600">
                    {{ displayStats?.overdue ?? 0 }}
                </div>
                <div class="mt-2 text-[11px] text-gray-500">
                    <span v-if="activeTab === 'compare'">
                        Моїх: <strong class="text-rose-700">{{ statsMe?.overdue ?? 0 }}</strong>
                    </span>
                    <span v-else>Дедлайн вийшов</span>
                </div>
            </div>
        </div>

        <!-- Порівняльні панелі: Загальна vs Моя статистика -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Блок: Загальна статистика системи -->
            <div v-if="activeTab === 'compare' || activeTab === 'all'"
                class="bg-white rounded-3xl p-6 sm:p-7 border border-gray-200 shadow-sm space-y-6"
                :class="{ 'lg:col-span-2': activeTab === 'all' }">
                <div class="flex items-center justify-between border-b border-gray-100 pb-4">
                    <div class="flex items-center gap-3">
                        <div
                            class="w-9 h-9 rounded-xl bg-black text-white flex items-center justify-center font-bold text-xs">
                            ВСІ
                        </div>
                        <div>
                            <h3 class="text-base font-bold text-gray-900">Загальний стан реєстру</h3>
                            <p class="text-xs text-gray-500">Агреговані дані по всіх користувачах системи</p>
                        </div>
                    </div>
                    <span class="px-3 py-1 rounded-full bg-gray-100 text-xs font-semibold text-gray-700">
                        Всього: {{ statsAll?.total ?? 0 }}
                    </span>
                </div>

                <!-- Прогрес-бари статусів -->
                <div class="space-y-3">
                    <div class="text-xs font-semibold uppercase tracking-wider text-gray-400">
                        Розподіл за статусами
                    </div>

                    <div class="space-y-2 text-xs">
                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-gray-400"></span> До виконання (TODO)
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsAll?.todo ?? 0 }} ({{
                                    getPercentage(statsAll?.todo, statsAll?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-gray-400 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsAll?.todo, statsAll?.total) + '%' }"></div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-blue-500"></span> В процесі
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsAll?.in_progress ?? 0 }} ({{
                                    getPercentage(statsAll?.in_progress, statsAll?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-blue-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsAll?.in_progress, statsAll?.total) + '%' }">
                                </div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-amber-500"></span> На тестуванні (QA)
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsAll?.qa ?? 0 }} ({{
                                    getPercentage(statsAll?.qa, statsAll?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-amber-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsAll?.qa, statsAll?.total) + '%' }"></div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Виконано
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsAll?.done ?? 0 }} ({{
                                    getPercentage(statsAll?.done, statsAll?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-emerald-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsAll?.done, statsAll?.total) + '%' }"></div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-red-500"></span> Заблоковано
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsAll?.flagged ?? 0 }} ({{
                                    getPercentage(statsAll?.flagged, statsAll?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-red-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsAll?.flagged, statsAll?.total) + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Розподіл за пріоритетами -->
                <div class="pt-2 border-t border-gray-100">
                    <div class="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-3">
                        Розподіл за пріоритетами
                    </div>
                    <div class="grid grid-cols-5 gap-2 text-center">
                        <div class="p-2.5 rounded-xl bg-red-50 border border-red-100">
                            <div class="text-[10px] text-red-600 font-semibold uppercase">Найвищий</div>
                            <div class="text-lg font-bold text-red-700 mt-1">{{ statsAll?.highest ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-orange-50 border border-orange-100">
                            <div class="text-[10px] text-orange-600 font-semibold uppercase">Високий</div>
                            <div class="text-lg font-bold text-orange-700 mt-1">{{ statsAll?.high ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-100">
                            <div class="text-[10px] text-amber-600 font-semibold uppercase">Середній</div>
                            <div class="text-lg font-bold text-amber-700 mt-1">{{ statsAll?.medium ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-blue-50 border border-blue-100">
                            <div class="text-[10px] text-blue-600 font-semibold uppercase">Низький</div>
                            <div class="text-lg font-bold text-blue-700 mt-1">{{ statsAll?.low ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-gray-50 border border-gray-200">
                            <div class="text-[10px] text-gray-500 font-semibold uppercase">Найнижчий</div>
                            <div class="text-lg font-bold text-gray-700 mt-1">{{ statsAll?.lowest ?? 0 }}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Блок: Статистика поточного користувача -->
            <div v-if="activeTab === 'compare' || activeTab === 'me'"
                class="bg-white rounded-3xl p-6 sm:p-7 border border-gray-200 shadow-sm space-y-6"
                :class="{ 'lg:col-span-2': activeTab === 'me' }">
                <div class="flex items-center justify-between border-b border-gray-100 pb-4">
                    <div class="flex items-center gap-3">
                        <div
                            class="w-9 h-9 rounded-xl bg-diia-accent text-black flex items-center justify-center font-bold text-xs">
                            МОЇ
                        </div>
                        <div>
                            <h3 class="text-base font-bold text-gray-900">Моя статистика</h3>
                            <p class="text-xs text-gray-500">Задачі, створені вашим обліковим записом</p>
                        </div>
                    </div>
                    <span class="px-3 py-1 rounded-full bg-diia-accent/30 text-xs font-semibold text-black">
                        Створено: {{ statsMe?.total ?? 0 }}
                    </span>
                </div>

                <!-- Прогрес-бари статусів -->
                <div class="space-y-3">
                    <div class="text-xs font-semibold uppercase tracking-wider text-gray-400">
                        Розподіл за статусами
                    </div>

                    <div class="space-y-2 text-xs">
                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-gray-400"></span> До виконання (TODO)
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsMe?.todo ?? 0 }} ({{
                                    getPercentage(statsMe?.todo, statsMe?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-gray-400 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsMe?.todo, statsMe?.total) + '%' }"></div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-blue-500"></span> В процесі
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsMe?.in_progress ?? 0 }} ({{
                                    getPercentage(statsMe?.in_progress, statsMe?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-blue-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsMe?.in_progress, statsMe?.total) + '%' }"></div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-amber-500"></span> На тестуванні (QA)
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsMe?.qa ?? 0 }} ({{
                                    getPercentage(statsMe?.qa, statsMe?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-amber-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsMe?.qa, statsMe?.total) + '%' }"></div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Виконано
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsMe?.done ?? 0 }} ({{
                                    getPercentage(statsMe?.done, statsMe?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-emerald-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsMe?.done, statsMe?.total) + '%' }"></div>
                            </div>
                        </div>

                        <div>
                            <div class="flex justify-between font-medium mb-1">
                                <span class="flex items-center gap-1.5 text-gray-700">
                                    <span class="w-2 h-2 rounded-full bg-red-500"></span> Заблоковано
                                </span>
                                <span class="text-gray-900 font-semibold">{{ statsMe?.flagged ?? 0 }} ({{
                                    getPercentage(statsMe?.flagged, statsMe?.total) }}%)</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                                <div class="bg-red-500 h-full rounded-full transition-all duration-500"
                                    :style="{ width: getPercentage(statsMe?.flagged, statsMe?.total) + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Розподіл за пріоритетами -->
                <div class="pt-2 border-t border-gray-100">
                    <div class="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-3">
                        Розподіл за пріоритетами
                    </div>
                    <div class="grid grid-cols-5 gap-2 text-center">
                        <div class="p-2.5 rounded-xl bg-red-50 border border-red-100">
                            <div class="text-[10px] text-red-600 font-semibold uppercase">Найвищий</div>
                            <div class="text-lg font-bold text-red-700 mt-1">{{ statsMe?.highest ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-orange-50 border border-orange-100">
                            <div class="text-[10px] text-orange-600 font-semibold uppercase">Високий</div>
                            <div class="text-lg font-bold text-orange-700 mt-1">{{ statsMe?.high ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-100">
                            <div class="text-[10px] text-amber-600 font-semibold uppercase">Середній</div>
                            <div class="text-lg font-bold text-amber-700 mt-1">{{ statsMe?.medium ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-blue-50 border border-blue-100">
                            <div class="text-[10px] text-blue-600 font-semibold uppercase">Низький</div>
                            <div class="text-lg font-bold text-blue-700 mt-1">{{ statsMe?.low ?? 0 }}</div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-gray-50 border border-gray-200">
                            <div class="text-[10px] text-gray-500 font-semibold uppercase">Найнижчий</div>
                            <div class="text-lg font-bold text-gray-700 mt-1">{{ statsMe?.lowest ?? 0 }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '../api/axios'
import { useAuthStore } from '../stores/auth'
import type { TaskStats } from '../types/models'

const authStore = useAuthStore()

const activeTab = ref<'compare' | 'all' | 'me'>('compare')
const loading = ref<boolean>(false)
const error = ref<string | null>(null)

const statsAll = ref<TaskStats | null>(null)
const statsMe = ref<TaskStats | null>(null)

const displayStats = computed<TaskStats | null>(() => {
    if (activeTab.value === 'me') {
        return statsMe.value
    }
    return statsAll.value
})

const getPercentage = (count: number | undefined, total: number | undefined): number => {
    if (!count || !total || total === 0) return 0
    return Math.round((count / total) * 100)
}

const fetchStats = async (): Promise<void> => {
    loading.value = true
    error.value = null

    try {
        const [resAll, resMe] = await Promise.all([
            api.get<TaskStats>('/stats/all'),
            api.get<TaskStats>('/stats/me')
        ])

        statsAll.value = resAll.data
        statsMe.value = resMe.data
    } catch (err: any) {
        error.value = err?.response?.data?.detail || 'Не вдалося завантажити статистику'
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchStats()
})
</script>