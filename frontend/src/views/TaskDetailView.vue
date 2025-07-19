<template>
  <div class="max-w-3xl mx-auto p-6 bg-white rounded-xl shadow-lg mt-6">
    <button @click="$router.back()" class="text-blue-600 hover:text-blue-800 mb-4 flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      Back to Tasks
    </button>

    <div v-if="loading" class="flex justify-center items-center p-10">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-md mt-6">
      <h3 class="font-bold">Error</h3>
      <p>{{ error }}</p>
    </div>

    <div v-else-if="task">
      <h2 class="text-2xl font-semibold text-slate-800 mb-2">{{ task.title }}</h2>
      <p class="text-slate-600 mb-4">{{ task.description }}</p>
      <p v-if="task.assigned_username" class="text-sm text-slate-500">Assigned to: {{ task.assigned_username }}</p>
      <p v-else class="text-sm text-slate-500">Unassigned</p>
      <p v-if="task.due_date" class="text-sm text-slate-500">Due: {{ formatDate(task.due_date) }}</p>

      <h4 class="text-lg font-semibold text-slate-700 mt-6 mb-2">Subtasks</h4>
      <div class="mb-4">
        <div v-if="task.subtasks && task.subtasks.length > 0" class="space-y-2 mb-3">
          <div v-for="subtask in task.subtasks" :key="subtask.id" class="flex items-center bg-gray-100 p-2 rounded-md">
            <input type="checkbox" :checked="subtask.status === 'done'" @change="handleUpdateSubtask({ ...subtask, status: ($event.target as HTMLInputElement).checked ? 'done' : 'todo' })" class="mr-2">
            <span :class="{'line-through text-slate-500': subtask.status === 'done'}">{{ subtask.title }}</span>
            <p v-if="subtask.description" class="text-sm text-slate-500 ml-4">{{ subtask.description }}</p>
          </div>
        </div>
        <div v-else class="text-slate-500 text-center mb-3">No subtasks yet.</div>
        <div class="flex gap-2">
          <input
            v-model="subtaskObjective"
            type="text"
            placeholder="Generate subtasks for..."
            class="flex-grow p-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button @click="handleGenerateSubtasks" :disabled="generatingSubtasks" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed">
            <span v-if="generatingSubtasks">Generating...</span>
            <span v-else>Generate</span>
          </button>
        </div>
      </div>

      <h4 class="text-lg font-semibold text-slate-700 mt-6 mb-2">Comments</h4>
      <div class="max-h-60 overflow-y-auto mb-4 border p-3 rounded-md bg-gray-50">
        <div v-if="comments.length === 0" class="text-slate-500 text-center">No comments yet.</div>
        <div v-for="comment in comments" :key="comment.id" class="mb-3 pb-3 border-b last:border-b-0 last:pb-0">
          <p class="text-slate-700 text-sm">{{ comment.content }}</p>
          <p class="text-xs text-slate-500 text-right">- {{ comment.username }} on {{ formatDate(comment.created_at) }}</p>
        </div>
      </div>
      <textarea
        v-model="newCommentContent"
        placeholder="Add a new comment..."
        rows="3"
        class="w-full p-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
      ></textarea>
      <div class="flex justify-end space-x-2">
        <button @click="handleAddComment" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Add Comment</button>
      </div>

      <AskAI :projectId="projectId" :taskId="taskId" :subtaskId="null" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getTask, getComments, createComment, generateSubtasks, getSubtasks, updateSubtask } from '../services/api';
import type { Task } from '../models/Task';
import type { Comment } from '../models/Comment';
import type { Subtask } from '../models/Subtask';
import AskAI from '@/components/AskAI.vue';

const route = useRoute();
const projectId = ref(route.params.projectId as string);
const taskId = ref(route.params.taskId as string);

const task = ref<Task | null>(null);
const comments = ref<Comment[]>([]);
const newCommentContent = ref('');
const subtaskObjective = ref('');
const loading = ref(false);
const generatingSubtasks = ref(false);
const error = ref<string | null>(null);

const fetchTaskDetails = async () => {
  loading.value = true;
  error.value = null;
  try {
    task.value = await getTask(projectId.value, taskId.value);
    comments.value = (await getComments(projectId.value, taskId.value)) as Comment[];
    if (task.value) {
      task.value.subtasks = (await getSubtasks(projectId.value, taskId.value)) as Subtask[];
    }
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const handleAddComment = async () => {
  if (!task.value || !newCommentContent.value.trim()) return;
  try {
    const newComment = await createComment(projectId.value, task.value.id, newCommentContent.value);
    comments.value.push(newComment);
    newCommentContent.value = '';
  } catch (err: any) {
    console.error("Error adding comment:", err);
    alert(`Failed to add comment: ${err.message}`);
  }
};

const handleGenerateSubtasks = async () => {
  if (!task.value || !subtaskObjective.value.trim()) return;
  generatingSubtasks.value = true;
  try {
    const newSubtasks = await generateSubtasks(projectId.value, task.value.id, subtaskObjective.value);
    if (task.value.subtasks) {
      task.value.subtasks.push(...newSubtasks);
    } else {
      task.value.subtasks = newSubtasks;
    }
    subtaskObjective.value = '';
  } catch (err: any) {
    console.error("Error generating subtasks:", err);
    alert(`Failed to generate subtasks: ${err.message}`);
  } finally {
    generatingSubtasks.value = false;
  }
};

const handleUpdateSubtask = async (subtask: Subtask) => {
  if (!task.value) return;
  try {
    const updated = await updateSubtask(projectId.value, task.value.id, subtask.id, subtask);
    if (task.value.subtasks) {
      const index = task.value.subtasks.findIndex(s => s.id === updated.id);
      if (index !== -1) {
        task.value.subtasks[index] = updated;
      }
    }
  } catch (err: any) {
    console.error("Error updating subtask:", err);
    alert(`Failed to update subtask: ${err.message}`);
  }
};

const formatDate = (dateString: string) => {
  const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

onMounted(() => {
  watch([projectId, taskId], fetchTaskDetails, { immediate: true });
});
</script>
