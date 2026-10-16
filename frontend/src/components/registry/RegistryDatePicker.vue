<template>
  <div ref="datePickerRoot" class="relative">
    <!-- Тригер вибору дати у стилі Дія -->
    <button type="button" :disabled="disabled" @click="togglePicker"
      class="w-full bg-diia-light/50 border border-gray-200 rounded-2xl px-4 py-2.5 text-sm text-left flex items-center justify-between transition-all focus:outline-none focus:bg-white focus:border-black cursor-pointer hover:bg-gray-100/60 disabled:opacity-50 disabled:cursor-not-allowed"
      :class="{ 'border-black bg-white ring-1 ring-black/5': isOpen }">
      <div class="flex items-center gap-2.5 truncate">
        <!-- Іконка календаря Дія -->
        <svg class="w-4 h-4 text-gray-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
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
        <button v-if="modelValue" type="button" @click.stop="clearDate"
          class="p-1 rounded-full text-gray-400 hover:text-black hover:bg-gray-200/60 transition cursor-pointer"
          title="Очистити дату">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200"
          :class="{ 'rotate-180 text-black': isOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </button>

    <!-- Випадаючий календар Дія -->
    <Teleport to="body">
      <Transition name="dropdown">
        <div v-if="isOpen" ref="dropdownMenu" :style="pickerStyle"
          class="fixed z-[9999] w-80 bg-white rounded-3xl border border-gray-100 shadow-2xl p-4 ring-1 ring-black/5">
          <!-- Навігація по місяцях -->
          <div class="flex items-center justify-between pb-3 border-b border-gray-100">
            <button type="button" @click="prevMonth"
              class="w-8 h-8 rounded-full flex items-center justify-center text-gray-500 hover:text-black hover:bg-gray-100 transition cursor-pointer">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>

            <span class="text-sm font-bold text-diia-primary">
              {{ currentMonthName }} {{ viewYear }}
            </span>

            <button type="button" @click="nextMonth"
              class="w-8 h-8 rounded-full flex items-center justify-center text-gray-500 hover:text-black hover:bg-gray-100 transition cursor-pointer">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>

          <!-- Дні тижня -->
          <div class="grid grid-cols-7 gap-1 text-center py-2">
            <span v-for="dayName in weekDayNames" :key="dayName"
              class="text-[11px] font-semibold text-gray-400 uppercase">
              {{ dayName }}
            </span>
          </div>

          <!-- Сітка днів місяця -->
          <div class="grid grid-cols-7 gap-1 text-center pb-3">
            <button v-for="(day, idx) in calendarDays" :key="idx" type="button" @click="selectDay(day)"
              class="w-8 h-8 mx-auto flex items-center justify-center text-xs rounded-full transition-all cursor-pointer"
              :class="[
                day.isSelected
                  ? 'bg-diia-dark text-white font-bold shadow-xs'
                  : day.isToday
                    ? 'ring-1 ring-diia-dark/40 font-bold text-diia-primary hover:bg-gray-100'
                    : day.isCurrentMonth
                      ? 'text-gray-800 hover:bg-gray-100 font-medium'
                      : 'text-gray-300 hover:text-gray-500'
              ]">
              {{ day.dayNumber }}
            </button>
          </div>

          <!-- Вибір часу -->
          <div class="border-t border-gray-100 pt-3 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-500 font-medium flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Час виконання:
              </span>

              <!-- Інпути годин та хвилин -->
              <div class="flex items-center gap-1 bg-diia-light/60 border border-gray-200 rounded-xl px-2 py-0.5">
                <input ref="hoursInputRef" type="text" inputmode="numeric" maxlength="2" v-model="hoursDisplay"
                  @focus="onHoursFocus" @input="onHoursInput" @blur="onHoursBlur"
                  @keydown.up.prevent="stepHours(1)" @keydown.down.prevent="stepHours(-1)"
                  class="w-7 text-center text-xs font-bold text-diia-primary bg-transparent focus:outline-none focus:bg-white rounded transition" />
                <span class="text-gray-400 font-bold">:</span>
                <input ref="minutesInputRef" type="text" inputmode="numeric" maxlength="2" v-model="minutesDisplay"
                  @focus="onMinutesFocus" @input="onMinutesInput" @blur="onMinutesBlur"
                  @keydown.up.prevent="stepMinutes(1)" @keydown.down.prevent="stepMinutes(-1)"
                  class="w-7 text-center text-xs font-bold text-diia-primary bg-transparent focus:outline-none focus:bg-white rounded transition" />
              </div>
            </div>

            <!-- Швидкі пресети часу -->
            <div class="flex items-center gap-1.5 justify-end">
              <button v-for="preset in timePresets" :key="preset.label" type="button"
                @click="applyTimePreset(preset.h, preset.m)"
                class="px-2 py-0.5 rounded-lg text-[10px] font-medium transition cursor-pointer" :class="[
                  hours === preset.h && minutes === preset.m
                    ? 'bg-diia-dark text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                ]">
                {{ preset.label }}
              </button>
            </div>
          </div>

          <!-- Нижня панель дій -->
          <div class="border-t border-gray-100 pt-3 mt-3 flex items-center justify-between">
            <button type="button" @click="setToday"
              class="text-xs font-semibold text-gray-600 hover:text-black transition cursor-pointer">
              Сьогодні
            </button>

            <div class="flex items-center gap-2">
              <button type="button" @click="isOpen = false"
                class="px-3.5 py-1.5 rounded-xl bg-diia-dark hover:bg-black text-white text-xs font-semibold transition cursor-pointer">
                Готово
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
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
const dropdownMenu = ref<HTMLElement | null>(null)
const pickerStyle = ref<Record<string, string>>({})

