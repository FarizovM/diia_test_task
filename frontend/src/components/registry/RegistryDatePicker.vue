<template>
  <div ref="datePickerRoot" class="relative">
    <!-- Тригер вибору дати у стилі Дія -->
    <button
      type="button"
      :disabled="disabled"
      @click="togglePicker"
      class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 text-sm text-left flex items-center justify-between transition-all focus:outline-none focus:bg-white focus:border-black cursor-pointer hover:bg-gray-100/60 disabled:opacity-50 disabled:cursor-not-allowed"
      :class="{ 'border-black bg-white ring-1 ring-black/5': isOpen }"
    >
      <div class="flex items-center gap-2.5 truncate">
        <!-- Іконка календаря Дія -->
        <svg
          class="w-4 h-4 text-gray-500 shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.8"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>

        <!-- Відформатована дата або плейсхолдер -->
        <span v-if="displayLabel" class="text-sm font-semibold text-diia-primary truncate">
          {{ displayLabel }}
        </span>
        <span v-else class="text-sm text-gray-400">
          {{ placeholder || 'Оберіть дату та час...' }}
        </span>
      </div>

      <!-- Кнопка очищення або стрілочка -->
      <div class="flex items-center gap-1.5 ml-2 shrink-0">
        <button
          v-if="modelValue"
          type="button"
          @click.stop="clearDate"
          class="p-1 rounded-full text-gray-400 hover:text-black hover:bg-gray-200/60 transition cursor-pointer"
          title="Очистити дату"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <svg
          class="w-4 h-4 text-gray-400 transition-transform duration-200"
          :class="{ 'rotate-180 text-black': isOpen }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </button>

    <!-- Випадаючий календар Дія -->
    <Transition name="dropdown">
      <div
        v-if="isOpen"
        class="absolute left-0 z-50 w-80 bg-white rounded-3xl border border-gray-100 shadow-2xl p-4 ring-1 ring-black/5"
        :class="openUpward ? 'bottom-full mb-2' : 'top-full mt-2'"
      >
        <!-- Навігація по місяцях -->
        <div class="flex items-center justify-between pb-3 border-b border-gray-100">
          <button
            type="button"
            @click="prevMonth"
            class="w-8 h-8 rounded-full flex items-center justify-center text-gray-500 hover:text-black hover:bg-gray-100 transition cursor-pointer"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>

          <span class="text-sm font-bold text-diia-primary">
            {{ currentMonthName }} {{ viewYear }}
          </span>

          <button
            type="button"
            @click="nextMonth"
            class="w-8 h-8 rounded-full flex items-center justify-center text-gray-500 hover:text-black hover:bg-gray-100 transition cursor-pointer"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <!-- Дні тижня -->
        <div class="grid grid-cols-7 gap-1 text-center py-2">
          <span
            v-for="dayName in weekDayNames"
            :key="dayName"
            class="text-[11px] font-semibold text-gray-400 uppercase"
          >
            {{ dayName }}
          </span>
        </div>

        <!-- Сітка днів місяця -->
        <div class="grid grid-cols-7 gap-1 text-center pb-3">
          <button
            v-for="(day, idx) in calendarDays"
            :key="idx"
            type="button"
            @click="selectDay(day)"
            class="w-8 h-8 mx-auto flex items-center justify-center text-xs rounded-full transition-all cursor-pointer"
            :class="[
              day.isSelected
                ? 'bg-diia-dark text-white font-bold shadow-xs'
                : day.isToday
                ? 'ring-1 ring-diia-dark/40 font-bold text-diia-primary hover:bg-gray-100'
                : day.isCurrentMonth
                ? 'text-gray-800 hover:bg-gray-100 font-medium'
                : 'text-gray-300 hover:text-gray-500'
            ]"
          >
            {{ day.dayNumber }}
          </button>
        </div>

        <!-- Вибір часу -->
        <div class="border-t border-gray-100 pt-3 space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-500 font-medium flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Час виконання:
            </span>

            <!-- Інпути годин та хвилин -->
            <div class="flex items-center gap-1 bg-diia-light/60 border border-gray-200 rounded-xl px-2 py-0.5">
              <input
                type="number"
                min="0"
                max="23"
                v-model.number="hours"
                @change="onTimeInputChange"
                class="w-7 text-center text-xs font-bold text-diia-primary bg-transparent focus:outline-none"
              />
              <span class="text-gray-400 font-bold">:</span>
              <input
                type="number"
                min="0"
                max="59"
                v-model.number="minutes"
                @change="onTimeInputChange"
                class="w-7 text-center text-xs font-bold text-diia-primary bg-transparent focus:outline-none"
              />
            </div>
          </div>

          <!-- Швидкі пресети часу -->
          <div class="flex items-center gap-1.5 justify-end">
            <button
              v-for="preset in timePresets"
              :key="preset.label"
              type="button"
              @click="applyTimePreset(preset.h, preset.m)"
              class="px-2 py-0.5 rounded-lg text-[10px] font-medium transition cursor-pointer"
              :class="[
                hours === preset.h && minutes === preset.m
                  ? 'bg-diia-dark text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              {{ preset.label }}
            </button>
          </div>
        </div>

        <!-- Нижня панель дій -->
        <div class="border-t border-gray-100 pt-3 mt-3 flex items-center justify-between">
          <button
            type="button"
            @click="setToday"
            class="text-xs font-semibold text-gray-600 hover:text-black transition cursor-pointer"
          >
            Сьогодні
          </button>

          <div class="flex items-center gap-2">
            <button
              type="button"
              @click="isOpen = false"
              class="px-3.5 py-1.5 rounded-xl bg-diia-dark hover:bg-black text-white text-xs font-semibold transition cursor-pointer"
            >
              Готово
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  modelValue?: string | null
  placeholder?: string
  required?: boolean
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: string | null): void
}>()

