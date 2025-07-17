<template>
  <div class="p-4">
    <div v-if="tasks.length === 0" class="text-gray-500">No tasks yet.</div>
    <div v-else class="space-y-4">
      <TaskItem v-for="task in tasks" :key="task.id" :task="task" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '../models/Task';
import TaskItem from './TaskItem.vue';

defineProps<{ tasks: Task[] }>();
</script>
