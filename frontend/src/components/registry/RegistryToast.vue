<template>
  <Transition name="toast">
    <div
      v-if="message"
      class="fixed bottom-6 right-6 z-50 flex items-center gap-3 px-5 py-3.5 rounded-2xl shadow-xl text-sm font-semibold transition-all"
      :class="[
        type === 'error'
          ? 'bg-red-600 text-white shadow-red-600/20'
          : 'bg-diia-dark text-white border border-white/10 shadow-black/20'
      ]"
    >
      <div
        v-if="type === 'success'"
        class="w-6 h-6 rounded-full bg-diia-accent text-black flex items-center justify-center shrink-0"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
        </svg>
      </div>

      <div
        v-else
        class="w-6 h-6 rounded-full bg-white/20 text-white flex items-center justify-center shrink-0"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>

      <span>{{ message }}</span>

      <button
        type="button"
        @click="$emit('close')"
        class="ml-2 text-white/60 hover:text-white transition cursor-pointer"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
defineProps<{
  message: string
  type: 'success' | 'error'
}>()

defineEmits<{
  (e: 'close'): void
}>()
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.95);
}
</style>
