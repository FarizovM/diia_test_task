import type { SelectOption } from '../types/config'

/**
 * Класифікатор статусів задач
 */
export type TaskStatus = 'todo' | 'in_progress' | 'qa' | 'done' | 'flagged'

export interface TaskStatusMetadata {
  key: TaskStatus
  label: string
  style: string
  description?: string
  icon?: string
}

export const TASK_STATUSES: Record<TaskStatus, TaskStatusMetadata> = {
  todo: {
    key: 'todo',
    label: 'До виконання',
    style: 'bg-gray-100 text-gray-800 border border-gray-200/80 font-medium',
    description: 'Задача очікує взяття в роботу',
    icon: `<svg class="w-3.5 h-3.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" stroke-width="2"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 7v5l3 3"/></svg>`,
  },
  in_progress: {
    key: 'in_progress',
    label: 'В роботі',
    style: 'bg-amber-50 text-amber-800 border border-amber-200/70 font-semibold',
    description: 'Задача зараз виконується',
    icon: `<svg class="w-3.5 h-3.5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 12a8 8 0 018-8v8H4z"/></svg>`,
  },
  qa: {
    key: 'qa',
    label: 'На перевірці',
    style: 'bg-purple-50 text-purple-800 border border-purple-200/70 font-semibold',
    description: 'Задача знаходиться на тестуванні або рецензії',
    icon: `<svg class="w-3.5 h-3.5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`,
  },
  done: {
    key: 'done',
    label: 'Виконано',
    style: 'bg-diia-accent/30 text-black border border-diia-accent/50 font-bold',
    description: 'Задачу успішно завершено',
    icon: `<svg class="w-3.5 h-3.5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>`,
  },
  flagged: {
    key: 'flagged',
    label: 'Заблоковано',
    style: 'bg-red-50 text-red-800 border border-red-200/70 font-semibold',
    description: 'Виконання заблоковано через зовнішні перешкоди',
    icon: `<svg class="w-3.5 h-3.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"/></svg>`,
  },
}

export const TASK_STATUS_OPTIONS: SelectOption<TaskStatus>[] = [
  {
    key: TASK_STATUSES.todo.key,
    label: TASK_STATUSES.todo.label,
    style: TASK_STATUSES.todo.style,
    icon: TASK_STATUSES.todo.icon,
  },
  {
    key: TASK_STATUSES.in_progress.key,
    label: TASK_STATUSES.in_progress.label,
    style: TASK_STATUSES.in_progress.style,
    icon: TASK_STATUSES.in_progress.icon,
  },
  {
    key: TASK_STATUSES.qa.key,
    label: TASK_STATUSES.qa.label,
    style: TASK_STATUSES.qa.style,
    icon: TASK_STATUSES.qa.icon,
  },
  {
    key: TASK_STATUSES.done.key,
    label: TASK_STATUSES.done.label,
    style: TASK_STATUSES.done.style,
    icon: TASK_STATUSES.done.icon,
  },
  {
    key: TASK_STATUSES.flagged.key,
    label: TASK_STATUSES.flagged.label,
    style: TASK_STATUSES.flagged.style,
    icon: TASK_STATUSES.flagged.icon,
  },
]

/**
 * Класифікатор пріоритетів задач
 */
export type TaskPriority = 'lowest' | 'low' | 'medium' | 'high' | 'highest'

export interface TaskPriorityMetadata {
  key: TaskPriority
  label: string
  icon: string
  weight: number
}

export const TASK_PRIORITIES: Record<TaskPriority, TaskPriorityMetadata> = {
  highest: {
    key: 'highest',
    label: 'Найвищий',
    weight: 5,
    icon: `<svg class="w-3.5 h-3.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`,
  },
  high: {
    key: 'high',
    label: 'Високий',
    weight: 4,
    icon: `<svg class="w-3.5 h-3.5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/></svg>`,
  },
  medium: {
    key: 'medium',
    label: 'Середній',
    weight: 3,
    icon: `<svg class="w-3.5 h-3.5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/></svg>`,
  },
  low: {
    key: 'low',
    label: 'Низький',
    weight: 2,
    icon: `<svg class="w-3.5 h-3.5 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>`,
  },
  lowest: {
    key: 'lowest',
    label: 'Найнижчий',
    weight: 1,
    icon: `<svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7-7-7m0 0l-7-7"/></svg>`,
  },
}

export const TASK_PRIORITY_OPTIONS: SelectOption<TaskPriority>[] = [
  {
    key: TASK_PRIORITIES.highest.key,
    label: TASK_PRIORITIES.highest.label,
    icon: TASK_PRIORITIES.highest.icon,
    style: 'bg-red-50 text-red-900 border border-red-200/60 font-semibold',
  },
  {
    key: TASK_PRIORITIES.high.key,
    label: TASK_PRIORITIES.high.label,
    icon: TASK_PRIORITIES.high.icon,
    style: 'bg-orange-50 text-orange-900 border border-orange-200/60 font-medium',
  },
  {
    key: TASK_PRIORITIES.medium.key,
    label: TASK_PRIORITIES.medium.label,
    icon: TASK_PRIORITIES.medium.icon,
    style: 'bg-blue-50 text-blue-900 border border-blue-200/60 font-medium',
  },
  {
    key: TASK_PRIORITIES.low.key,
    label: TASK_PRIORITIES.low.label,
    icon: TASK_PRIORITIES.low.icon,
    style: 'bg-teal-50 text-teal-900 border border-teal-200/60 font-medium',
  },
  {
    key: TASK_PRIORITIES.lowest.key,
    label: TASK_PRIORITIES.lowest.label,
    icon: TASK_PRIORITIES.lowest.icon,
    style: 'bg-gray-50 text-gray-700 border border-gray-200/60 font-medium',
  },
]
