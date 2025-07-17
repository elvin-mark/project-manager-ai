<template>
  <div class="bg-white p-6 rounded-xl shadow-lg mb-6">
    <h2 class="text-2xl font-semibold text-slate-800 mb-4">Your Organizations</h2>
    
    <form @submit.prevent="handleCreateOrganization" class="mb-6">
      <div class="flex flex-col sm:flex-row gap-4">
        <input
          v-model="newOrgName"
          type="text"
          placeholder="New Organization Name"
          class="flex-grow p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
          required
        />
        <input
          v-model="newOrgDescription"
          type="text"
          placeholder="Organization Description (optional)"
          class="flex-grow p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
        />
        <button
          type="submit"
          :disabled="creatingOrganization"
          class="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors shadow-md hover:shadow-lg"
        >
          <span v-if="creatingOrganization">Creating...</span>
          <span v-else>Create Organization</span>
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

    <div v-if="organizations.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="org in organizations" 
        :key="org.id" 
        class="bg-slate-50 p-5 rounded-xl shadow-md border border-slate-200 transition-all duration-200"
      >
        <h3 class="text-xl font-semibold text-slate-700 mb-2">{{ org.name }}</h3>
        <p class="text-slate-600 text-sm">{{ org.description || 'No description provided.' }}</p>
        <div class="mt-3 flex justify-end space-x-2">
          <button @click="goToOrganizationProjects(org.id)" class="text-blue-500 hover:text-blue-700 text-sm">View Projects</button>
          <button @click="goToManageMembers(org.id)" class="text-purple-500 hover:text-purple-700 text-sm">Manage Members</button>
          <button @click.stop="deleteOrganization(org.id)" class="text-red-500 hover:text-red-700 text-sm">
            Delete
          </button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="text-center py-10 px-4 bg-white rounded-xl shadow-md">
      <h3 class="text-lg font-medium text-slate-600">No organizations yet.</h3>
      <p class="text-slate-500">Create a new organization to get started.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { createOrganization, getOrganizations, deleteOrganization as apiDeleteOrganization } from '../services/api';
import type { Organization } from '../models/Organization';

const organizations = ref<Organization[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const newOrgName = ref('');
const newOrgDescription = ref('');
const creatingOrganization = ref(false);
const createError = ref<string | null>(null);

const router = useRouter();

const fetchOrganizations = async () => {
  loading.value = true;
  error.value = null;
  try {
    organizations.value = await getOrganizations();
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const handleCreateOrganization = async () => {
  if (!newOrgName.value.trim()) {
    createError.value = 'Organization name cannot be empty.';
    return;
  }
  creatingOrganization.value = true;
  createError.value = null;
  try {
    const newOrg = await createOrganization(newOrgName.value, newOrgDescription.value);
    organizations.value.push(newOrg);
    newOrgName.value = '';
    newOrgDescription.value = '';
  } catch (err: any) {
    createError.value = err.message;
  } finally {
    creatingOrganization.value = false;
  }
};

const deleteOrganization = async (orgId: string) => {
  if (confirm('Are you sure you want to delete this organization and all its projects/tasks?')) {
    try {
      await apiDeleteOrganization(orgId);
      organizations.value = organizations.value.filter(o => o.id !== orgId);
    } catch (err: any) {
      alert(`Failed to delete organization: ${err.message}`);
    }
  }
};

const goToOrganizationProjects = (orgId: string) => {
  router.push({ name: 'organization-projects', params: { orgId: orgId } });
};

const goToManageMembers = (orgId: string) => {
  router.push({ name: 'organization-members', params: { orgId: orgId } });
};

onMounted(fetchOrganizations);
</script>