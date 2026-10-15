<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs"
      @click.self="$emit('close')">
      <div
        class="bg-white rounded-3xl border border-gray-100 shadow-2xl w-full max-w-lg overflow-hidden transform transition-all">
        <!-- Шапка модалки -->
        <div class="px-6 sm:px-8 pt-6 pb-4 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h2 class="text-xl font-extrabold text-diia-primary">
              {{ mode === 'create' ? 'Додати запис' : 'Редагувати запис' }}
            </h2>
            <p class="text-xs text-gray-500 mt-0.5">
              {{ mode === 'create' ? 'Заповніть форму для створення нового запису' : `Внесіть необхідні зміни та
              збережіть` }}
            </p>
          </div>
          <button type="button" @click="$emit('close')"
            class="w-9 h-9 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-500 hover:text-black flex items-center justify-center transition cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Тіло форми на основі конфігурації колонок -->
        <form @submit.prevent="handleSubmit" class="p-6 sm:p-8 space-y-4 max-h-[75vh] overflow-y-auto">
          <div v-for="col in editableColumns" :key="col.key" class="space-y-1.5">
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700">
              {{ col.label }}
              <span v-if="col.required || col.key === 'title'" class="text-red-500">*</span>
            </label>

            <!-- 1. Textarea для великих текстових полів (тип 'textarea') -->
            <template v-if="col.type === 'textarea'">
              <textarea v-model="formData[col.key]" :rows="col.rows || 3"
                :placeholder="col.placeholder || `Введіть ${col.label.toLowerCase()}...`"
                :required="col.required || col.key === 'title'"
                class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 text-sm text-diia-primary focus:outline-none focus:bg-white focus:border-black transition resize-none"></textarea>
            </template>

            <!-- 2. Select для випадних списків / класифікаторів (тип 'select' або 'badge') -->
            <template v-else-if="col.type === 'select' || col.type === 'badge'">
              <RegistrySelect
                v-model="formData[col.key]"
                :options="col.options || []"
                :placeholder="col.placeholder || `Оберіть ${col.label.toLowerCase()}...`"
                :required="col.required"
              />
            </template>

            <!-- 3. Date / Datetime (тип 'date') -->
            <template v-else-if="col.type === 'date'">
              <RegistryDatePicker
                v-model="formData[col.key]"
                :placeholder="col.placeholder || `Оберіть ${col.label.toLowerCase()}...`"
                :required="col.required"
              />
            </template>

            <!-- 4. Числове поле (тип 'number') -->
            <template v-else-if="col.type === 'number'">
              <input type="number" v-model.number="formData[col.key]" :required="col.required"
                :placeholder="col.placeholder || `Введіть ${col.label.toLowerCase()}...`"
                class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 text-sm text-diia-primary focus:outline-none focus:bg-white focus:border-black transition" />
            </template>

            <!-- 5. Стандартний текстовий інпут (тип 'text' або за замовчуванням) -->
            <template v-else>
              <input type="text" v-model="formData[col.key]" :required="col.required || col.key === 'title'"
                :placeholder="col.placeholder || `Введіть ${col.label.toLowerCase()}...`"
                class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 text-sm text-diia-primary focus:outline-none focus:bg-white focus:border-black transition" />
            </template>
          </div>

          <!-- Помилка валідації/сервера -->
          <div v-if="localError" class="p-3 rounded-2xl bg-red-50 text-red-700 text-xs font-medium">
            {{ localError }}
          </div>

          <!-- Кнопки дій -->
          <div class="pt-4 flex items-center justify-end gap-3 border-t border-gray-100">
            <button type="button" @click="$emit('close')" :disabled="isSubmitting"
              class="px-5 py-2.5 rounded-2xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold transition cursor-pointer">
              Скасувати
            </button>
            <button type="submit" :disabled="isSubmitting"
              class="inline-flex items-center gap-2 px-6 py-2.5 rounded-2xl bg-diia-dark hover:bg-black text-white text-sm font-semibold transition shadow-sm active:scale-95 disabled:opacity-50 cursor-pointer">
              <svg v-if="isSubmitting" class="w-4 h-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span>{{ mode === 'create' ? 'Створити' : 'Зберегти' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { RegistryColumn } from '../../types/config'
import RegistrySelect from './RegistrySelect.vue'
import RegistryDatePicker from './RegistryDatePicker.vue'

const props = defineProps<{
  isOpen: boolean
  mode: 'create' | 'edit'
  columns: RegistryColumn[]
  initialData?: any
  isSubmitting?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'submit', payload: Record<string, any>): void
}>()

const formData = ref<Record<string, any>>({})
const localError = ref<string>('')

// Відображаємо в формі лише поля, які не позначені як системні або readonly
const editableColumns = computed(() => {
  return props.columns.filter((c) => {
    return !c.readonly && !['created_at', 'updated_at', 'task_id', 'id'].includes(c.key)
  })
})

watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      localError.value = ''
      const data: Record<string, any> = {}

      editableColumns.value.forEach((col) => {
        if (props.mode === 'edit' && props.initialData) {
          let val = props.initialData[col.key]
          // Якщо поле дати, конвертуємо в формат для input datetime-local YYYY-MM-DDTHH:mm
          if (col.type === 'date' && val) {
            try {
              const d = new Date(val)
              val = new Date(d.getTime() - d.getTimezoneOffset() * 60000)
                .toISOString()
                .slice(0, 16)
            } catch {
              // ignore
            }
          }
          data[col.key] = val ?? ''
        } else {
          // Для нового запису: перевіряємо defaultValue, далі options для select, або порожній рядок
          if (col.defaultValue !== undefined) {
            data[col.key] = col.defaultValue
          } else if (col.options && col.options.length > 0) {
            data[col.key] = col.options[0].key || ''
          } else {
            data[col.key] = ''
          }
        }
      })

      formData.value = data
    }
  },
  { immediate: true }
)

function handleSubmit() {
  localError.value = ''

  // Перевірка обов'язкових полів з конфігурації
  for (const col of editableColumns.value) {
    if (col.required || col.key === 'title') {
      const val = formData.value[col.key]
      if (val === undefined || val === null || String(val).trim() === '') {
        localError.value = `Поле «${col.label}» обов'язкове для заповнення`
        return
      }
    }
  }

  // Очищення та приведення типів даних на основі col.type перед відправкою
  const payload: Record<string, any> = { ...formData.value }
  editableColumns.value.forEach((col) => {
    if (col.type === 'date') {
      if (payload[col.key]) {
        payload[col.key] = new Date(payload[col.key]).toISOString()
      } else {
        payload[col.key] = null
      }
    } else if (col.type === 'number') {
      if (payload[col.key] !== '' && payload[col.key] !== null && payload[col.key] !== undefined) {
        payload[col.key] = Number(payload[col.key])
      } else {
        payload[col.key] = null
      }
    }
  })

  emit('submit', payload)
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.98);
}
</style>