const isOpen = ref(false)
const datePickerRoot = ref<HTMLElement | null>(null)

const now = new Date()
const viewYear = ref(now.getFullYear())
const viewMonth = ref(now.getMonth())
const selectedDate = ref<Date | null>(null)
const hours = ref(18)
const minutes = ref(0)

const weekDayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
const monthNames = [
  'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
  'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'
]

const timePresets = [
  { label: '09:00', h: 9, m: 0 },
  { label: '13:00', h: 13, m: 0 },
  { label: '18:00', h: 18, m: 0 },
  { label: '23:59', h: 23, m: 59 },
]

const currentMonthName = computed(() => monthNames[viewMonth.value] || '')

// Відформатований рядок для кнопки
const displayLabel = computed(() => {
  if (!props.modelValue) return ''
  try {
    const d = new Date(props.modelValue)
    if (isNaN(d.getTime())) return String(props.modelValue)

    const day = d.getDate()
    const genitiveMonths = [
      'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
      'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
    ]
    const mStr = genitiveMonths[d.getMonth()]
    const y = d.getFullYear()
    const h = String(d.getHours()).padStart(2, '0')
    const m = String(d.getMinutes()).padStart(2, '0')
    return `${day} ${mStr} ${y}, ${h}:${m}`
  } catch {
    return String(props.modelValue)
  }
})

interface CalendarDay {
  date: Date
  dayNumber: number
  isCurrentMonth: boolean
  isToday: boolean
  isSelected: boolean
}

