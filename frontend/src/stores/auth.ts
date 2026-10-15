import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { AxiosError } from 'axios'
import api from '../api/axios'
import type { User, AuthTokenResponse, UserRegisterPayload } from '../types/models'

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const token = ref<string | null>(localStorage.getItem('access_token'))
    const loading = ref<boolean>(false)
    const error = ref<string | null>(null)

    const isAuthenticated = computed<boolean>(() => !!token.value)

    async function login(email: string, password: string): Promise<boolean> {
        loading.value = true
        error.value = null
        try {
            const formData = new URLSearchParams()
            formData.append('username', email)
            formData.append('password', password)

            const { data } = await api.post<AuthTokenResponse>('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            })

            token.value = data.access_token
            localStorage.setItem('access_token', data.access_token)
            await fetchUser()
            return true
        } catch (err) {
            const axiosErr = err as AxiosError<{ detail?: string }>
            error.value = axiosErr.response?.data?.detail || 'Помилка авторизації'
            return false
        } finally {
            loading.value = false
        }
    }

    async function register(payload: UserRegisterPayload): Promise<boolean> {
        loading.value = true
        error.value = null
        try {
            await api.post<User>('/auth/register', payload)
            return await login(payload.email, payload.password)
        } catch (err) {
            const axiosErr = err as AxiosError<{ detail?: string | any[] }>
            const detail = axiosErr.response?.data?.detail
            if (typeof detail === 'string') {
                error.value = detail
            } else if (Array.isArray(detail) && detail.length > 0) {
                error.value = detail
                    .map((e: any) => {
                        const raw = String(e.msg || e.message || '')
                        return raw.replace(/^Value error,\s*/i, '')
                    })
                    .join(', ')
            } else {
                error.value = 'Помилка реєстрації'
            }
            return false
        } finally {
            loading.value = false
        }
    }

    async function fetchUser(): Promise<void> {
        if (!token.value) return
        try {
            const { data } = await api.get<User>('/users/me')
            user.value = data
        } catch {
            user.value = null
        }
    }

    async function logout(): Promise<void> {
        try {
            if (token.value) {
                await api.post('/auth/logout')
            }
        } catch (e) {
            console.warn('Logout error:', e)
        } finally {
            token.value = null
            user.value = null
            localStorage.removeItem('access_token')
        }
    }

    return {
        user,
        token,
        loading,
        error,
        isAuthenticated,
        login,
        register,
        fetchUser,
        logout,
    }
})