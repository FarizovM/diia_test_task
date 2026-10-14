export type TaskStatus = 'todo' | 'in_progress' | 'qa' | 'done'
export type TaskPriority = 'lowest' | 'low' | 'medium' | 'high' | 'highest'

export interface User {
    user_id: string
    email: string
    hashed_password: string
    first_name: string
    last_name: string
    middle_name: string | null
    created_at: string
    updated_at: string
    updated_by: string | null
}

export interface AuthTokenResponse {
    access_token: string
    token_type: string
}

export interface Task {
    task_id: string
    title: string
    description: string | null
    status: TaskStatus
    priority: TaskPriority
    deadline: string | null
    created_at: string
    updated_at: string | null
    created_by: string
    updated_by: string | null
}

export interface TaskCreatePayload {
    title: string
    description?: string | null
    status: TaskStatus
    priority: TaskPriority
    deadline?: string | null
}

export interface TaskUpdatePayload extends Partial<TaskCreatePayload> { }