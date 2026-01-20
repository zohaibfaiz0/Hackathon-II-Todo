export interface Task {
  id: number
  user_id: string
  title: string
  description: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskInput {
  title: string
  description?: string
  completed?: boolean
}

export interface User {
  id: string
  email: string
}

export interface Session {
  user: User
  token: string
}