export interface Comment {
  id: string;
  content: string;
  created_at: string;
  task_id: string;
  user_id: string;
  username?: string;
}