const now = new Date()
const viewYear = ref(now.getFullYear())
const viewMonth = ref(now.getMonth())
const selectedDate = ref<Date | null>(null)
const hours = ref(18)
const minutes = ref(0)
const hoursDisplay = ref('18')
const minutesDisplay = ref('00')

const hoursInputRef = ref<HTMLInputElement | null>(null)
const minutesInputRef = ref<HTMLInputElement | null>(null)
const isHoursFocused = ref(false)
const isMinutesFocused = ref(false)

function syncDisplayTime(force = false) {
  if (force || !isHoursFocused.value) {
    hoursDisplay.value = String(hours.value).padStart(2, '0')
  }
  if (force || !isMinutesFocused.value) {
    minutesDisplay.value = String(minutes.value).padStart(2, '0')
  }
}

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
          syncDisplayTime()
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

function updatePickerPosition() {
  if (!datePickerRoot.value) return
  const rect = datePickerRoot.value.getBoundingClientRect()
  const spaceBelow = window.innerHeight - rect.bottom
  const spaceAbove = rect.top
  const calendarHeight = 390
  const openUpward = spaceBelow < calendarHeight && spaceAbove > spaceBelow

  const calendarWidth = 320
  let left = rect.left
  if (left + calendarWidth > window.innerWidth - 16) {
    left = Math.max(16, window.innerWidth - calendarWidth - 16)
  }

  const style: Record<string, string> = {
    position: 'fixed',
    left: `${left}px`,
    width: `${calendarWidth}px`,
    zIndex: '9999',
  }

  if (openUpward) {
    style.bottom = `${window.innerHeight - rect.top + 8}px`
    style.top = 'auto'
  } else {
    style.top = `${rect.bottom + 8}px`
    style.bottom = 'auto'
  }

  pickerStyle.value = style
}

function togglePicker() {
  if (props.disabled) return
  if (!isOpen.value) {
    updatePickerPosition()
    isOpen.value = true
  } else {
    isOpen.value = false
  }
}

function onScrollOrResize() {
  if (isOpen.value) {
    updatePickerPosition()
  }
}

watch(isOpen, (open) => {
  if (open) {
    updatePickerPosition()
    window.addEventListener('resize', onScrollOrResize)
    window.addEventListener('scroll', onScrollOrResize, true)
  } else {
    window.removeEventListener('resize', onScrollOrResize)
    window.removeEventListener('scroll', onScrollOrResize, true)
  }
})

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
  syncDisplayTime(true)
  if (!selectedDate.value) {
    selectedDate.value = new Date()
  }
  const d = new Date(selectedDate.value)
  d.setHours(h, m, 0, 0)
  selectedDate.value = d
  emitDate(d)
}

function onHoursFocus(e: FocusEvent) {
  isHoursFocused.value = true
  ;(e.target as HTMLInputElement)?.select()
}

function onMinutesFocus(e: FocusEvent) {
  isMinutesFocused.value = true
  ;(e.target as HTMLInputElement)?.select()
}

function onHoursInput() {
  hoursDisplay.value = hoursDisplay.value.replace(/\D/g, '').slice(0, 2)
  if (hoursDisplay.value.length === 2) {
    let val = parseInt(hoursDisplay.value, 10)
    if (!isNaN(val)) {
      val = Math.max(0, Math.min(23, val))
      hours.value = val
      hoursDisplay.value = String(val).padStart(2, '0')
      updateSelectedDateTime()
      minutesInputRef.value?.focus()
      minutesInputRef.value?.select()
    }
  }
}

function onHoursBlur() {
  isHoursFocused.value = false
  let val = parseInt(hoursDisplay.value, 10)
  if (isNaN(val) || val < 0) val = 0
  if (val > 23) val = 23
  hours.value = val
  hoursDisplay.value = String(val).padStart(2, '0')
  updateSelectedDateTime()
}

function onMinutesInput() {
  minutesDisplay.value = minutesDisplay.value.replace(/\D/g, '').slice(0, 2)
  if (minutesDisplay.value.length === 2) {
    let val = parseInt(minutesDisplay.value, 10)
    if (!isNaN(val)) {
      val = Math.max(0, Math.min(59, val))
      minutes.value = val
      minutesDisplay.value = String(val).padStart(2, '0')
      updateSelectedDateTime()
    }
  }
}

function onMinutesBlur() {
  isMinutesFocused.value = false
  let val = parseInt(minutesDisplay.value, 10)
  if (isNaN(val) || val < 0) val = 0
  if (val > 59) val = 59
  minutes.value = val
  minutesDisplay.value = String(val).padStart(2, '0')
  updateSelectedDateTime()
}

function stepHours(delta: number) {
  let h = hours.value + delta
  if (h > 23) h = 0
  if (h < 0) h = 23
  hours.value = h
  hoursDisplay.value = String(h).padStart(2, '0')
  updateSelectedDateTime()
}

function stepMinutes(delta: number) {
  let m = minutes.value + delta
  if (m > 59) m = 0
  if (m < 0) m = 59
  minutes.value = m
  minutesDisplay.value = String(m).padStart(2, '0')
  updateSelectedDateTime()
}

function updateSelectedDateTime() {
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
  syncDisplayTime(true)
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
  if (!isOpen.value) return
  const target = e.target as Node
  const isInsideTrigger = datePickerRoot.value && datePickerRoot.value.contains(target)
  const isInsideDropdown = dropdownMenu.value && dropdownMenu.value.contains(target)
  if (!isInsideTrigger && !isInsideDropdown) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', onScrollOrResize)
  window.removeEventListener('scroll', onScrollOrResize, true)
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
