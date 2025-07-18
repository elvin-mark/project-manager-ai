import type { Subtask } from './Subtask';

export interface Task {
  id: string;
  title: string;
  description: string;
  status: string;
  project_id: string;
  assigned_user_id?: string;
  assigned_username?: string;
  due_date?: string;
  subtasks?: Subtask[];
}