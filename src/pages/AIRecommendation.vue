<script setup>
import { ref } from "vue";

const query = ref("");
const results = ref([]);

async function searchRecommendation() {
  const response = await fetch("http://127.0.0.1:8000/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query.value,
    }),
  });

  const data = await response.json();

  results.value = data;
}
</script>

<template>
  <div class="p-10">
    <h1 class="text-3xl font-bold mb-6">AI Recommendation Page</h1>

    <div class="mb-6">
      <input
        v-model="query"
        placeholder="Example: gaming laptop under 3000"
        class="border p-2 w-96 mr-3"
      />

      <button
        @click="searchRecommendation"
        class="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Search
      </button>
    </div>

    <div v-if="results.length">
      <h2 class="text-xl font-semibold mb-4">Top Recommendations</h2>

      <div
        v-for="item in results"
        :key="item.id"
        class="border p-4 mb-3 rounded"
      >
        <p class="font-bold">{{ item.name }}</p>

        <p>Brand: {{ item.brand }}</p>

        <p>Price: RM {{ item.price_rm }}</p>

        <p>Processor: {{ item.processor }}</p>
      </div>
    </div>
  </div>
</template>
