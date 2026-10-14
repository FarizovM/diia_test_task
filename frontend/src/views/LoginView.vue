<template>
    <div class="min-h-screen flex items-center justify-center bg-diia-dark px-4">
        <div class="w-full max-w-md bg-white rounded-3xl p-8 shadow-2xl">
            <div class="flex items-center gap-3 mb-6">
                <div
                    class="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center font-bold text-xl">
                    Дія
                </div>
                <div>
                    <h1 class="text-xl font-bold text-black">Трембіта CRM</h1>
                    <p class="text-xs text-gray-500">Авторизація в системі управління задачами</p>
                </div>
            </div>

            <!-- Повідомлення про помилку -->
            <div v-if="authStore.error"
                class="mb-4 p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
                {{ authStore.error }}
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-600 mb-1.5">
                        Електронна пошта
                    </label>
                    <input v-model="email" type="email" required placeholder="test@diia.gov.ua"
                        class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-black focus:outline-none text-sm" />
                </div>

                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-600 mb-1.5">
                        Пароль
                    </label>
                    <div class="relative">
                        <input :type="showPassword ? 'text' : 'password'" v-model="password" required
                            placeholder="••••••••"
                            class="w-full pl-4 pr-11 py-3 rounded-xl border border-gray-300 focus:border-black focus:outline-none text-sm" />
                        <button type="button" @click="showPassword = !showPassword"
                            class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-black transition focus:outline-none"
                            :aria-label="showPassword ? 'Приховати пароль' : 'Показати пароль'" tabindex="-1">
                            <!-- Eye icon (when password is hidden) -->
                            <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>
                            <!-- Eye-slash icon (when password is shown) -->
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                            </svg>
                        </button>
                    </div>
                </div>

                <button type="submit" :disabled="authStore.loading"
                    class="w-full py-3.5 rounded-xl bg-black text-white font-semibold text-sm hover:bg-gray-800 transition disabled:opacity-50">
                    {{ authStore.loading ? 'Завантаження...' : (isRegister ? 'Зареєструватися' : 'Увійти в систему') }}
                </button>
            </form>

            <div class="mt-6 pt-5 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
                <span>{{ isRegister ? 'Вже маєте акаунт?' : 'Немає облікового запису?' }}</span>
                <button @click="isRegister = !isRegister" class="font-semibold text-black underline">
                    {{ isRegister ? 'Увійти' : 'Створити акаунт' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isRegister = ref<boolean>(false)
const showPassword = ref<boolean>(false)
const email = ref<string>('')
const password = ref<string>('')

const handleSubmit = async (): Promise<void> => {
    if (!email.value || !password.value) return

    const success = isRegister.value
        ? await authStore.register(email.value, password.value)
        : await authStore.login(email.value, password.value)

    if (success) {
        router.push('/tasks')
    }
}
</script>