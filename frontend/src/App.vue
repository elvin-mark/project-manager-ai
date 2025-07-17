<template>
  <div id="app" class="bg-slate-100 min-h-screen font-sans">
    <Header />
    <main class="container mx-auto p-4 md:p-8">
      <div class="max-w-3xl mx-auto">
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
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Header from './components/Header.vue';
import TaskInput from './components/TaskInput.vue';
import TaskList from './components/TaskList.vue';
import { generateTasks } from './services/api';
import type { Task } from './models/Task';

const tasks = ref<Task[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const handleGenerateTasks = async (objective: string) => {
  loading.value = true;
  error.value = null;
  tasks.value = [];

  try {
    tasks.value = await generateTasks(objective);
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>
