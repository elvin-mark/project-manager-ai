<template>
  <div class="max-w-5xl mx-auto">
    <h2 class="text-2xl font-semibold text-slate-800 mb-4">Tasks for Project: {{ projectName }}</h2>
    <TaskInput @generate="handleGenerateTasks" :loading="loading" />

    <div class="mt-6 mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search tasks by title or description..."
        class="w-full p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
      />
    </div>

    <div v-if="loading" class="flex justify-center items-center p-10">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-md mt-6">
      <h3 class="font-bold">Error</h3>
      <p>{{ error }}</p>
    </div>

    <template v-if="isMobileView">
      <TaskList 
        :tasks="tasks" 
        class="mt-6" 
        @update-task="handleUpdateTask" 
        @delete-task="handleDeleteTask" 
        @assign-task="handleAssignTask"
        @view-task="handleViewTask"
      />
    </template>
    <template v-else>
      <KanbanBoard 
        :tasks="tasks" 
        class="mt-6" 
        @update-task="handleUpdateTask" 
        @delete-task="handleDeleteTask" 
        @assign-task="handleAssignTask"
        @view-task="handleViewTask"
      />
    </template>

    <!-- Comment Modal -->
    <div v-if="showCommentModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
      <div class="bg-white p-8 rounded-lg shadow-xl max-w-md w-full mx-4">
        <h3 class="text-xl font-semibold text-slate-800 mb-4">Comments for {{ selectedTask?.title }}</h3>
        <div class="max-h-80 overflow-y-auto mb-4 border p-3 rounded-md bg-gray-50">
          <div v-if="comments.length === 0" class="text-slate-500 text-center">No comments yet.</div>
          <div v-for="comment in comments" :key="comment.id" class="mb-3 pb-3 border-b last:border-b-0 last:pb-0">
            <p class="text-slate-700 text-sm">{{ comment.content }}</p>
            <p class="text-xs text-slate-500 text-right">- {{ comment.username }} on {{ formatDate(comment.created_at) }}</p>
          </div>
        </div>
        <textarea
          v-model="newCommentContent"
          placeholder="Add a new comment..."
          rows="3"
          class="w-full p-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
        ></textarea>
        <div class="flex justify-end space-x-2">
          <button @click="showCommentModal = false" class="px-4 py-2 border border-slate-300 rounded-md text-slate-700 hover:bg-slate-100">Close</button>
          <button @click="handleAddComment" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Add Comment</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import TaskInput from '../components/TaskInput.vue';
import KanbanBoard from '../components/KanbanBoard.vue';
import TaskList from '../components/TaskList.vue';
import { generateTasks, getTasks, getProjectById, updateTask, deleteTask, assignTask, getComments, createComment } from '../services/api';
import type { Task } from '../models/Task';
import type { Comment } from '../models/Comment';

const props = defineProps<{ orgId: string, projectId: string }>();

const tasks = ref<Task[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const projectName = ref('Loading...');
const isMobileView = ref(false);

const selectedTask = ref<Task | null>(null);
const comments = ref<Comment[]>([]);
const newCommentContent = ref('');
const showCommentModal = ref(false);
const searchQuery = ref('');

const route = useRoute();
const currentOrgId = ref(props.orgId);
const currentProjectId = ref(props.projectId);

const checkMobile = () => {
  isMobileView.value = window.innerWidth < 768; // Tailwind's 'md' breakpoint
};

const fetchProjectAndTasks = async () => {
  loading.value = true;
  error.value = null;
  tasks.value = [];

  try {
    const project = await getProjectById(currentProjectId.value);
    projectName.value = project.name;
    tasks.value = await getTasks(currentProjectId.value, searchQuery.value);
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const handleGenerateTasks = async (objective: string, dueDate?: string) => {
  loading.value = true;
  error.value = null;
  tasks.value = [];

  try {
    tasks.value = await generateTasks(currentProjectId.value, objective, dueDate);
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const handleUpdateTask = async (updatedTask: Partial<Task> & { id: string }) => {
  try {
    const responseTask = await updateTask(currentProjectId.value, updatedTask.id, updatedTask);
    const index = tasks.value.findIndex(t => t.id === responseTask.id);
    if (index !== -1) {
      tasks.value[index] = responseTask;
    }
  } catch (err: any) {
    alert(`Failed to update task: ${err.message}`);
  }
};

const handleDeleteTask = async (taskId: string) => {
  try {
    await deleteTask(currentProjectId.value, taskId);
    tasks.value = tasks.value.filter(t => t.id !== taskId);
  } catch (err: any) {
    alert(`Failed to delete task: ${err.message}`);
  }
};

const handleAssignTask = async (taskId: string) => {
  try {
    const responseTask = await assignTask(currentProjectId.value, taskId); // No userId needed here
    const index = tasks.value.findIndex(t => t.id === responseTask.id);
    if (index !== -1) {
      tasks.value[index] = responseTask;
    }
  } catch (err: any) {
    console.error("Error assigning task:", err);
    alert(`Failed to assign task: ${err.message}`);
  }
};

const handleViewTask = async (task: Task) => {
  selectedTask.value = task;
  showCommentModal.value = true;
  try {
    comments.value = (await getComments(currentProjectId.value, task.id)) as Comment[];
  } catch (err: any) {
    console.error("Error fetching comments:", err);
    alert(`Failed to fetch comments: ${err.message}`);
  }
};

const handleAddComment = async () => {
  if (!selectedTask.value || !newCommentContent.value.trim()) return;
  try {
    const newComment = await createComment(currentProjectId.value, selectedTask.value.id, newCommentContent.value);
    comments.value.push(newComment);
    newCommentContent.value = '';
  } catch (err: any) {
    console.error("Error adding comment:", err);
    alert(`Failed to add comment: ${err.message}`);
  }
};

const formatDate = (dateString: string) => {
  const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

onMounted(() => {
  fetchProjectAndTasks();
  checkMobile();
  window.addEventListener('resize', checkMobile);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile);
});

watch(() => props.projectId, (newProjectId) => {
  currentProjectId.value = newProjectId;
  fetchProjectAndTasks();
});

watch(() => props.orgId, (newOrgId) => {
  currentOrgId.value = newOrgId;
  // Re-fetch projects and tasks when organization changes
  fetchProjectAndTasks();
});

watch(searchQuery, () => {
  fetchProjectAndTasks();
});
</script>
