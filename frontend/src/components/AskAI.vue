<template>
  <div>
    <h4 class="text-lg font-semibold text-slate-700 mt-6 mb-2">Ask AI a Question</h4>
    <textarea v-model="question" placeholder="Ask a question about the project..." class="w-full p-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"></textarea>
    <div class="flex justify-end space-x-2">
        <button @click="ask" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Ask</button>
      </div>
    <div v-if="answer" class="mt-4 p-4 bg-gray-100 rounded-md">
      <h4>Answer:</h4>
       <div v-html="renderedAnswer"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { askTaskQuestion, askSubtaskQuestion, askProjectQuestion } from '../services/api';
import { marked } from 'marked';

const props = defineProps<{ projectId: string, taskId: string | null, subtaskId: string | null}>();

const question = ref('');
const answer = ref('');
const isAsking = ref(false);

const renderedAnswer = computed(() => marked(answer.value));


const ask = async () => {
  if (!question.value) return;
  isAsking.value = true;
  answer.value = '';
  try {
    if(props.subtaskId != null && props.taskId != null){
      const result = await askSubtaskQuestion(props.projectId, props.taskId, props.subtaskId, question.value);
      answer.value = result;
    }else if (props.taskId != null){
      const result = await askTaskQuestion(props.projectId, props.taskId, question.value);
      answer.value = result;
    }else{
      const result = await askProjectQuestion(props.projectId, question.value);
      answer.value = result;
    }
  } catch (err: any) {
    answer.value = 'Error: Could not get an answer.';
  } finally {
    isAsking.value = false;
  }
};
</script>