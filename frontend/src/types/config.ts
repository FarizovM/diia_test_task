export interface NavItem {
    id: string
    title: string
    route: string
    icon: string
}

export interface SelectOption<T = string> {
    key: T
    label: string
    icon?: string
    style?: string
}

export interface RegistryFilter<TKey extends string = string, TOption = any> {
    key: TKey
    label: string
    options: SelectOption<TOption>[]
}

export type ColumnType = 'number' | 'text' | 'textarea' | 'select' | 'badge' | 'date'

export interface RegistryColumn<TKey extends string = string, TOption = any> {
    key: TKey
    label: string
    type: ColumnType
    width?: string
    bold?: boolean
    options?: SelectOption<TOption>[]
    hidden?: boolean
    sortable?: boolean
    required?: boolean
    placeholder?: string
    rows?: number
    defaultValue?: any
    readonly?: boolean
}

export interface RegistryConfig<TColumnKey extends string = string> {
    registryId?: string
    registry_id?: string
    title: string
    subtitle?: string
    endpoint: string
    searchPlaceholder?: string
    defaultSort?: {
        sortBy: TColumnKey
        sortOrder: 'asc' | 'desc'
    }
    filters?: RegistryFilter<string, any>[]
    columns: RegistryColumn<TColumnKey, any>[]
}

export interface RegistryResponse<TRow = any> {
    total: number
    filtered: number
    rows: TRow[]
}