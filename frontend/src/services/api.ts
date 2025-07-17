import type { Task } from '../models/Task';

const API_URL = 'http://localhost:8000/api';

export async function generateTasks(objective: string): Promise<Task[]> {
  const response = await fetch(`${API_URL}/tasks/generate?objective=${encodeURIComponent(objective)}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to generate tasks');
  }

  return response.json();
}
