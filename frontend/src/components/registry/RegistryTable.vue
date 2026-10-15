<template>
  <div class="bg-white rounded-3xl border border-gray-200/90 shadow-xs overflow-hidden relative">
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse table-fixed min-w-[800px]">
        <!-- Заголовки стовпців -->
        <thead>
          <tr
            class="border-b border-gray-100 bg-gray-50/70 text-xs font-bold text-gray-500 uppercase tracking-wider select-none">
            <th v-for="col in visibleColumns" :key="col.key" :style="col.width ? { width: col.width } : {}"
              @click="onHeaderClick(col)" class="px-6 py-6 transition-colors" :class="[
                col.sortable !== false ? 'cursor-pointer hover:bg-gray-100/60 hover:text-black' : '',
                sortBy === col.key ? 'text-black font-extrabold' : ''
              ]">
              <div class="flex items-center gap-2">
                <span>{{ col.label }}</span>
                <span v-if="col.sortable !== false" class="text-gray-400">
                  <svg v-if="sortBy === col.key" class="w-3.5 h-3.5 transition-transform"
                    :class="{ 'rotate-180': sortOrder === 'desc' }" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7" />
                  </svg>
                  <svg v-else class="w-3.5 h-3.5 opacity-0 group-hover:opacity-100" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 10l5 5 5-5" />
                  </svg>
                </span>
              </div>
            </th>

            <!-- Стовпець дій -->
            <th class="px-6 py-6 text-right w-24">
              Дії
            </th>
          </tr>
        </thead>

        <!-- Тіло таблиці -->
        <tbody
          class="divide-y divide-gray-100 text-sm transition-opacity duration-150"
          :class="{ 'opacity-60 pointer-events-none': isLoading && rows.length > 0 }"
        >
          <!-- Стан початкового завантаження (скелетон відображається тільки якщо рядків ще немає) -->
          <template v-if="isLoading && rows.length === 0">
            <tr v-for="i in 10" :key="'skeleton-' + i" class="animate-pulse">
              <td v-for="col in visibleColumns" :key="col.key" class="px-6 py-4.5">
                <div class="h-4 bg-gray-100 rounded-lg w-3/4"></div>
              </td>
              <td class="px-6 py-4.5 text-right">
                <div class="inline-flex gap-2">
                  <div class="w-8 h-8 bg-gray-100 rounded-xl"></div>
                  <div class="w-8 h-8 bg-gray-100 rounded-xl"></div>
                </div>
              </td>
            </tr>
          </template>

          <!-- Порожній стан -->
          <tr v-else-if="rows.length === 0">
            <td :colspan="visibleColumns.length + 1" class="px-6 py-16 text-center">
              <div class="flex flex-col items-center justify-center max-w-sm mx-auto space-y-3">
                <div class="w-14 h-14 rounded-2xl bg-gray-100 text-gray-400 flex items-center justify-center">
                  <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 class="text-base font-bold text-gray-900">Записів не знайдено</h3>
                <p class="text-xs text-gray-500">
                  Спробуйте змінити фільтри чи параметри пошуку або додайте новий запис.
                </p>
              </div>
            </td>
          </tr>

          <!-- Рядки з даними -->
          <tr v-else v-for="(row, idx) in rows" :key="getRowKey(row, idx)" class="hover:bg-gray-50/70 transition-colors group">
            <td v-for="col in visibleColumns" :key="col.key" class="px-6 py-4 align-middle">
              <!-- Тип: select / badge -->
              <template v-if="col.type === 'select' || col.type === 'badge'">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium"
                  :class="getOptionStyle(col, row[col.key])">
                  <span v-if="getOptionIcon(col, row[col.key])"
                    class="w-3.5 h-3.5 inline-flex items-center justify-center"
                    v-html="getOptionIcon(col, row[col.key])"></span>
                  <span>{{ getOptionLabel(col, row[col.key]) }}</span>
                </span>
              </template>

              <!-- Тип: date -->
              <template v-else-if="col.type === 'date'">
                <span class="text-gray-600 font-mono text-xs">
                  {{ formatDate(row[col.key]) }}
                </span>
              </template>

              <!-- Тип: text з жирним шрифтом або звичайний -->
              <template v-else>
                <span :class="[
                  col.bold ? 'font-bold text-diia-primary' : 'text-gray-700',
                  'line-clamp-2'
                ]" :title="row[col.key] || '—'">
                  {{ row[col.key] || '—' }}
                </span>
              </template>
            </td>

            <!-- Кнопки дій: Редагувати та Видалити -->
            <td class="px-6 py-4 align-middle text-right whitespace-nowrap">
              <div class="inline-flex items-center gap-1.5">
                <button type="button" @click="$emit('edit', row)"
                  class="p-2 rounded-xl text-gray-500 hover:text-black hover:bg-gray-100 transition active:scale-95 cursor-pointer"
                  title="Редагувати">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>

                <button type="button" @click="$emit('delete', row)"
                  class="p-2 rounded-xl text-gray-500 hover:text-red-600 hover:bg-red-50 transition active:scale-95 cursor-pointer"
                  title="Видалити">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Слот пагінації внизу таблиці -->
    <slot name="pagination"></slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { RegistryColumn } from '../../types/config'

const props = defineProps<{
  columns: RegistryColumn[]
  rows: any[]
  isLoading: boolean
  sortBy: string
  sortOrder: 'asc' | 'desc'
  primaryKey?: string
}>()

const emit = defineEmits<{
  (e: 'sort', columnKey: string): void
  (e: 'edit', row: any): void
  (e: 'delete', row: any): void
}>()

const visibleColumns = computed(() => {
  return props.columns.filter((c) => !c.hidden)
})

function onHeaderClick(col: RegistryColumn) {
  if (col.sortable !== false) {
    emit('sort', col.key)
  }
}

function getRowKey(row: any, idx: number): string | number {
  if (props.primaryKey && row[props.primaryKey]) return row[props.primaryKey]
  return row.task_id || row.id || row._id || idx
}

function getOption(col: RegistryColumn, val: any) {
  if (!col.options || val === undefined || val === null) return null
  const strVal = String(val).toLowerCase()
  return col.options.find(
    (o) => String(o.key).toLowerCase() === strVal
  )
}

function getOptionLabel(col: RegistryColumn, val: any): string {
  const opt = getOption(col, val)
  return opt?.label || String(val ?? '—')
}

function getOptionStyle(col: RegistryColumn, val: any): string {
  const opt = getOption(col, val)
  return opt?.style || 'bg-gray-100 text-gray-800'
}

function getOptionIcon(col: RegistryColumn, val: any): string | undefined {
  const opt = getOption(col, val)
  return opt?.icon
}

function formatDate(val: any): string {
  if (!val) return '—'
  try {
    const d = new Date(val)
    if (isNaN(d.getTime())) return String(val)
    return new Intl.DateTimeFormat('uk-UA', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(d)
  } catch {
    return String(val)
  }
}
</script>
