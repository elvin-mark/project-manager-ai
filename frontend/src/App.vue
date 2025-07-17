<template>
  <div id="app" class="bg-slate-100 min-h-screen font-sans">
    <Header />
    <main class="container mx-auto p-4 md:p-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from './components/Header.vue';
</script>