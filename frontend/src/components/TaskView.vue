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
        @add-task="handleAddTask"
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
        @add-task="handleAddTask"
      />
    </template>

    <ProjectDashboard :project-id="currentProjectId" />

    <!-- Add Task Modal -->
    <div v-if="showAddTaskModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center">
      <div class="bg-white p-8 rounded-lg shadow-xl max-w-md w-full">
        <h3 class="text-xl font-semibold mb-4">Add New Task</h3>
        <form @submit.prevent="submitNewTask">
          <div class="mb-4">
            <label for="taskTitle" class="block text-sm font-medium text-gray-700">Title</label>
            <input
              type="text"
              id="taskTitle"
              v-model="newTask.title"
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
              required
            />
          </div>
          <div class="mb-4">
            <label for="taskDescription" class="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              id="taskDescription"
              v-model="newTask.description"
              rows="3"
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            ></textarea>
          </div>
          <div class="mb-4">
            <label for="taskDueDate" class="block text-sm font-medium text-gray-700">Due Date</label>
            <input
              type="date"
              id="taskDueDate"
              v-model="newTask.due_date"
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="showAddTaskModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
            >
              Create Task
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TaskInput from '../components/TaskInput.vue';
import KanbanBoard from '../components/KanbanBoard.vue';
import TaskList from '../components/TaskList.vue';
import { generateTasks, getTasks, getProjectById, updateTask, deleteTask, assignTask, getComments, createComment, generateSubtasks, getSubtasks, updateSubtask, createTask } from '../services/api';
import type { Task } from '../models/Task';
import type { Comment } from '../models/Comment';
import type { Subtask } from '../models/Subtask';
import ProjectDashboard from '../components/ProjectDashboard.vue';

const props = defineProps<{ orgId: string, projectId: string }>();

const tasks = ref<Task[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const projectName = ref('Loading...');
const isMobileView = ref(false);

const selectedTask = ref<Task | null>(null);
const comments = ref<Comment[]>([]);
const newCommentContent = ref('');
const searchQuery = ref('');
const subtaskObjective = ref('');
const showAddTaskModal = ref(false);
const newTask = ref<Partial<Task>>({
  title: '',
  description: '',
  due_date: undefined,
});

const route = useRoute();
const router = useRouter();
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
  router.push({ name: 'task-details', params: { orgId: currentOrgId.value, projectId: currentProjectId.value, taskId: task.id } });
};

const handleAddTask = () => {
  showAddTaskModal.value = true;
};

const submitNewTask = async () => {
  try {
    const createdTask = await createTask(
      currentProjectId.value,
      newTask.value.title || '',
      newTask.value.description || '',
      newTask.value.due_date ? new Date(newTask.value.due_date).toISOString() : undefined
    );
    tasks.value.push(createdTask);
    showAddTaskModal.value = false;
    newTask.value = { title: '', description: '', due_date: undefined };
  } catch (err: any) {
    alert(`Failed to create task: ${err.message}`);
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

const handleGenerateSubtasks = async () => {
  if (!selectedTask.value || !subtaskObjective.value.trim()) return;
  try {
    const newSubtasks = await generateSubtasks(currentProjectId.value, selectedTask.value.id, subtaskObjective.value);
    if (selectedTask.value.subtasks) {
      selectedTask.value.subtasks.push(...newSubtasks);
    } else {
      selectedTask.value.subtasks = newSubtasks;
    }
    subtaskObjective.value = '';
  } catch (err: any) {
    console.error("Error generating subtasks:", err);
    alert(`Failed to generate subtasks: ${err.message}`);
  }
};

const handleUpdateSubtask = async (subtask: Subtask) => {
  if (!selectedTask.value) return;
  try {
    const updated = await updateSubtask(currentProjectId.value, selectedTask.value.id, subtask.id, subtask);
    if (selectedTask.value.subtasks) {
      const index = selectedTask.value.subtasks.findIndex(s => s.id === updated.id);
      if (index !== -1) {
        selectedTask.value.subtasks[index] = updated;
      }
    }
  } catch (err: any) {
    console.error("Error updating subtask:", err);
    alert(`Failed to update subtask: ${err.message}`);
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
