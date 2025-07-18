<template>
  <div id="app" class="flex flex-col min-h-screen bg-slate-100 font-sans">
    <Header />
    <main class="flex-grow container mx-auto p-4 md:p-8">
      <router-view />
    </main>
    <footer class="bg-gray-800 text-white text-center p-4 mt-8">
      <p>&copy; 2025 Project Manager AI. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import Header from './components/Header.vue';
</script>