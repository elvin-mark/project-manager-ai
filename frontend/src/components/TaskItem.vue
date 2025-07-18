<template>
  <div class="bg-white p-5 rounded-xl shadow-lg border border-slate-200 hover:shadow-xl transition-shadow duration-300">
    <div v-if="!isEditing">
      <div class="flex justify-between items-start">
        <div>
          <h3 class="text-lg font-semibold text-slate-800 mb-1">{{ task.title }}</h3>
          <p v-if="task.assigned_username" class="text-sm text-slate-500">Assigned to: {{ task.assigned_username }}</p>
          <p v-else class="text-sm text-slate-500">Unassigned</p>
          <p v-if="task.due_date" class="text-sm text-slate-500">Due: {{ formatDate(task.due_date) }}</p>
        </div>
        <span 
          class="text-xs font-semibold uppercase px-3 py-1 rounded-full"
          :class="statusClass"
        >
          {{ task.status }}
        </span>
      </div>
      <p class="text-slate-600">{{ task.description }}</p>
      <div class="mt-4 flex justify-end space-x-2">
        <button @click.stop="assignToMe" class="text-green-500 hover:text-green-700 text-sm">Assign to Me</button>
        <button @click.stop="startEditing" class="text-blue-500 hover:text-blue-700 text-sm">Edit</button>
        <button @click.stop="confirmDelete" class="text-red-500 hover:text-red-700 text-sm">Delete</button>
        <button @click.stop="viewTask" class="text-purple-500 hover:text-purple-700 text-sm">Details</button>
      </div>
    </div>
    <div v-else>
      <div class="mb-3">
        <label for="edit-title" class="block text-sm font-medium text-slate-700">Title</label>
        <input 
          id="edit-title"
          v-model="editedTitle"
          type="text"
          class="mt-1 block w-full p-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <div class="mb-3">
        <label for="edit-description" class="block text-sm font-medium text-slate-700">Description</label>
        <textarea 
          id="edit-description"
          v-model="editedDescription"
          rows="3"
          class="mt-1 block w-full p-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        ></textarea>
      </div>
      <div class="mb-3">
        <label for="edit-due-date" class="block text-sm font-medium text-slate-700">Due Date</label>
        <input 
          id="edit-due-date"
          v-model="editedDueDate"
          type="date"
          class="mt-1 block w-full p-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <div class="mb-4">
        <label for="edit-status" class="block text-sm font-medium text-slate-700">Status</label>
        <select 
          id="edit-status"
          v-model="editedStatus"
          class="mt-1 block w-full p-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </div>
      <div class="flex justify-end space-x-2">
        <button @click="cancelEditing" class="px-3 py-1 border border-slate-300 rounded-md text-slate-700 hover:bg-slate-100 text-sm">Cancel</button>
        <button @click="saveChanges" class="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm">Save</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Task } from '../models/Task';

const props = defineProps<{ task: Task }>();
const emit = defineEmits(['update-task', 'delete-task', 'assign-task', 'view-task']);

const isEditing = ref(false);
const editedTitle = ref(props.task.title);
const editedDescription = ref(props.task.description);
const editedStatus = ref(props.task.status);
const editedDueDate = ref(props.task.due_date ? props.task.due_date.split('T')[0] : '');

const startEditing = () => {
  isEditing.value = true;
  editedTitle.value = props.task.title;
  editedDescription.value = props.task.description;
  editedStatus.value = props.task.status;
  editedDueDate.value = props.task.due_date ? props.task.due_date.split('T')[0] : '';
};

const cancelEditing = () => {
  isEditing.value = false;
};

const saveChanges = () => {
  emit('update-task', {
    id: props.task.id,
    title: editedTitle.value,
    description: editedDescription.value,
    status: editedStatus.value,
    assigned_user_id: props.task.assigned_user_id, // Keep existing assignment unless explicitly changed
    due_date: editedDueDate.value || undefined,
  });
  isEditing.value = false;
};

const assignToMe = () => { 
  emit('assign-task', props.task.id);
};

const confirmDelete = () => {
  if (confirm('Are you sure you want to delete this task?')) {
    emit('delete-task', props.task.id);
  }
};

const viewTask = () => {
  emit('view-task', props.task);
};

const formatDate = (dateString: string) => {
  const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const statusClass = computed(() => {
  const status = isEditing.value ? editedStatus.value : props.task.status;
  switch (status.toLowerCase()) {
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
