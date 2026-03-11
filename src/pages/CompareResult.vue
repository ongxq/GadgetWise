<script setup>
import { useRoute } from "vue-router";
import { onMounted, ref } from "vue";
import Chart from "chart.js/auto";
import Navbar from "../components/Navbar.vue";

const route = useRoute();

/* Safe laptops data */
//const laptops = ref(history.state?.laptops || []);

const laptops = ref([]);

onMounted(() => {
  const stored = localStorage.getItem("compareLaptops");

  if (!stored) {
    console.warn("No laptops received");
    return;
  }

  laptops.value = JSON.parse(stored);

  const ctx = document.getElementById("priceChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: laptops.value.map((l) => l.Brand),
      datasets: [
        {
          label: "Price (RM)",
          data: laptops.value.map((l) => l["Price (RM)"]),
        },
      ],
    },
  });
});
</script>

<template>
  <Navbar>
    <div class="p-10">
      <h1 class="text-3xl font-bold mb-6">Laptop Comparison</h1>

      <!-- Table -->
      <table class="table-auto border w-full mb-10">
        <thead>
          <tr class="bg-gray-200">
            <th class="border p-2">Brand</th>
            <th class="border p-2">Price</th>
            <th class="border p-2">RAM</th>
            <th class="border p-2">SSD</th>
            <th class="border p-2">VRAM</th>
            <th class="border p-2">Battery</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="l in laptops" :key="l.Brand">
            <td class="border p-2">
              {{ l.Brand }}
            </td>

            <td class="border p-2">RM {{ l["Price (RM)"] }}</td>

            <td class="border p-2">{{ l.Ram }} GB</td>

            <td class="border p-2">{{ l.SSD }} GB</td>

            <td class="border p-2">{{ l.VRAM }} GB</td>

            <td class="border p-2">{{ l.Battery }} Wh</td>
          </tr>
        </tbody>
      </table>

      <!-- Chart -->
      <div class="w-full max-w-3xl">
        <canvas id="priceChart"></canvas>
      </div>
    </div>
  </Navbar>
</template>
