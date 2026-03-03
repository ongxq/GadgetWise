<script setup>
import { ref } from "vue";
import Navbar from "../components/AdminNavbar.vue";

const isOpen = ref(true);

const toggleSidebar = () => {
  isOpen.value = !isOpen.value;
};
</script>

<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <Navbar :isOpen="isOpen" :toggleSidebar="toggleSidebar" />

    <!-- Main Content -->
    <div
      class="flex-1 transition-all duration-300 p-8"
      :class="isOpen ? 'ml-64' : 'ml-20'"
    >
      <h1 class="text-2xl font-bold">Admin Dashboard</h1>
    </div>
  </div>
</template>
