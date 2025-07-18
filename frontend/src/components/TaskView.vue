<template>
  <div class="max-w-5xl mx-auto">
    <h2 class="text-2xl font-semibold text-slate-800 mb-4">Tasks for Project: {{ projectName }}</h2>
    <TaskInput @generate="handleGenerateTasks" :loading="loading" />

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
      />
    </template>
    <template v-else>
      <KanbanBoard 
        :tasks="tasks" 
        class="mt-6" 
        @update-task="handleUpdateTask" 
        @delete-task="handleDeleteTask" 
        @assign-task="handleAssignTask"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import TaskInput from '../components/TaskInput.vue';
import KanbanBoard from '../components/KanbanBoard.vue';
import TaskList from '../components/TaskList.vue';
import { generateTasks, getTasks, getProjectById, updateTask, deleteTask, assignTask } from '../services/api';
import type { Task } from '../models/Task';

const props = defineProps<{ orgId: string, projectId: string }>();

const tasks = ref<Task[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const projectName = ref('Loading...');
const isMobileView = ref(false);

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
    tasks.value = await getTasks(currentProjectId.value);
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const handleGenerateTasks = async (objective: string) => {
  loading.value = true;
  error.value = null;
  tasks.value = [];

  try {
    tasks.value = await generateTasks(currentProjectId.value, objective);
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
</script>
