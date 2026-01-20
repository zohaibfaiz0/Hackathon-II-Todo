import { Task, TaskInput } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const getSessionData = (): { userId: string; token: string } | null => {
  if (typeof window === 'undefined') return null
  
  const sessionStr = localStorage.getItem('session')
  if (!sessionStr) return null
  
  try {
    const session = JSON.parse(sessionStr)
    const userId = session.user?.id
    const token = session.token
    
    if (!userId || !token) return null
    
    return { userId, token }
  } catch (e) {
    console.error('Failed to parse session data', e)
    return null
  }
}

const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const sessionData = getSessionData()

  if (!sessionData) {
    throw new Error('User not authenticated')
  }

  const { userId, token } = sessionData

  // Build URL: /api/{userId}/tasks...
  // endpoint comes in as "/tasks" or "/tasks/123" etc.
  let path = endpoint
  if (endpoint.startsWith('/tasks')) {
    path = `/${userId}/tasks` + endpoint.substring(6)
  }

  // Final URL: http://localhost:8000/api/{userId}/tasks
  const url = `${API_BASE_URL}/api${path}`
  
  console.log('API URL:', url) // Debug log

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

export const getTasks = async (): Promise<Task[]> => {
  return apiRequest<Task[]>('/tasks')
}

export const getTask = async (id: number): Promise<Task> => {
  return apiRequest<Task>(`/tasks/${id}`)
}

export const createTask = async (taskData: TaskInput): Promise<Task> => {
  return apiRequest<Task>('/tasks', {
    method: 'POST',
    body: JSON.stringify(taskData),
  })
}

export const updateTask = async (id: number, taskData: Partial<TaskInput>): Promise<Task> => {
  return apiRequest<Task>(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  })
}

export const deleteTask = async (id: number): Promise<void> => {
  await apiRequest<void>(`/tasks/${id}`, {
    method: 'DELETE',
  })
}

export const toggleTaskComplete = async (id: number): Promise<Task> => {
  return apiRequest<Task>(`/tasks/${id}/complete`, {
    method: 'PATCH',
  })
}