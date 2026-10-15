<template>
  <div class="px-6 py-4 bg-gray-50/70 border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-4 select-none">
    <!-- Ліва частина: Інформація про записи -->
    <div class="text-xs sm:text-sm text-gray-500 order-2 sm:order-1">
      <span v-if="filtered > 0">
        Показано
        <span class="font-semibold text-gray-900">{{ fromRecord }}</span>
        –
        <span class="font-semibold text-gray-900">{{ toRecord }}</span>
        з
        <span class="font-semibold text-gray-900">{{ filtered }}</span>
        записів
      </span>
      <span v-else>
        Немає записів для відображення
      </span>
    </div>

    <!-- Центральна/Права частина: Кнопки сторінок та вибір розміру -->
    <div class="flex flex-wrap items-center gap-4 order-1 sm:order-2">
      <!-- Вибір кількості на сторінці -->
      <div class="flex items-center gap-2 text-xs sm:text-sm text-gray-500">
        <span>Рядків:</span>
        <select
          :value="pageSize"
          @change="$emit('update:pageSize', Number(($event.target as HTMLSelectElement).value))"
          class="bg-white border border-gray-200 rounded-xl px-2.5 py-1 text-xs font-medium text-gray-900 focus:outline-none focus:border-black transition cursor-pointer"
        >
          <option v-for="size in pageSizeOptions" :key="size" :value="size">
            {{ size }}
          </option>
        </select>
      </div>

      <!-- Кнопки перемикання сторінок -->
      <nav class="inline-flex items-center gap-1">
        <!-- Попередня -->
        <button
          type="button"
          @click="changePage(currentPage - 1)"
          :disabled="currentPage <= 1"
          class="w-8 h-8 inline-flex items-center justify-center rounded-xl border border-gray-200 bg-white text-gray-600 hover:bg-gray-100 hover:text-black transition disabled:opacity-30 disabled:pointer-events-none cursor-pointer"
          title="Попередня сторінка"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- Номери сторінок -->
        <template v-for="(page, idx) in visiblePages" :key="idx">
          <span
            v-if="page === '...'"
            class="w-7 text-center text-xs text-gray-400 font-bold"
          >
            …
          </span>
          <button
            v-else
            type="button"
            @click="changePage(Number(page))"
            class="min-w-8 h-8 px-2 text-xs font-semibold rounded-xl transition cursor-pointer"
            :class="[
              currentPage === page
                ? 'bg-diia-dark text-white shadow-xs'
                : 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-100 hover:text-black'
            ]"
          >
            {{ page }}
          </button>
        </template>

        <!-- Наступна -->
        <button
          type="button"
          @click="changePage(currentPage + 1)"
          :disabled="currentPage >= totalPages"
          class="w-8 h-8 inline-flex items-center justify-center rounded-xl border border-gray-200 bg-white text-gray-600 hover:bg-gray-100 hover:text-black transition disabled:opacity-30 disabled:pointer-events-none cursor-pointer"
          title="Наступна сторінка"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    currentPage: number
    pageSize: number
    total: number
    filtered: number
    pageSizeOptions?: number[]
  }>(),
  {
    pageSizeOptions: () => [10, 20, 50],
  }
)

const emit = defineEmits<{
  (e: 'update:currentPage', page: number): void
  (e: 'update:pageSize', size: number): void
}>()

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.filtered / props.pageSize))
})

const fromRecord = computed(() => {
  if (props.filtered === 0) return 0
  return (props.currentPage - 1) * props.pageSize + 1
})

const toRecord = computed(() => {
  return Math.min(props.currentPage * props.pageSize, props.filtered)
})

function changePage(page: number) {
  if (page >= 1 && page <= totalPages.value && page !== props.currentPage) {
    emit('update:currentPage', page)
  }
}

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const total = totalPages.value
  const current = props.currentPage

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
    return pages
  }

  pages.push(1)

  if (current > 3) {
    pages.push('...')
  }

  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  if (current < total - 2) {
    pages.push('...')
  }

  pages.push(total)

  return pages
})
</script>
