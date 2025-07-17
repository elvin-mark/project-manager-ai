<template>
  <div class="bg-white p-5 rounded-xl shadow-lg border border-slate-200 hover:shadow-xl transition-shadow duration-300">
    <div class="flex justify-between items-start">
      <h3 class="text-lg font-semibold text-slate-800 mb-2">{{ task.title }}</h3>
      <span 
        class="text-xs font-semibold uppercase px-3 py-1 rounded-full"
        :class="statusClass"
      >
        {{ task.status }}
      </span>
    </div>
    <p class="text-slate-600">{{ task.description }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Task } from '../models/Task';

const props = defineProps<{ task: Task }>();

const statusClass = computed(() => {
  switch (props.task.status.toLowerCase()) {
    case 'todo':
      return 'bg-blue-100 text-blue-800';
    case 'in_progress':
      return 'bg-yellow-100 text-yellow-800';
    case 'done':
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-slate-100 text-slate-800';
  }
});
</script>
