<template>
  <div class="max-w-3xl mx-auto">
    <h2 class="text-2xl font-semibold text-slate-800 mb-4">Tasks for Project: {{ projectName }}</h2>
    <TaskInput @generate="handleGenerateTasks" :loading="loading" />

    <div v-if="loading" class="flex justify-center items-center p-10">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-md mt-6">
      <h3 class="font-bold">Error</h3>
      <p>{{ error }}</p>
    </div>

    <TaskList :tasks="tasks" class="mt-6" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import TaskInput from '../components/TaskInput.vue';
import TaskList from '../components/TaskList.vue';
import { generateTasks, getTasks, getProjectById } from '../services/api';
import type { Task } from '../models/Task';

const props = defineProps<{ projectId: string }>();

const tasks = ref<Task[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const projectName = ref('Loading...');

const route = useRoute();
const currentProjectId = ref(props.projectId);

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

onMounted(fetchProjectAndTasks);

watch(() => props.projectId, (newProjectId) => {
  currentProjectId.value = newProjectId;
  fetchProjectAndTasks();
});
</script>
