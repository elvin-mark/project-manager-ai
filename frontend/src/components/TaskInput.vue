<template>
  <div class="p-4">
    <form @submit.prevent="handleSubmit">
      <div class="flex gap-4">
        <input
          v-model="objective"
          type="text"
          placeholder="Enter your high-level objective..."
          class="flex-grow p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          :disabled="loading"
          class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
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

const objective = ref('');
const loading = ref(false);

const emit = defineEmits(['generate']);

const handleSubmit = () => {
  if (objective.value.trim()) {
    emit('generate', objective.value);
  }
};
</script>
