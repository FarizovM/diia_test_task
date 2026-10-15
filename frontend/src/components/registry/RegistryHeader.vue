<template>
  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
    <!-- Ліва частина: Заголовок, підзаголовок та лічильник -->
    <div class="space-y-1">
      <div class="flex items-center gap-3">
        <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-diia-primary">
          {{ title }}
        </h1>
        <span
          class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white border border-gray-200 text-gray-700 shadow-xs">
          {{ filteredCount }}
          <span v-if="filteredCount !== totalCount" class="text-gray-400 ml-1">/ {{ totalCount }}</span>
        </span>
      </div>
      <p v-if="subtitle" class="text-sm text-gray-500">
        {{ subtitle }}
      </p>
    </div>

    <div class="flex items-center gap-2.5 self-start sm:self-auto">
      <button type="button" @click="$emit('refresh')" :disabled="isLoading"
        class="inline-flex items-center justify-center w-11 h-11 rounded-2xl bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:text-black transition-all shadow-xs active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
        title="Оновити дані">
        <svg class="w-4 h-4 transition-transform duration-500" :class="{ 'animate-spin': isLoading }" fill="none"
          stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>

      <button type="button" @click="$emit('add')"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-2xl bg-diia-dark hover:bg-black text-white text-sm font-semibold transition-all shadow-sm hover:shadow active:scale-95 cursor-pointer">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
        </svg>
        <span>Додати запис</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
  totalCount: number
  filteredCount: number
  isLoading: boolean
}>()

defineEmits<{
  (e: 'add'): void
  (e: 'refresh'): void
}>()
</script>
