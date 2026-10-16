<template>
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Стан завантаження конфігурації -->
        <div v-if="isLoadingConfig"
            class="bg-white rounded-3xl p-12 border border-gray-200/80 shadow-xs flex flex-col items-center justify-center space-y-4">
            <div class="w-10 h-10 border-4 border-diia-dark border-t-transparent rounded-full animate-spin"></div>
            <p class="text-sm font-semibold text-gray-600">Завантаження реєстру...</p>
        </div>

        <!-- Помилка завантаження конфігурації -->
        <div v-else-if="configError"
            class="bg-red-50 border border-red-200 text-red-800 rounded-3xl p-8 text-center space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center mx-auto">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
            </div>
            <h3 class="text-base font-bold text-red-900">{{ configError }}</h3>
            <p class="text-xs text-red-600">Перевірте назву розділу або наявність файлу конфігурації.</p>
        </div>

        <!-- Основний контент реєстру -->
        <div v-else class="space-y-6">
            <!-- Шапка реєстру -->
            <RegistryHeader :title="registryConfig?.title || 'Реєстр'" :subtitle="registryConfig?.subtitle"
                :total-count="total" :filtered-count="filtered" :is-loading="isTableLoading" @refresh="refreshData"
                @add="openCreateModal" />

            <!-- Панель пошуку та фільтрації -->
            <RegistryToolbar :search-placeholder="registryConfig?.searchPlaceholder" :filters="registryFilters"
                v-model:search="searchQuery" v-model:active-filters="activeFilters" @reset="resetFilters" />

            <!-- Таблиця даних з пагінацією -->
            <RegistryTable :columns="columns" :rows="rows" :is-loading="isTableLoading" :sort-by="sortBy"
                :sort-order="sortOrder" @sort="handleSort" @edit="openEditModal" @delete="openDeleteModal">
                <template #pagination>
                    <RegistryPagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
                        :filtered="filtered" />
                </template>
            </RegistryTable>
        </div>

        <!-- Модалка створення / редагування запису -->
        <RegistryRowModal :is-open="isRowModalOpen" :mode="modalMode" :columns="columns" :initial-data="selectedRow"
            :is-submitting="isSubmitting" @close="isRowModalOpen = false" @submit="handleRowSubmit" />

        <!-- Модалка підтвердження видалення -->
        <RegistryDeleteModal :is-open="isDeleteModalOpen" :item-title="rowToDelete?.title || rowToDelete?.name || ''"
            :is-deleting="isDeleting" @close="isDeleteModalOpen = false" @confirm="handleConfirmDelete" />

        <!-- Сповіщення Toast -->
        <RegistryToast :message="toastMessage" :type="toastType" @close="toastMessage = ''" />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/axios'

import type {
    RegistryConfig,
    RegistryResponse,
    RegistryFilter,
    RegistryColumn,
} from '../types/config'

import RegistryHeader from '../components/registry/RegistryHeader.vue'
import RegistryToolbar from '../components/registry/RegistryToolbar.vue'
import RegistryTable from '../components/registry/RegistryTable.vue'
import RegistryPagination from '../components/registry/RegistryPagination.vue'
import RegistryRowModal from '../components/registry/RegistryRowModal.vue'
import RegistryDeleteModal from '../components/registry/RegistryDeleteModal.vue'
import RegistryToast from '../components/registry/RegistryToast.vue'

const route = useRoute()

// Визначаємо alias з маршруту
const alias = computed(() => {
    const parts = route.path.split('/').filter(Boolean)
    return parts[parts.length - 1] || ''
})

// Стан конфігурації
const registryConfig = ref<RegistryConfig | null>(null)
const isLoadingConfig = ref<boolean>(true)
const configError = ref<string | null>(null)

// Дані таблиці
const rows = ref<any[]>([])
const total = ref<number>(0)
const filtered = ref<number>(0)
const isTableLoading = ref<boolean>(false)

// Фільтри та пагінація
const currentPage = ref<number>(1)
const pageSize = ref<number>(10)
const sortBy = ref<string>('created_at')
const sortOrder = ref<'asc' | 'desc'>('desc')
const searchQuery = ref<string>('')
const activeFilters = ref<Record<string, string>>({})

const columns = ref<RegistryColumn[]>([])
const registryFilters = ref<RegistryFilter[]>([])

// Стан модалок
const isRowModalOpen = ref<boolean>(false)
const modalMode = ref<'create' | 'edit'>('create')
const selectedRow = ref<any>(null)
const isSubmitting = ref<boolean>(false)

const isDeleteModalOpen = ref<boolean>(false)
const rowToDelete = ref<any>(null)
const isDeleting = ref<boolean>(false)

// Стан тостів
const toastMessage = ref<string>('')
const toastType = ref<'success' | 'error'>('success')

let toastTimer: any = null
function showToast(msg: string, type: 'success' | 'error' = 'success') {
    toastMessage.value = msg
    toastType.value = type
    clearTimeout(toastTimer)
    toastTimer = setTimeout(() => {
        toastMessage.value = ''
    }, 4000)
}

function getBaseEndpoint(): string {
    const ep = registryConfig.value?.endpoint || ''
    if (!ep) return ''
    return ep.endsWith('/') ? ep : `${ep}/`
}

function getRowId(row: any): string {
    return row?.task_id || row?.id || row?._id || ''
}

