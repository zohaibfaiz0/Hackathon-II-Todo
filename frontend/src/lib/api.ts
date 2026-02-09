import { Task, TaskInput } from '@/types'

// Support Dapr sidecar invocation if enabled
const DIRECT_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const DAPR_PORT = process.env.NEXT_PUBLIC_DAPR_HTTP_PORT || "3500";
const ENABLE_DAPR = process.env.NEXT_PUBLIC_ENABLE_DAPR === "true";

// If Dapr is enabled, route requests through sidecar
// Format: http://localhost:<dapr-port>/v1.0/invoke/<app-id>/method
const API_BASE_URL = ENABLE_DAPR 
  ? `http://localhost:${DAPR_PORT}/v1.0/invoke/backend/method`
  : DIRECT_URL;

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

  // Final URL
  const url = `${API_BASE_URL}/api${path}`
  
  console.log('API URL:', url) // Debug log

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      // Add Dapr App ID header if using Dapr (optional but good practice)
      ...(ENABLE_DAPR ? { 'dapr-app-id': 'backend' } : {}),
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