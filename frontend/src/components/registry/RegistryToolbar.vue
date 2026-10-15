<template>
  <div class="relative z-20 bg-white rounded-3xl p-4 sm:p-5 border border-gray-200/90 shadow-xs mb-7 space-y-4">
    <div class="flex flex-col lg:flex-row lg:items-center gap-3">
      <!-- Пошуковий рядок у стилі Дія -->
      <div class="relative flex-1">
        <span class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </span>
        <input :value="search" @input="$emit('update:search', ($event.target as HTMLInputElement).value)" type="text"
          :placeholder="searchPlaceholder || 'Пошук у реєстрі...'"
          class="w-full bg-diia-light/60 border border-gray-200 rounded-2xl pl-11 pr-10 py-2.5 text-sm text-diia-primary placeholder-gray-400 focus:outline-none focus:bg-white focus:border-black transition-all" />
        <button v-if="search" type="button" @click="$emit('update:search', '')"
          class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-black transition focus:outline-none cursor-pointer"
          title="Очистити пошук">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Селектори фільтрів у стилі Дія -->
      <div class="flex flex-wrap items-center gap-2.5">
        <div v-for="filter in filters" :key="filter.key" class="min-w-[170px] sm:min-w-[195px]">
          <RegistrySelect
            :model-value="activeFilters[filter.key] || ''"
            :options="getFilterOptions(filter)"
            :placeholder="`${filter.label}: Всі`"
            :active="Boolean(activeFilters[filter.key])"
            @update:model-value="onFilterChange(filter.key, $event)"
          />
        </div>

        <!-- Кнопка скидання фільтрів -->
        <button v-if="hasActiveFilters || search" type="button" @click="$emit('reset')"
          class="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-2xl bg-gray-100 hover:bg-gray-200 text-xs sm:text-sm font-medium text-gray-700 transition active:scale-95 cursor-pointer">
          <svg class="w-3.5 h-3.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <span>Скинути</span>
        </button>
      </div>
    </div>

    <!-- Бейджі активних фільтрів -->
    <div v-if="hasActiveFilters" class="flex flex-wrap items-center gap-2 pt-2 border-t border-gray-100">
      <span class="text-xs text-gray-400 font-medium mr-1">Застосовано:</span>
      <span v-for="(val, key) in activeFilters" :key="key" v-show="val"
        class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-diia-dark text-white shadow-xs">
        <span>{{ getFilterLabel(key) }}: {{ getOptionLabel(key, val) }}</span>
        <button type="button" @click="onFilterChange(String(key), '')"
          class="hover:text-diia-accent transition focus:outline-none cursor-pointer">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { RegistryFilter, SelectOption } from '../../types/config'
import RegistrySelect from './RegistrySelect.vue'

const props = defineProps<{
  searchPlaceholder?: string
  filters: RegistryFilter[]
  search: string
  activeFilters: Record<string, string>
}>()

const emit = defineEmits<{
  (e: 'update:search', val: string): void
  (e: 'update:activeFilters', val: Record<string, string>): void
  (e: 'reset'): void
}>()

const hasActiveFilters = computed(() => {
  return Object.values(props.activeFilters).some((val) => Boolean(val))
})

function onFilterChange(key: string, value: string) {
  const next = { ...props.activeFilters }
  if (value) {
    next[key] = value
  } else {
    delete next[key]
  }
  emit('update:activeFilters', next)
}

function getFilterLabel(key: string | number): string {
  const f = props.filters.find((item) => item.key === String(key))
  return f?.label || String(key)
}

function getOptionLabel(key: string | number, val: string): string {
  const f = props.filters.find((item) => item.key === String(key))
  const opt = f?.options.find((o) => (o.key) === val)
  return opt?.label || val
}

function getFilterOptions(filter: RegistryFilter): SelectOption<any>[] {
  return [
    { key: '', label: `${filter.label}: Всі` },
    ...filter.options,
  ]
}
</script>
