<script setup>
import { ref, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";

const query = ref("");
const results = ref([]);
const errorMessage = ref("");

// Load saved search when page opens
onMounted(() => {
  const savedQuery = localStorage.getItem("savedQuery");
  const savedResults = localStorage.getItem("savedResults");

  if (savedQuery) {
    query.value = savedQuery;
  }

  if (savedResults) {
    results.value = JSON.parse(savedResults);
  }
});

async function searchRecommendation() {
  // clear previous results
  results.value = [];
  errorMessage.value = "";
  try {
    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query.value, top_k: 10 }),
    });

    if (!response.ok) throw new Error("Failed to fetch recommendations");

    const data = await response.json();

    if (data.error) {
      errorMessage.value = data.error;
      results.value = [];
    } else {
      results.value = data.recommendations || []; // fallback if undefined

      // ⭐ Save query and results
      localStorage.setItem("savedQuery", query.value);
      localStorage.setItem("savedResults", JSON.stringify(results.value));
    }
  } catch (err) {
    console.error(err);
    errorMessage.value = err.message;
    results.value = [];
  }
}

// Clear saved search
// function clearSearch() {
//   query.value = "";
//   results.value = [];

//   localStorage.removeItem("savedQuery");
//   localStorage.removeItem("savedResults");
// }
</script>

<template>
  <Navbar>
    <h1 class="text-3xl font-bold mb-6">AI Recommendation Page</h1>

    <div class="mb-6">
      <input
        v-model="query"
        @keyup.enter="searchRecommendation"
        placeholder="Example: gaming laptop under 3000"
        class="border p-2 w-96 mr-3"
      />

      <button
        @click="searchRecommendation"
        class="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Search
      </button>
      <!-- <button
        @click="clearSearch"
        class="bg-gray-500 text-white px-4 py-2 rounded"
      >
        Clear
      </button> -->
    </div>

    <div v-if="errorMessage" class="text-red-500 mb-4">
      {{ errorMessage }}
    </div>

    <div v-if="results && results.length">
      <h2 class="text-xl font-semibold mb-4">Top Recommendations</h2>

      <div
        v-for="(item, index) in results"
        :key="index"
        class="border p-4 mb-3 rounded"
      >
        <p class="font-bold">{{ item.model }}</p>
        <p>Brand: {{ item.brand }}</p>
        <p>Price: RM {{ item.price }}</p>
        <p>RAM: {{ item.ram }}</p>
        <p>SSD: {{ item.ssd }}</p>
        <p>GPU: {{ item.gpu }}</p>
      </div>
    </div>

    <div v-else-if="!errorMessage">
      <p>No results found.</p>
    </div>
  </Navbar>
</template>
