<template>
  <div class="ask-ai-container">
    <h3>Ask AI a Question</h3>
    <textarea v-model="question" placeholder="Ask a question about the project..."></textarea>
    <button @click="ask" :disabled="isAsking">Ask</button>
    <div v-if="answer" class="answer">
      <h4>Answer:</h4>
      <p>{{ answer }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { askTaskQuestion, askSubtaskQuestion, askProjectQuestion } from '../services/api';

const props = defineProps<{ projectId: string, taskId: string, subtaskId: string }>();

const question = ref('');
const answer = ref('');
const isAsking = ref(false);

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

<style scoped>
.ask-ai-container {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
textarea {
  width: 100%;
  min-height: 80px;
  margin-bottom: 10px;
}
</style>
