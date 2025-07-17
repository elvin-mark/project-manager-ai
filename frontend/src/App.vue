<template>
  <div id="app" class="bg-gray-100 min-h-screen">
    <Header />
    <main class="container mx-auto py-8">
      <TaskInput @generate="handleGenerateTasks" />
      <div v-if="loading" class="text-center p-4">Loading...</div>
      <div v-if="error" class="text-red-500 p-4">{{ error }}</div>
      <TaskList :tasks="tasks" />
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

<style>
/* You can add global styles here if needed */
</style>