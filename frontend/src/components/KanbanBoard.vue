<template>
  <div class="flex flex-col space-y-4">
    <button
      @click="addNewTask"
      class="self-start px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
    >
      Add New Task
    </button>
    <div class="flex space-x-4 overflow-x-auto">
    <div
      v-for="column in columns"
      :key="column.status"
      class="flex-shrink-0 w-80 bg-gray-100 rounded-lg shadow-md p-4"
    >
      <h2 class="text-lg font-semibold mb-4">{{ column.title }}</h2>
      <div
        class="min-h-[98%] p-4 rounded-md border border-dashed border-gray-300"
        @dragover.prevent
        @drop="onDrop(column.status)"
        :data-status="column.status"
      >
        <TaskItem
          v-for="task in filteredTasks(column.status)"
          :key="task.id"
          :task="task"
          draggable="true"
          @dragstart="onDragStart(task)"
          @update-task="(updatedTask) => $emit('update-task', updatedTask)"
          @delete-task="(taskId) => $emit('delete-task', taskId)"
          @assign-task="(taskId) => $emit('assign-task', taskId)"
          @view-task="(task) => $emit('view-task', task)"
          class="mb-3 cursor-grab"
        />
        <p v-if="filteredTasks(column.status).length === 0" class="text-gray-500 text-sm">No tasks in this column.</p>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Task } from '../models/Task';
import TaskItem from './TaskItem.vue';

const props = defineProps<{ tasks: Task[] }>();
const emit = defineEmits(['update-task', 'delete-task', 'assign-task', 'view-task', 'add-task']);

const addNewTask = () => {
  emit('add-task');
};

const columns = ref([
  { status: 'todo', title: 'To Do' },
  { status: 'in_progress', title: 'In Progress' },
  { status: 'done', title: 'Done' },
]);

const draggingTask = ref<Task | null>(null);

const filteredTasks = (status: string) => {
  return props.tasks.filter(task => task.status === status);
};

const onDragStart = (task: Task) => {
  draggingTask.value = task;
};

const onDrop = (newStatus: string) => {
  if (draggingTask.value) {
    const updatedTask = { ...draggingTask.value, status: newStatus };
    emit('update-task', updatedTask);
    draggingTask.value = null;
  }
};
</script>

<style scoped>
/* Add any specific styles for your Kanban board here */
</style>
