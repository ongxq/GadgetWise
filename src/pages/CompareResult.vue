<script setup>
import { useRoute } from "vue-router";
import { onMounted, ref } from "vue";
import Chart from "chart.js/auto";
import Navbar from "../components/Navbar.vue";

const route = useRoute();
const laptops = ref([]);

// Generate a color for each laptop
function getColor(index) {
  const colors = [
    "#FF6384",
    "#36A2EB",
    "#FFCE56",
    "#4BC0C0",
    "#9966FF",
    "#FF9F40",
    "#C9CBCF",
    "#8DD9B9",
    "#FF6F91",
    "#6A4C93",
  ];
  return colors[index % colors.length];
}

// Shorten model names for charts
function getShortModel(model) {
  return model.split("(")[0].trim();
}

const features = [
  { label: "Brand", key: "Brand" },
  { label: "Price (RM)", key: "Price (RM)" },
  { label: "RAM", key: "Ram" },
  { label: "SSD", key: "SSD" },
  { label: "Display", key: "Display" },
  { label: "Graphics", key: "Graphics" },
  { label: "VRAM", key: "VRAM" },
  { label: "Battery", key: "Battery" },
];

onMounted(() => {
  const stored = localStorage.getItem("compareLaptops");
  if (!stored) {
    console.warn("No laptops received");
    return;
  }

  laptops.value = JSON.parse(stored);

  // Prepare datasets for charts (one dataset per model for unique colors)
  const priceDatasets = laptops.value.map((l, i) => ({
    label: getShortModel(l.Model),
    data: [l["Price (RM)"]],
    backgroundColor: getColor(i),
  }));

  const ramDatasets = laptops.value.map((l, i) => ({
    label: getShortModel(l.Model),
    data: [l["RAM (filter)"]],
    backgroundColor: getColor(i),
  }));

  const vramDatasets = laptops.value.map((l, i) => ({
    label: getShortModel(l.Model),
    data: [l.VRAM],
    backgroundColor: getColor(i),
  }));

  // Create Price chart (horizontal)
  new Chart(document.getElementById("priceChart"), {
    type: "bar",
    data: {
      labels: ["Price (RM)"], // single category
      datasets: priceDatasets,
    },
    options: {
      indexAxis: "x", // horizontal bars
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
          position: "top",
          labels: { boxWidth: 20, padding: 10 },
        },
        title: {
          display: true,
          text: "Price Comparison",
          font: { size: 18 },
        },
      },
      scales: {
        x: { beginAtZero: true },
      },
    },
  });

  // RAM chart
  new Chart(document.getElementById("ramChart"), {
    type: "bar",
    data: {
      labels: ["RAM (GB)"],
      datasets: ramDatasets,
    },
    options: {
      indexAxis: "x",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
          position: "top",
          labels: { boxWidth: 20, padding: 10 },
        },
        title: {
          display: true,
          text: "RAM Comparison",
          font: { size: 18 },
        },
      },
      scales: { x: { beginAtZero: true } },
    },
  });

  // VRAM chart
  new Chart(document.getElementById("vramChart"), {
    type: "bar",
    data: {
      labels: ["VRAM (GB)"],
      datasets: vramDatasets,
    },
    options: {
      indexAxis: "x",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
          position: "top",
          labels: { boxWidth: 20, padding: 10 },
        },
        title: {
          display: true,
          text: "VRAM Comparison",
          font: { size: 18 },
        },
      },
      scales: { x: { beginAtZero: true } },
    },
  });
});
</script>

<template>
  <Navbar>
    <div class="p-10">
      <h1 class="text-3xl font-bold mb-8">Laptop Comparison</h1>

      <!-- Comparison Table -->
      <div class="overflow-x-auto">
        <table class="table-auto border w-full text-center">
          <thead>
            <tr class="bg-gray-200">
              <th class="border p-3">Feature</th>
              <th v-for="l in laptops" :key="l.id" class="border p-3">
                {{ l.Model }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="feature in features" :key="feature.key">
              <td class="border p-2 font-semibold bg-gray-100">
                {{ feature.label }}
              </td>
              <td v-for="l in laptops" :key="l.id" class="border p-2">
                {{ l[feature.key] || "-" }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Charts -->
      <!-- Graph Comparison Wrapper -->
      <div class="mt-10">
        <h2 class="text-2xl font-bold mb-4">Graph Comparison</h2>

        <!-- Custom Legend for all models -->
        <div class="flex flex-wrap gap-4 mb-6">
          <div
            v-for="(l, index) in laptops"
            :key="l.id"
            class="flex items-center gap-1 text-sm"
          >
            <span
              class="w-4 h-4 rounded"
              :style="{ backgroundColor: getColor(index) }"
            ></span>
            <span>{{ getShortModel(l.Model) }}</span>
          </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid md:grid-cols-3 gap-10">
          <div
            class="w-full h-96 bg-white border-4 border-blue-900 rounded-lg p-4"
          >
            <canvas id="priceChart"></canvas>
          </div>
          <div
            class="w-full h-96 bg-white border-4 border-blue-900 rounded-lg p-4"
          >
            <canvas id="ramChart"></canvas>
          </div>
          <div
            class="w-full h-96 bg-white border-4 border-blue-900 rounded-lg p-4"
          >
            <canvas id="vramChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </Navbar>
</template>
