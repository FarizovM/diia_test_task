import type { RegistryConfig } from '../types/config'
import {
  TASK_STATUS_OPTIONS,
  TASK_PRIORITY_OPTIONS,
  type TaskStatus,
  type TaskPriority,
} from '../constants/classifiers'

/**
 * Типізація моделі задачі (відповідає схемі бекенду TaskResponse)
 */
export interface TaskRow {
  task_id: string
  title: string
  description?: string | null
  status: TaskStatus
  priority: TaskPriority
  deadline?: string | null
  created_at: string
  updated_at: string
  created_by?: string
}

export type TaskColumnKey =
  | 'title'
  | 'description'
  | 'priority'
  | 'status'
  | 'deadline'
  | 'created_at'

export const tasksRegistry: RegistryConfig<TaskColumnKey> = {
  registryId: 'tasks',
  registry_id: 'tasks',
  title: 'Реєстр задач',
  subtitle: 'Єдиний список завдань та моніторинг виконання у системі',
  endpoint: '/tasks',
  searchPlaceholder: 'Пошук за назвою та описом...',
  defaultSort: {
    sortBy: 'created_at',
    sortOrder: 'desc',
  },
  columns: [
    {
      key: 'title',
      label: 'Назва задачі',
      type: 'text',
      width: '240px',
      bold: true,
      sortable: true,
      required: true,
      placeholder: 'Введіть назву задачі...',
    },
    {
      key: 'description',
      label: 'Опис',
      type: 'textarea',
      width: '320px',
      sortable: false,
      rows: 3,
      placeholder: 'Детальний опис задачі...',
    },
    {
      key: 'priority',
      label: 'Пріоритет',
      type: 'select',
      width: '160px',
      options: TASK_PRIORITY_OPTIONS,
      sortable: true,
      required: true,
      defaultValue: 'medium'
    },
    {
      key: 'status',
      label: 'Статус',
      type: 'select',
      width: '170px',
      options: TASK_STATUS_OPTIONS,
      required: true,
      sortable: true,
    },
    {
      key: 'deadline',
      label: 'Дедлайн',
      type: 'date',
      width: '180px',
      sortable: true,
    },
  ],
  filters: [
    {
      key: 'status',
      label: 'Статус',
      options: TASK_STATUS_OPTIONS,
    },
    {
      key: 'priority',
      label: 'Пріоритет',
      options: TASK_PRIORITY_OPTIONS,
    },
  ],
}

export default tasksRegistry
