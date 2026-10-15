<template>
    <div class="min-h-screen flex items-center justify-center bg-diia-dark px-4 py-8">
        <div class="w-full max-w-md sm:max-w-lg bg-white rounded-3xl p-6 sm:p-8 shadow-2xl transition-all">
            <!-- Шапка форми у стилі Дія -->
            <div class="flex items-center gap-3.5 mb-6">
                <div
                    class="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center font-bold text-xl shrink-0 shadow-xs">
                    Дія
                </div>
                <div>
                    <h1 class="text-xl font-extrabold text-diia-primary">
                        {{ isRegister ? 'Реєстрація у CRM' : 'Трембіта CRM' }}
                    </h1>
                    <p class="text-xs text-gray-500 mt-0.5">
                        {{ isRegister ? 'Створіть новий обліковий запис користувача' : 'Авторизація в системі управління задачами' }}
                    </p>
                </div>
            </div>

            <!-- Повідомлення про помилку -->
            <div v-if="authStore.error"
                class="mb-4 p-3.5 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-xs sm:text-sm font-medium">
                {{ authStore.error }}
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <!-- Блок ПІБ (тільки для реєстрації) -->
                <template v-if="isRegister">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-1.5">
                                Прізвище <span class="text-red-500">*</span>
                            </label>
                            <input v-model="lastName" type="text" required placeholder="Шевченко"
                                class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 sm:py-3 text-sm text-diia-primary placeholder-gray-400 focus:outline-none focus:bg-white focus:border-black transition" />
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-1.5">
                                Ім'я <span class="text-red-500">*</span>
                            </label>
                            <input v-model="firstName" type="text" required placeholder="Тарас"
                                class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 sm:py-3 text-sm text-diia-primary placeholder-gray-400 focus:outline-none focus:bg-white focus:border-black transition" />
                        </div>
                    </div>

                    <div>
                        <div class="flex items-center justify-between mb-1.5">
                            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700">
                                По батькові
                            </label>
                            <span class="text-[11px] text-gray-400 font-medium">необов'язково</span>
                        </div>
                        <input v-model="middleName" type="text" placeholder="Григорович"
                            class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 sm:py-3 text-sm text-diia-primary placeholder-gray-400 focus:outline-none focus:bg-white focus:border-black transition" />
                    </div>
                </template>

                <!-- Електронна пошта -->
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-1.5">
                        Електронна пошта <span class="text-red-500">*</span>
                    </label>
                    <input v-model="email" type="email" required placeholder="test@diia.gov.ua"
                        class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 sm:py-3 text-sm text-diia-primary placeholder-gray-400 focus:outline-none focus:bg-white focus:border-black transition" />
                </div>

                <!-- Пароль з перемикачем видимості -->
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-1.5">
                        Пароль <span class="text-red-500">*</span>
                    </label>
                    <div class="relative">
                        <input :type="showPassword ? 'text' : 'password'" v-model="password" required
                            placeholder="••••••••"
                            class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl pl-4 pr-11 py-2.5 sm:py-3 text-sm text-diia-primary placeholder-gray-400 focus:outline-none focus:bg-white focus:border-black transition" />
                        <button type="button" @click="showPassword = !showPassword"
                            class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-black transition focus:outline-none cursor-pointer"
                            :aria-label="showPassword ? 'Приховати пароль' : 'Показати пароль'" tabindex="-1">
                            <!-- Іконка відкритого ока -->
                            <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.8" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>
                            <!-- Іконка перекресленого ока -->
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.8" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                            </svg>
                        </button>
                    </div>

                    <!-- Візуальний чекліст вимог до пароля (у режимі реєстрації) -->
                    <div v-if="isRegister" class="mt-2.5 p-3.5 bg-diia-light/60 border border-gray-100 rounded-2xl space-y-2 text-xs">
                        <div class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">
                            Вимоги до пароля:
                        </div>
                        <div class="space-y-1.5">
                            <!-- Мінімум 8 символів -->
                            <div class="flex items-center gap-2 transition-colors"
                                :class="hasMinLength ? 'text-emerald-700 font-semibold' : 'text-gray-400'">
                                <svg v-if="hasMinLength" class="w-4 h-4 text-emerald-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                                </svg>
                                <span v-else class="w-1.5 h-1.5 rounded-full bg-gray-300 ml-1.5 mr-1 shrink-0"></span>
                                <span>Щонайменше 8 символів</span>
                            </div>

                            <!-- Літера -->
                            <div class="flex items-center gap-2 transition-colors"
                                :class="hasLetter ? 'text-emerald-700 font-semibold' : 'text-gray-400'">
                                <svg v-if="hasLetter" class="w-4 h-4 text-emerald-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                                </svg>
                                <span v-else class="w-1.5 h-1.5 rounded-full bg-gray-300 ml-1.5 mr-1 shrink-0"></span>
                                <span>Містить хоча б одну латинську літеру (a-z, A-Z)</span>
                            </div>

                            <!-- Цифра -->
                            <div class="flex items-center gap-2 transition-colors"
                                :class="hasDigit ? 'text-emerald-700 font-semibold' : 'text-gray-400'">
                                <svg v-if="hasDigit" class="w-4 h-4 text-emerald-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                                </svg>
                                <span v-else class="w-1.5 h-1.5 rounded-full bg-gray-300 ml-1.5 mr-1 shrink-0"></span>
                                <span>Містить хоча б одну цифру (0-9)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Кнопка відправки форми -->
                <button type="submit" :disabled="authStore.loading"
                    class="w-full mt-2 py-3.5 rounded-2xl bg-diia-dark hover:bg-black text-white font-semibold text-sm transition shadow-sm active:scale-95 disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2">
                    <svg v-if="authStore.loading" class="w-4 h-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                    </svg>
                    <span>
                        {{ authStore.loading ? 'Обробка запиту...' : (isRegister ? 'Зареєструватися' : 'Увійти в систему') }}
                    </span>
                </button>
            </form>

            <!-- Перемикання між входом та реєстрацією -->
            <div class="mt-6 pt-5 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
                <span>{{ isRegister ? 'Вже маєте акаунт?' : 'Немає облікового запису?' }}</span>
                <button type="button" @click="toggleMode" class="font-bold text-black hover:underline cursor-pointer">
                    {{ isRegister ? 'Увійти' : 'Створити акаунт' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isRegister = ref<boolean>(false)
const showPassword = ref<boolean>(false)

const firstName = ref<string>('')
const lastName = ref<string>('')
const middleName = ref<string>('')
const email = ref<string>('')
const password = ref<string>('')

// Критерії валідації пароля
const hasMinLength = computed<boolean>(() => password.value.length >= 8)
const hasLetter = computed<boolean>(() => /[a-zA-Z]/.test(password.value))
const hasDigit = computed<boolean>(() => /\d/.test(password.value))
const isPasswordValid = computed<boolean>(() => hasMinLength.value && hasLetter.value && hasDigit.value)

function toggleMode() {
    isRegister.value = !isRegister.value
    authStore.error = null
}

const handleSubmit = async (): Promise<void> => {
    if (!email.value.trim() || !password.value) return

    let success = false
    if (isRegister.value) {
        if (!lastName.value.trim()) {
            authStore.error = "Будь ласка, вкажіть прізвище"
            return
        }
        if (!firstName.value.trim()) {
            authStore.error = "Будь ласка, вкажіть ім'я"
            return
        }
        if (!isPasswordValid.value) {
            authStore.error = "Пароль не відповідає всім вимогам безпеки"
            return
        }

        success = await authStore.register({
            email: email.value.trim(),
            password: password.value,
            first_name: firstName.value.trim(),
            last_name: lastName.value.trim(),
            middle_name: middleName.value.trim() || null,
        })
    } else {
        success = await authStore.login(email.value.trim(), password.value)
    }

    if (success) {
        router.push('/about')
    }
}
</script>