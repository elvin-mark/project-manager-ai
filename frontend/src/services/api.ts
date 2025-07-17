import type { Task } from '../models/Task'
import type { Project } from '../models/Project'

const API_URL = 'http://localhost:8000/api'

function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem('access_token')
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

export async function login(
  username: string,
  password: string,
): Promise<{ access_token: string; token_type: string }> {
  const details = new URLSearchParams()
  details.append('username', username)
  details.append('password', password)

  const response = await fetch(`${API_URL}/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: details.toString(),
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to login')
  }
  const data = await response.json()
  localStorage.setItem('access_token', data.access_token)
  return data
}

export async function register(username: string, password: string): Promise<any> {
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ username, password }),
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to register')
  }
  return response.json()
}

// Project API calls
export async function createProject(name: string, description: string): Promise<Project> {
  const response = await fetch(`${API_URL}/projects`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ name, description }),
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to create project')
  }
  return response.json()
}

export async function getProjects(): Promise<Project[]> {
  const response = await fetch(`${API_URL}/projects`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch projects')
  }
  return response.json()
}

export async function getProjectById(projectId: string): Promise<Project> {
  const response = await fetch(`${API_URL}/projects/${projectId}`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch project')
  }
  return response.json()
}

export async function deleteProject(projectId: string): Promise<void> {
  const response = await fetch(`${API_URL}/projects/${projectId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to delete project')
  }
}

// Task API calls
export async function generateTasks(projectId: string, objective: string): Promise<Task[]> {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/tasks/generate?objective=${encodeURIComponent(objective)}`,
    {
      method: 'POST',
      headers: getAuthHeaders(),
    },
  )

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to generate tasks')
  }

  return response.json()
}

export async function getTasks(projectId: string): Promise<Task[]> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch tasks')
  }
  return response.json()
}

export async function updateTask(
  projectId: string,
  taskId: string,
  task: Partial<Task>,
): Promise<Task> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(task),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to update task')
  }
  return response.json()
}

export async function deleteTask(projectId: string, taskId: string): Promise<void> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to delete task')
  }
}
