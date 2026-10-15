<template>
  <div ref="selectRoot" class="relative">
    <!-- Кнопка відкриття випадалки у стилі Дія -->
    <button type="button" :disabled="disabled" @click="toggleDropdown"
      class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 text-sm text-left flex items-center justify-between transition-all focus:outline-none focus:bg-white focus:border-black cursor-pointer hover:bg-gray-100/60 disabled:opacity-50 disabled:cursor-not-allowed"
      :class="{
        'border-black bg-white ring-1 ring-black/5': isOpen,
        'border-black/70 bg-white shadow-2xs': active && !isOpen
      }">
      <!-- Контент обраного елемента -->
      <div class="flex items-center gap-2 truncate">
        <!-- Якщо обрано і є стиль бейджа -->
        <span v-if="selectedOption?.style"
          class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold shrink-0"
          :class="selectedOption.style">
          <span v-if="selectedOption.icon" class="w-3.5 h-3.5 inline-flex items-center justify-center shrink-0"
            v-html="selectedOption.icon"></span>
          <span>{{ selectedOption.label }}</span>
        </span>

        <!-- Якщо обрано і є тільки іконка -->
        <template v-else-if="selectedOption?.icon">
          <span class="w-4 h-4 inline-flex items-center justify-center shrink-0 text-diia-primary"
            v-html="selectedOption.icon"></span>
          <span class="text-sm font-semibold text-diia-primary truncate">
            {{ selectedOption.label }}
          </span>
        </template>

        <!-- Якщо обрано звичайний варіант -->
        <span v-else-if="selectedOption" class="text-sm font-semibold text-diia-primary truncate">
          {{ selectedOption.label }}
        </span>

        <!-- Плейсхолдер, якщо нічого не обрано -->
        <span v-else class="text-sm text-gray-400">
          {{ placeholder || 'Оберіть значення...' }}
        </span>
      </div>

      <!-- Шеврон зі зміною напрямку -->
      <span class="ml-2 flex items-center pointer-events-none text-gray-400">
        <svg class="w-4 h-4 transition-transform duration-200" :class="{ 'rotate-180 text-black': isOpen }" fill="none"
          stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </span>
    </button>

    <!-- Випадаючий список -->
    <Transition name="dropdown">
      <div v-if="isOpen"
        class="absolute left-0 right-0 z-50 bg-white rounded-2xl border border-gray-100 shadow-2xl p-1.5 max-h-60 overflow-y-auto space-y-1 ring-1 ring-black/5"
        :class="openUpward ? 'bottom-full mb-1.5' : 'top-full mt-1.5'">
        <button v-for="opt in options" :key="String(opt.key)" type="button" @click="selectOption(opt)"
          class="w-full px-3 py-2 rounded-xl text-left text-sm flex items-center justify-between transition cursor-pointer hover:bg-gray-100/70"
          :class="{ 'bg-gray-100 font-semibold': isSelected(opt) }">
          <div class="flex items-center gap-2 truncate">
            <!-- Якщо у класифікатора є бейдж стиль -->
            <span v-if="opt.style"
              class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold shrink-0"
              :class="opt.style">
              <span v-if="opt.icon" class="w-3.5 h-3.5 inline-flex items-center justify-center shrink-0"
                v-html="opt.icon"></span>
              <span>{{ opt.label }}</span>
            </span>

            <!-- Якщо є тільки іконка -->
            <template v-else-if="opt.icon">
              <span class="w-4 h-4 inline-flex items-center justify-center shrink-0" v-html="opt.icon"></span>
              <span class="text-diia-primary truncate">{{ opt.label }}</span>
            </template>

            <!-- Звичайний текстовий пункт -->
            <span v-else class="text-diia-primary truncate">{{ opt.label }}</span>
          </div>

          <!-- Галочка активного пункту -->
          <svg v-if="isSelected(opt)" class="w-4 h-4 text-black shrink-0 ml-2" fill="none" stroke="currentColor"
            viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          </svg>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { SelectOption } from '../../types/config'

const props = defineProps<{
  modelValue?: any
  options: SelectOption<any>[]
  placeholder?: string
  required?: boolean
  disabled?: boolean
  active?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: any): void
}>()

const isOpen = ref(false)
const selectRoot = ref<HTMLElement | null>(null)

const selectedOption = computed(() => {
  if (props.modelValue === undefined || props.modelValue === null) {
    return null
  }
  const valStr = String(props.modelValue).toLowerCase()
  return (
    props.options.find(
      (opt) => String(opt.key).toLowerCase() === valStr
    ) || null
  )
})

function isSelected(opt: SelectOption<any>): boolean {
  if (props.modelValue === undefined || props.modelValue === null) return false
  const optVal = String(opt.key).toLowerCase()
  return String(props.modelValue).toLowerCase() === optVal
}

const openUpward = ref(false)

function toggleDropdown() {
  if (props.disabled) return
  if (!isOpen.value && selectRoot.value) {
    const rect = selectRoot.value.getBoundingClientRect()
    openUpward.value = window.innerHeight - rect.bottom < 260
  }
  isOpen.value = !isOpen.value
}

function selectOption(opt: SelectOption<any>) {
  if (props.disabled) return
  emit('update:modelValue', opt.key)
  isOpen.value = false
}

function handleClickOutside(e: MouseEvent) {
  if (selectRoot.value && !selectRoot.value.contains(e.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
}
</style>
