<template>
  <div class="bg-white p-6 rounded-xl shadow-lg mt-6">
    <h3 class="text-xl font-semibold text-slate-700 mb-4">Project Overview</h3>
    <div v-if="loading" class="text-center text-slate-500">Loading dashboard data...</div>
    <div v-else-if="error" class="text-center text-red-500">Error loading dashboard: {{ error }}</div>
    <div v-else>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-blue-50 p-4 rounded-lg">
          <p class="text-sm text-blue-700">Total Tasks</p>
          <p class="text-2xl font-bold text-blue-900">{{ dashboardData.total_tasks }}</p>
        </div>
        <div class="bg-yellow-50 p-4 rounded-lg">
          <p class="text-sm text-yellow-700">In Progress</p>
          <p class="text-2xl font-bold text-yellow-900">{{ dashboardData.in_progress_tasks }}</p>
        </div>
        <div class="bg-green-50 p-4 rounded-lg">
          <p class="text-sm text-green-700">Completed</p>
          <p class="text-2xl font-bold text-green-900">{{ dashboardData.done_tasks }}</p>
        </div>
      </div>
      <div class="mt-6">
        <h4 class="text-lg font-semibold text-slate-700 mb-2">Tasks by Status</h4>
        <ul class="list-disc list-inside">
          <li>To Do: {{ dashboardData.todo_tasks }}</li>
          <li>In Progress: {{ dashboardData.in_progress_tasks }}</li>
          <li>Done: {{ dashboardData.done_tasks }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { getProjectSummary } from '../services/api';

const props = defineProps<{ projectId: string }>();

const dashboardData = ref({
  total_tasks: 0,
  todo_tasks: 0,
  in_progress_tasks: 0,
  done_tasks: 0,
});
const loading = ref(false);
const error = ref<string | null>(null);

const fetchProjectSummary = async () => {
  loading.value = true;
  error.value = null;
  try {
    const summary = await getProjectSummary(props.projectId);
    dashboardData.value = summary;
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

watch(() => props.projectId, fetchProjectSummary, { immediate: true });
</script>
