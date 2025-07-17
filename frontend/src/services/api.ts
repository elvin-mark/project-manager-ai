import type { Task } from '../models/Task'
import type { Project } from '../models/Project'

const API_URL = 'http://localhost:8000/api'

// Project API calls
export async function createProject(name: string, description: string): Promise<Project> {
  const response = await fetch(`${API_URL}/projects`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, description }),
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to create project')
  }
  return response.json()
}

export async function getProjects(): Promise<Project[]> {
  const response = await fetch(`${API_URL}/projects`)
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch projects')
  }
  return response.json()
}

export async function getProjectById(projectId: string): Promise<Project> {
  const response = await fetch(`${API_URL}/projects/${projectId}`)
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch project')
  }
  return response.json()
}

export async function deleteProject(projectId: string): Promise<void> {
  const response = await fetch(`${API_URL}/projects/${projectId}`, {
    method: 'DELETE',
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
      headers: {
        'Content-Type': 'application/json',
      },
    },
  )

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to generate tasks')
  }

  return response.json()
}

export async function getTasks(projectId: string): Promise<Task[]> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks`)
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
    headers: {
      'Content-Type': 'application/json',
    },
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
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to delete task')
  }
}