// Завантаження даних з бекенду
async function loadData() {
    const endpoint = getBaseEndpoint()
    if (!endpoint) return

    isTableLoading.value = true

    try {
        const params: Record<string, any> = {
            page: currentPage.value,
            limit: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            ...activeFilters.value,
        }

        if (searchQuery.value.trim()) {
            params.search = searchQuery.value.trim()
        }

        const { data } = await api.get<RegistryResponse>(endpoint, { params })

        if (data && Array.isArray(data.rows)) {
            total.value = data.total
            filtered.value = data.filtered
            rows.value = data.rows
        } else {
            total.value = 0
            filtered.value = 0
            rows.value = []
        }
    } catch (err: any) {
        console.error('Failed to load table data:', err)
        showToast('Не вдалося завантажити дані реєстру', 'error')
    } finally {
        isTableLoading.value = false
    }
}

// Оновлення даних користувачем
function refreshData() {
    loadData()
}

// Сортування стовпця
function handleSort(columnKey: string) {
    if (sortBy.value === columnKey) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
        sortBy.value = columnKey
        sortOrder.value = 'asc'
    }
    currentPage.value = 1
    loadData()
}

// Скидання фільтрів
function resetFilters() {
    searchQuery.value = ''
    currentPage.value = 1
    if (Object.keys(activeFilters.value).length > 0) {
        activeFilters.value = {}
    } else {
        loadData()
    }
}

// Слідкуємо за зміною сторінки або ліміту
watch([currentPage, pageSize], () => {
    if (isLoadingConfig.value) return
    loadData()
})

// Слідкуємо за фільтрами
watch(activeFilters, () => {
    if (isLoadingConfig.value) return
    currentPage.value = 1
    loadData()
}, { deep: true })

// Слідкуємо за пошуком із debounce
let searchDebounce: any = null
watch(searchQuery, () => {
    if (isLoadingConfig.value) return
    clearTimeout(searchDebounce)
    searchDebounce = setTimeout(() => {
        currentPage.value = 1
        loadData()
    }, 350)
})

// Відкриття модалок
function openCreateModal() {
    modalMode.value = 'create'
    selectedRow.value = null
    isRowModalOpen.value = true
}

function openEditModal(row: any) {
    modalMode.value = 'edit'
    selectedRow.value = { ...row }
    isRowModalOpen.value = true
}

function openDeleteModal(row: any) {
    rowToDelete.value = row
    isDeleteModalOpen.value = true
}

// Створення або редагування запису
async function handleRowSubmit(formData: Record<string, any>) {
    const baseEp = getBaseEndpoint()
    if (!baseEp) return

    isSubmitting.value = true
    try {
        if (modalMode.value === 'create') {
            await api.post(baseEp, formData)
            showToast('Запис успішно створено!', 'success')
        } else {
            const id = getRowId(selectedRow.value)
            await api.put(`${baseEp}${id}`, formData)
            showToast('Запис успішно оновлено!', 'success')
        }

        isRowModalOpen.value = false
        await loadData()
    } catch (err: any) {
        console.error('Failed to submit row:', err)
        const detail = err.response?.data?.detail
        const msg = typeof detail === 'string' ? detail : 'Помилка при збереженні запису'
        showToast(msg, 'error')
    } finally {
        isSubmitting.value = false
    }
}

// Видалення запису
async function handleConfirmDelete() {
    const baseEp = getBaseEndpoint()
    if (!baseEp || !rowToDelete.value) return

    const id = getRowId(rowToDelete.value)
    if (!id) return

    isDeleting.value = true
    try {
        await api.delete(`${baseEp}${id}`)
        showToast('Запис успішно видалено', 'success')
        isDeleteModalOpen.value = false
        rowToDelete.value = null
        await loadData()
    } catch (err: any) {
        console.error('Failed to delete row:', err)
        const detail = err.response?.data?.detail
        const msg = typeof detail === 'string' ? detail : 'Помилка при видаленні запису'
        showToast(msg, 'error')
    } finally {
        isDeleting.value = false
    }
}

// Динамічний пошук конфігів реєстрів (.ts)
const registryModules = import.meta.glob<{ default: RegistryConfig }>([
    '../config/*Registry.ts',
])

// Завантаження конфігу реєстру (tasksRegistry.ts тощо)
async function loadConfig(name: string) {
    if (!name) return
    configError.value = null

    try {
        const tsKey = `../config/${name}Registry.ts`

        const loader = registryModules[tsKey];
        if (!loader) {
            throw new Error(`Конфігурацію для "${name}" не знайдено`)
        }

        const module = await loader()
        registryConfig.value = module.default
        document.title = `${registryConfig.value?.title || name} | ДІЯ`

        columns.value = registryConfig.value?.columns || []
        registryFilters.value = registryConfig.value?.filters || []
        sortBy.value = registryConfig.value?.defaultSort?.sortBy || 'created_at'
        sortOrder.value = registryConfig.value?.defaultSort?.sortOrder || 'desc'

        currentPage.value = 1
        if (Object.keys(activeFilters.value).length > 0) {
            activeFilters.value = {}
        }
        searchQuery.value = ''

        await nextTick()
        isLoadingConfig.value = false

        await loadData()
    } catch (err) {
        console.error(`Failed to load config for: ${name}`, err)
        configError.value = `Конфігурацію для "${name}" не знайдено`
        registryConfig.value = null
        isLoadingConfig.value = false
    }
}

// Слідкуємо за зміною маршруту для завантаження конфігу
watch(
    alias,
    (newAlias) => {
        loadConfig(newAlias)
    },
    { immediate: true }
)
</script>