// Генерація днів сітки календаря
const calendarDays = computed<CalendarDay[]>(() => {
  const year = viewYear.value
  const month = viewMonth.value

  const firstDay = new Date(year, month, 1)
  let startDayOfWeek = firstDay.getDay() - 1
  if (startDayOfWeek < 0) startDayOfWeek = 6

  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const daysInPrevMonth = new Date(year, month, 0).getDate()

  const today = new Date()
  const isSameDate = (d1: Date, d2: Date) =>
    d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate()

  const days: CalendarDay[] = []

  // Дні попереднього місяця
  for (let i = startDayOfWeek - 1; i >= 0; i--) {
    const d = new Date(year, month - 1, daysInPrevMonth - i)
    days.push({
      date: d,
      dayNumber: daysInPrevMonth - i,
      isCurrentMonth: false,
      isToday: isSameDate(d, today),
      isSelected: selectedDate.value ? isSameDate(d, selectedDate.value) : false,
    })
  }

  // Дні поточного місяця
  for (let i = 1; i <= daysInMonth; i++) {
    const d = new Date(year, month, i)
    days.push({
      date: d,
      dayNumber: i,
      isCurrentMonth: true,
      isToday: isSameDate(d, today),
      isSelected: selectedDate.value ? isSameDate(d, selectedDate.value) : false,
    })
  }

  // Дні наступного місяця для завершення рядків (кратне 7)
  const remaining = 7 - (days.length % 7)
  if (remaining < 7) {
    for (let i = 1; i <= remaining; i++) {
      const d = new Date(year, month + 1, i)
      days.push({
        date: d,
        dayNumber: i,
        isCurrentMonth: false,
        isToday: isSameDate(d, today),
        isSelected: selectedDate.value ? isSameDate(d, selectedDate.value) : false,
      })
    }
  }

  return days
})

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      try {
        const d = new Date(val)
        if (!isNaN(d.getTime())) {
          selectedDate.value = d
          viewYear.value = d.getFullYear()
          viewMonth.value = d.getMonth()
          hours.value = d.getHours()
          minutes.value = d.getMinutes()
          return
        }
      } catch {
        // ignore
      }
    }
    selectedDate.value = null
  },
  { immediate: true }
)

const openUpward = ref(false)

function togglePicker() {
  if (props.disabled) return
  if (!isOpen.value && datePickerRoot.value) {
    const rect = datePickerRoot.value.getBoundingClientRect()
    openUpward.value = window.innerHeight - rect.bottom < 380
  }
  isOpen.value = !isOpen.value
}

function prevMonth() {
  if (viewMonth.value === 0) {
    viewMonth.value = 11
    viewYear.value--
  } else {
    viewMonth.value--
  }
}

function nextMonth() {
  if (viewMonth.value === 11) {
    viewMonth.value = 0
    viewYear.value++
  } else {
    viewMonth.value++
  }
}

function selectDay(day: CalendarDay) {
  const d = new Date(day.date)
  d.setHours(hours.value, minutes.value, 0, 0)
  selectedDate.value = d
  viewYear.value = d.getFullYear()
  viewMonth.value = d.getMonth()
  emitDate(d)
}

function applyTimePreset(h: number, m: number) {
  hours.value = h
  minutes.value = m
  if (!selectedDate.value) {
    selectedDate.value = new Date()
  }
  const d = new Date(selectedDate.value)
  d.setHours(h, m, 0, 0)
  selectedDate.value = d
  emitDate(d)
}

function onTimeInputChange() {
  hours.value = Math.max(0, Math.min(23, Number(hours.value) || 0))
  minutes.value = Math.max(0, Math.min(59, Number(minutes.value) || 0))
  if (selectedDate.value) {
    const d = new Date(selectedDate.value)
    d.setHours(hours.value, minutes.value, 0, 0)
    selectedDate.value = d
    emitDate(d)
  }
}

function setToday() {
  const d = new Date()
  viewYear.value = d.getFullYear()
  viewMonth.value = d.getMonth()
  hours.value = d.getHours()
  minutes.value = d.getMinutes()
  selectedDate.value = d
  emitDate(d)
}

function clearDate() {
  selectedDate.value = null
  emit('update:modelValue', null)
  isOpen.value = false
}

function emitDate(d: Date) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const h = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  emit('update:modelValue', `${y}-${m}-${day}T${h}:${min}`)
}

function handleClickOutside(e: MouseEvent) {
  if (datePickerRoot.value && !datePickerRoot.value.contains(e.target as Node)) {
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
