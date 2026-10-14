export interface NavItem {
    id: string
    title: string
    route: string
    icon: string
}

export interface SelectOption {
    id: string
    label: string,
    icon?: string,
    style?: string
}

export interface RegistryFilter {
    key: string
    label: string
    options: SelectOption[]
}

export type ColumnType = 'number' | 'text' | 'select' | 'badge' | 'date'

export interface RegistryColumn {
    key: string
    label: string
    type: ColumnType
    width?: string
    bold?: boolean
    options?: SelectOption[],
    hidden?: boolean
}

export interface RegistryConfig {
    registryId: string
    title: string
    subtitle: string
    endpoint: string
    searchPlaceholder: string
    defaultSort: {
        sortBy: string
        sortOrder: 'asc' | 'desc'
    }
    filters: RegistryFilter[]
    columns: RegistryColumn[]
}