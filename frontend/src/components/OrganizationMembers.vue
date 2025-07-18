<template>
  <div class="bg-white p-6 rounded-xl shadow-lg mb-6">
    <h2 class="text-2xl font-semibold text-slate-800 mb-4">Manage Members for {{ organizationName }}</h2>

    <div v-if="loading" class="flex justify-center items-center p-10">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-md mt-6">
      <h3 class="font-bold">Error</h3>
      <p>{{ error }}</p>
    </div>

    <div class="mb-6">
      <h3 class="text-xl font-semibold text-slate-700 mb-3">Current Members</h3>
      <ul v-if="currentMembers.length > 0" class="space-y-2">
        <li v-for="member in currentMembers" :key="member.id" class="flex justify-between items-center bg-slate-50 p-3 rounded-md shadow-sm">
          <span>{{ member.username }}</span>
          <button 
            @click="removeMember(member.id)"
            class="bg-red-500 text-white px-3 py-1 rounded-md text-sm hover:bg-red-600 transition-colors"
          >
            Remove
          </button>
        </li>
      </ul>
      <p v-else class="text-slate-600">No members in this organization yet.</p>
    </div>

    <div>
      <h3 class="text-xl font-semibold text-slate-700 mb-3">Add New Member</h3>
      <div class="flex flex-col sm:flex-row gap-4">
        <select
          v-model="selectedUserToAdd"
          class="flex-grow p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
        >
          <option value="" disabled>Select a user</option>
          <option v-for="user in availableUsers" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
        <button
          @click="addMember"
          :disabled="!selectedUserToAdd || addingMember"
          class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors shadow-md hover:shadow-lg"
        >
          <span v-if="addingMember">Adding...</span>
          <span v-else>Add User</span>
        </button>
      </div>
      <p v-if="addError" class="text-red-500 mt-2">{{ addError }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { getOrganizationById, getAllUsers, addUserToOrganization, removeUserFromOrganization } from '../services/api';
import type { Organization } from '../models/Organization';

const props = defineProps<{ orgId: string }>();

const organization = ref<Organization | null>(null);
const allUsers = ref<{ id: string; username: string }[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const addError = ref<string | null>(null);
const selectedUserToAdd = ref('');
const addingMember = ref(false);

const organizationName = computed(() => organization.value?.name || 'Loading...');
const currentMembers = computed(() => organization.value?.members || []);
const availableUsers = computed(() => {
  const memberIds = new Set(currentMembers.value.map((m:any) => m.id));
  return allUsers.value.filter(user => !memberIds.has(user.id));
});

const fetchOrganizationAndUsers = async () => {
  loading.value = true;
  error.value = null;
  try {
    organization.value = await getOrganizationById(props.orgId);
    allUsers.value = await getAllUsers();
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const addMember = async () => {
  if (!selectedUserToAdd.value) return;
  addingMember.value = true;
  addError.value = null;
  try {
    organization.value = await addUserToOrganization(props.orgId, selectedUserToAdd.value);
    selectedUserToAdd.value = ''; // Clear selection
  } catch (err: any) {
    addError.value = err.message;
  } finally {
    addingMember.value = false;
  }
};

const removeMember = async (userId: string) => {
  if (confirm('Are you sure you want to remove this user from the organization?')) {
    try {
      organization.value = await removeUserFromOrganization(props.orgId, userId);
    } catch (err: any) {
      alert(`Failed to remove user: ${err.message}`);
    }
  }
};

onMounted(fetchOrganizationAndUsers);
</script>
