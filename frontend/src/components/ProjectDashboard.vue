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
      <div class="mt-6">
        <button @click="fetchAiSummary" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Get AI Summary
        </button>
      </div>
      <div class="mt-6">
        <h4 class="text-lg font-semibold text-slate-700 mb-2">Ask a Question</h4>
        <div class="flex">
          <input v-model="question" type="text" class="border border-gray-300 rounded-l-md p-2 w-full" placeholder="Ask something about the project..." :disabled="isAsking">
          <button @click="askQuestion" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-r-md" :disabled="isAsking">
            <span v-if="isAsking">Asking...</span>
            <span v-else>Ask</span>
          </button>
        </div>
        <div v-if="isAsking" class="mt-4 text-center text-slate-500">
            Getting an answer...
        </div>
        <div v-if="answer && !isAsking" class="mt-4 p-4 bg-gray-100 rounded-md">
          <div v-html="renderedAnswer"></div>
        </div>
      </div>
      <div v-if="showSummaryModal" class="fixed z-10 inset-0 overflow-y-auto">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 transition-opacity" aria-hidden="true">
            <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
          </div>
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
          <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">AI Project Summary</h3>
              <div class="mt-2">
                <div v-html="renderedSummary"></div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button @click="showSummaryModal = false" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { getProjectSummary, getProjectAiSummary, askProjectQuestion } from '../services/api';
import { marked } from 'marked';

const props = defineProps<{ projectId: string }>();

const dashboardData = ref({
  total_tasks: 0,
  todo_tasks: 0,
  in_progress_tasks: 0,
  done_tasks: 0,
});
const loading = ref(false);
const error = ref<string | null>(null);
const aiSummary = ref('');
const showSummaryModal = ref(false);
const question = ref('');
const answer = ref('');
const isAsking = ref(false);

const renderedSummary = computed(() => marked(aiSummary.value));
const renderedAnswer = computed(() => marked(answer.value));

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

const fetchAiSummary = async () => {
  try {
    const summary = await getProjectAiSummary(props.projectId);
    aiSummary.value = summary;
    showSummaryModal.value = true;
  } catch (err: any) {
    error.value = err.message;
  }
};

const askQuestion = async () => {
  if (!question.value) return;
  isAsking.value = true;
  answer.value = '';
  try {
    const result = await askProjectQuestion(props.projectId, question.value);
    answer.value = result;
  } catch (err: any) {
    error.value = err.message;
  } finally {
    isAsking.value = false;
  }
};

watch(() => props.projectId, fetchProjectSummary, { immediate: true });
</script>
