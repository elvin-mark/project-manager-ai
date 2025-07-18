<template>
  <header class="bg-white shadow-md">
    <div class="container mx-auto px-4 md:px-8 py-4 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">Adept AI Project Manager</h1>
      <button
        v-if="isLoggedIn"
        @click="handleLogout"
        class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors"
      >
        Logout
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoggedIn = ref(false);

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('access_token');
};

const handleLogout = () => {
  localStorage.removeItem('access_token');
  isLoggedIn.value = false;
  router.push('/login');
};

// Initial check
onMounted(() => {
  checkLoginStatus();

  // Listen to route changes
  router.afterEach(() => {
    checkLoginStatus();
  });

  // Listen to storage events (for changes from other tabs)
  window.addEventListener('storage', checkLoginStatus);
});

onUnmounted(() => {
  window.removeEventListener('storage', checkLoginStatus);
});
</script>