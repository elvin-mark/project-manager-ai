import type { Task } from '../models/Task'
import type { Project, ProjectSummary } from '../models/Project'
import type { Comment } from '../models/Comment'
import type { Subtask } from '../models/Subtask'
import type { Organization } from '../models/Organization'

const API_URL = import.meta.env.VITE_API_URL

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

// User API calls
export async function getAllUsers(): Promise<
  {
    id: string
    username: string
  }[]
> {
  const response = await fetch(`${API_URL}/users`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch users')
  }
  return response.json()
}

// Organization API calls
export async function createOrganization(name: string, description: string): Promise<Organization> {
  const response = await fetch(`${API_URL}/organizations`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ name, description }),
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to create organization')
  }
  return response.json()
}

export async function getOrganizations(): Promise<Organization[]> {
  const response = await fetch(`${API_URL}/organizations`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch organizations')
  }
  return response.json()
}

export async function getOrganizationById(orgId: string): Promise<Organization> {
  const response = await fetch(`${API_URL}/organizations/${orgId}`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch organization')
  }
  return response.json()
}

export async function addUserToOrganization(orgId: string, userId: string): Promise<Organization> {
  const response = await fetch(`${API_URL}/organizations/${orgId}/add_user/${userId}`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to add user to organization')
  }
  return response.json()
}

export async function removeUserFromOrganization(
  orgId: string,
  userId: string,
): Promise<Organization> {
  const response = await fetch(`${API_URL}/organizations/${orgId}/remove_user/${userId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to remove user from organization')
  }
  return response.json()
}

export async function deleteOrganization(orgId: string): Promise<void> {
  const response = await fetch(`${API_URL}/organizations/${orgId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to delete organization')
  }
}

// Project API calls
export async function createProject(
  orgId: string,
  name: string,
  description: string,
): Promise<Project> {
  const response = await fetch(`${API_URL}/projects`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ name, description, organization_id: orgId }),
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to create project')
  }
  return response.json()
}

export async function getProjects(orgId: string): Promise<Project[]> {
  const response = await fetch(`${API_URL}/organizations/${orgId}/projects`, {
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

export async function getProjectSummary(projectId: string): Promise<ProjectSummary> {
  const response = await fetch(`${API_URL}/projects/${projectId}/summary`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch project summary')
  }
  return response.json()
}

export async function getProjectAiSummary(projectId: string): Promise<string> {
  const response = await fetch(`${API_URL}/projects/${projectId}/ai_summary`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch AI project summary')
  }
  return response.text()
}

export async function askProjectQuestion(projectId: string, question: string): Promise<string> {
  const response = await fetch(`${API_URL}/projects/${projectId}/ask`,
    {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ question }),
    });
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to ask project question')
  }
  return response.text()
}

// Task API calls
export async function generateTasks(projectId: string, objective: string, dueDate?: string): Promise<Task[]> {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/tasks/generate?objective=${encodeURIComponent(objective)}${dueDate ? `&due_date=${encodeURIComponent(dueDate)}` : ''}`,
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

export async function getTasks(projectId: string, searchQuery?: string): Promise<Task[]> {
  const url = searchQuery ? `${API_URL}/projects/${projectId}/tasks?search_query=${encodeURIComponent(searchQuery)}` : `${API_URL}/projects/${projectId}/tasks`;
  const response = await fetch(url, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch tasks')
  }
  return response.json()
}

export async function createTask(
  projectId: string,
  title: string,
  description: string,
  due_date?: string,
): Promise<Task> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ title, description, due_date }),
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to create task')
  }
  return response.json()
}

export async function assignTask(projectId: string, taskId: string): Promise<Task> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}/assign`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to assign task')
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

export async function getTask(projectId: string, taskId: string): Promise<Task> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch task')
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

// Comment API calls
export async function getComments(projectId: string, taskId: string): Promise<Comment[]> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}/comments`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch comments')
  }
  return response.json()
}

export async function createComment(projectId: string, taskId: string, content: string): Promise<Comment> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}/comments`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ content }),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to add comment')
  }
  return response.json()
}

// Subtask API calls
export async function generateSubtasks(projectId: string, taskId: string, objective: string): Promise<Subtask[]> {
  const response = await fetch(
    `${API_URL}/projects/${projectId}/tasks/${taskId}/subtasks/generate?objective=${encodeURIComponent(objective)}`,
    {
      method: 'POST',
      headers: getAuthHeaders(),
    },
  )

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to generate subtasks')
  }

  return response.json()
}

export async function getSubtasks(projectId: string, taskId: string): Promise<Subtask[]> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}/subtasks`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch subtasks')
  }
  return response.json()
}

export async function updateSubtask(
  projectId: string,
  taskId: string,
  subtaskId: string,
  subtask: Partial<Subtask>,
): Promise<Subtask> {
  const response = await fetch(`${API_URL}/projects/${projectId}/tasks/${taskId}/subtasks/${subtaskId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(subtask),
  })
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to update subtask')
  }
  return response.json()
}
