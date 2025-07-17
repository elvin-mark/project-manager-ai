<template>
  <div class="bg-white p-6 rounded-xl shadow-lg mb-6">
    <h2 class="text-2xl font-semibold text-slate-800 mb-4">Your Projects</h2>
    
    <form @submit.prevent="handleCreateProject" class="mb-6">
      <div class="flex flex-col sm:flex-row gap-4">
        <input
          v-model="newProjectName"
          type="text"
          placeholder="New Project Name"
          class="flex-grow p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
          required
        />
        <input
          v-model="newProjectDescription"
          type="text"
          placeholder="Project Description (optional)"
          class="flex-grow p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
        />
        <button
          type="submit"
          :disabled="creatingProject"
          class="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors shadow-md hover:shadow-lg"
        >
          <span v-if="creatingProject">Creating...</span>
          <span v-else>Create Project</span>
        </button>
      </div>
      <p v-if="createError" class="text-red-500 mt-2">{{ createError }}</p>
    </form>

    <div v-if="loading" class="flex justify-center items-center p-10">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-md mt-6">
      <h3 class="font-bold">Error</h3>
      <p>{{ error }}</p>
    </div>

    <div v-if="projects.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="project in projects" 
        :key="project.id" 
        @click="goToProject(project.id)"
        class="bg-slate-50 p-5 rounded-xl shadow-md border border-slate-200 cursor-pointer hover:shadow-lg hover:border-blue-300 transition-all duration-200"
      >
        <h3 class="text-xl font-semibold text-slate-700 mb-2">{{ project.name }}</h3>
        <p class="text-slate-600 text-sm">{{ project.description || 'No description provided.' }}</p>
        <div class="mt-3 text-right">
          <button @click.stop="deleteProject(project.id)" class="text-red-500 hover:text-red-700 text-sm">
            Delete
          </button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="text-center py-10 px-4 bg-white rounded-xl shadow-md">
      <h3 class="text-lg font-medium text-slate-600">No projects yet.</h3>
      <p class="text-slate-500">Create a new project to get started.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { createProject, getProjects, deleteProject as apiDeleteProject } from '../services/api';
import type { Project } from '../models/Project';

const projects = ref<Project[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const newProjectName = ref('');
const newProjectDescription = ref('');
const creatingProject = ref(false);
const createError = ref<string | null>(null);

const router = useRouter();

const fetchProjects = async () => {
  loading.value = true;
  error.value = null;
  try {
    projects.value = await getProjects();
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const handleCreateProject = async () => {
  if (!newProjectName.value.trim()) {
    createError.value = 'Project name cannot be empty.';
    return;
  }
  creatingProject.value = true;
  createError.value = null;
  try {
    const newProject = await createProject(newProjectName.value, newProjectDescription.value);
    projects.value.push(newProject);
    newProjectName.value = '';
    newProjectDescription.value = '';
  } catch (err: any) {
    createError.value = err.message;
  } finally {
    creatingProject.value = false;
  }
};

const deleteProject = async (projectId: string) => {
  if (confirm('Are you sure you want to delete this project and all its tasks?')) {
    try {
      await apiDeleteProject(projectId);
      projects.value = projects.value.filter(p => p.id !== projectId);
    } catch (err: any) {
      alert(`Failed to delete project: ${err.message}`);
    }
  }
};

const goToProject = (projectId: string) => {
  router.push({ name: 'tasks', params: { projectId: projectId } });
};

onMounted(fetchProjects);
</script>
