export interface Project {
  id: string;
  name: string;
  description: string;
  organization_id: string;
}

export interface ProjectSummary {
  total_tasks: number;
  todo_tasks: number;
  in_progress_tasks: number;
  done_tasks: number;
}