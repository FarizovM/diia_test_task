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
                    <input v-model="password" type="password" required placeholder="••••••••"
                        class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-black focus:outline-none text-sm" />
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
const email = ref<string>('test@diia.gov.ua')
const password = ref<string>('password123')

const handleSubmit = async (): Promise<void> => {
    const success = isRegister.value
        ? await authStore.register(email.value, password.value)
        : await authStore.login(email.value, password.value)

    if (success) {
        router.push('/tasks')
    }
}
</script>