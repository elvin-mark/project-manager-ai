<template>
  <div class="bg-white p-6 rounded-xl shadow-lg">
    <h2 class="text-xl font-semibold text-slate-700 mb-4">Start a New Objective</h2>
    <form @submit.prevent="handleSubmit">
      <div class="flex flex-col sm:flex-row gap-4">
        <input
          v-model="objective"
          type="text"
          placeholder="e.g., Implement user authentication with JWT"
          class="flex-grow p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
        />
        <button
          type="submit"
          :disabled="loading"
          class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors shadow-md hover:shadow-lg"
        >
          <span v-if="loading">Generating...</span>
          <span v-else>Generate Tasks</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

defineProps<{ loading: boolean }>();

const objective = ref('');
const emit = defineEmits(['generate']);

const handleSubmit = () => {
  if (objective.value.trim()) {
    emit('generate', objective.value);
  }
};
</script>
