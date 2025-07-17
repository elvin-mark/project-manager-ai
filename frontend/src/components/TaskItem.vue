<template>
  <div class="bg-white p-4 rounded-lg shadow-md">
    <h3 class="text-lg font-bold">{{ task.title }}</h3>
    <p class="text-gray-700">{{ task.description }}</p>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '../models/Task';

defineProps<{ task: Task }>();
</script>
