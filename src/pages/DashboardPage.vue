<script setup>
import { ref } from "vue";
import Navbar from "../components/Navbar.vue";

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
    ></div>
  </div>
</template>
