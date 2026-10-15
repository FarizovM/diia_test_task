import type { SelectOption } from '../types/config'

/**
 * Класифікатор статусів задач
 */
export type TaskStatus = 'todo' | 'in_progress' | 'qa' | 'done' | 'flagged'

export const TASK_STATUS_OPTIONS: SelectOption<TaskStatus>[] = [
  {
    key: 'todo',
    label: 'До виконання',
    style: 'bg-gray-100 text-gray-800 border border-gray-200/80 font-medium',
    icon: `<svg class="w-3.5 h-3.5 text-gray-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" stroke-width="2"/></svg>`,
  },
  {
    key: 'in_progress',
    label: 'В роботі',
    style: 'bg-blue-50 text-blue-800 border border-blue-200/70 font-semibold',
    icon: `<svg class="w-3.5 h-3.5 text-blue-600 shrink-0" viewBox="0 0 16 16" fill="none" stroke="currentColor"><circle cx="8" cy="8" r="6" stroke-width="2"/><path d="M8 2a6 6 0 0 1 0 12V2z" fill="currentColor"/></svg>`,
  },
  {
    key: 'qa',
    label: 'На перевірці',
    style: 'bg-purple-50 text-purple-800 border border-purple-200/70 font-semibold',
    icon: `<svg class="w-3.5 h-3.5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`,
  },
  {
    key: 'done',
    label: 'Виконано',
    style: 'bg-diia-accent/30 text-black border border-diia-accent/50 font-bold',
    icon: `<svg class="w-3.5 h-3.5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>`,
  },
  {
    key: 'flagged',
    label: 'Заблоковано',
    style: 'bg-red-50 text-red-800 border border-red-200/70 font-semibold',
    icon: `<svg class="w-3.5 h-3.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"/></svg>`,
  },
]

/**
 * Класифікатор пріоритетів задач (у стилі Jira)
 */
export type TaskPriority = 'lowest' | 'low' | 'medium' | 'high' | 'highest'

export const TASK_PRIORITY_OPTIONS: SelectOption<TaskPriority>[] = [
  {
    key: 'highest',
    label: 'Найвищий',
    style: 'bg-red-50 text-red-900 border border-red-200/60 font-semibold',
    icon: `<svg class="w-3.5 h-3.5 text-red-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 16 16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.5 7L8 3L12.5 7M3.5 12L8 8L12.5 12"/></svg>`,
  },
  {
    key: 'high',
    label: 'Високий',
    style: 'bg-red-50 text-red-800 border border-red-200/60 font-medium',
    icon: `<svg class="w-3.5 h-3.5 text-red-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 16 16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.5 10L8 5.5L12.5 10"/></svg>`,
  },
  {
    key: 'medium',
    label: 'Середній',
    style: 'bg-amber-50 text-amber-900 border border-amber-200/60 font-medium',
    icon: `<svg class="w-3.5 h-3.5 text-amber-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 16 16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.5 6h9M3.5 10h9"/></svg>`,
  },
  {
    key: 'low',
    label: 'Низький',
    style: 'bg-blue-50 text-blue-900 border border-blue-200/60 font-medium',
    icon: `<svg class="w-3.5 h-3.5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 16 16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.5 6L8 10.5L12.5 6"/></svg>`,
  },
  {
    key: 'lowest',
    label: 'Найнижчий',
    style: 'bg-blue-50 text-blue-900 border border-blue-200/60 font-medium',
    icon: `<svg class="w-3.5 h-3.5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 16 16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.5 4L8 8L12.5 4M3.5 9L8 13L12.5 9"/></svg>`,
  },
]
