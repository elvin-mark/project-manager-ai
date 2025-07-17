<template>
  <div>
    <div v-if="tasks.length > 0" class="space-y-4">
      <TaskItem 
        v-for="task in tasks" 
        :key="task.id" 
        :task="task" 
        @update-task="(updatedTask) => $emit('update-task', updatedTask)"
        @delete-task="(taskId) => $emit('delete-task', taskId)"
        @assign-task="(taskId) => $emit('assign-task', taskId)"
      />
    </div>
    <div v-else class="text-center py-10 px-4 bg-white rounded-xl shadow-md">
      <h3 class="text-lg font-medium text-slate-600">No tasks yet.</h3>
      <p class="text-slate-500">Enter an objective above to get started.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '../models/Task';
import TaskItem from './TaskItem.vue';

defineProps<{ tasks: Task[] }>();
const emit = defineEmits(['update-task', 'delete-task', 'assign-task']);
</script>
