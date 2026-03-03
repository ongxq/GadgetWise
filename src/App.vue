<template>
  <router-view />
</template>

<script setup>
import { ref } from "vue";

const currentPage = ref("login"); // or 'signup'
</script>

<style scoped></style>
