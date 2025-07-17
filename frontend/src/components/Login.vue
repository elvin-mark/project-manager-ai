<template>
  <div class="max-w-md mx-auto mt-10 bg-white p-8 rounded-xl shadow-lg">
    <h2 class="text-2xl font-semibold text-slate-800 mb-6 text-center">Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-4">
        <label for="username" class="block text-sm font-medium text-slate-700">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          class="mt-1 block w-full p-3 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>
      <div class="mb-6">
        <label for="password" class="block text-sm font-medium text-slate-700">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="mt-1 block w-full p-3 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-blue-600 text-white px-4 py-3 rounded-md font-semibold hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading">Logging in...</span>
        <span v-else>Login</span>
      </button>
      <p v-if="error" class="text-red-500 text-sm mt-4 text-center">{{ error }}</p>
    </form>
    <p class="mt-6 text-center text-sm text-slate-600">
      Don't have an account? <router-link to="/register" class="text-blue-600 hover:underline">Register here</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '../services/api';

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  try {
    await login(username.value, password.value);
    router.push('/'); // Redirect to projects page on successful login
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>
