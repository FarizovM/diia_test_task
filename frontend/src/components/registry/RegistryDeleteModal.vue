<template>
  <Transition name="fade">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs"
      @click.self="$emit('close')"
    >
      <div
        class="bg-white rounded-3xl border border-gray-100 shadow-2xl w-full max-w-md overflow-hidden transform transition-all p-6 sm:p-7 text-center"
      >
        <div class="w-12 h-12 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.8"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </div>

        <h3 class="text-lg font-bold text-gray-900 mb-1.5">
          Видалити запис?
        </h3>
        <p class="text-xs sm:text-sm text-gray-500 mb-6">
          Ви збираєтеся видалити
          <span v-if="itemTitle" class="font-bold text-gray-800">«{{ itemTitle }}»</span><span v-else>цей запис</span>.
          Цю дію неможливо скасувати.
        </p>

        <div class="flex items-center justify-center gap-3">
          <button
            type="button"
            @click="$emit('close')"
            :disabled="isDeleting"
            class="w-1/2 py-2.5 rounded-2xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold transition cursor-pointer"
          >
            Скасувати
          </button>
          <button
            type="button"
            @click="$emit('confirm')"
            :disabled="isDeleting"
            class="w-1/2 inline-flex items-center justify-center gap-2 py-2.5 rounded-2xl bg-red-600 hover:bg-red-700 text-white text-sm font-semibold transition shadow-sm active:scale-95 disabled:opacity-50 cursor-pointer"
          >
            <svg
              v-if="isDeleting"
              class="w-4 h-4 animate-spin text-white"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
            </svg>
            <span>Видалити</span>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
defineProps<{
  isOpen: boolean
  itemTitle?: string
  isDeleting?: boolean
}>()

defineEmits<{
  (e: 'close'): void
  (e: 'confirm'): void
}>()
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
