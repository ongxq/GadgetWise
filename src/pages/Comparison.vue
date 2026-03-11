<script setup>
import { ref, onMounted } from "vue";
import { supabase } from "../supabase";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";

const router = useRouter();

const laptops = ref([]);
const filteredLaptops = ref([]);
const selected = ref([]);

const filters = ref({
  brand: "",
  gaming: "",
  priceMin: "",
  priceMax: "",
  cpuBrand: "",
  cpuSeries: "",
  ram: "",
  ssd: "",
  gpu: "",
  vram: "",
  os: "",
  displayInches: "",
  pixel: "",
  touch: "",
});

// default image if brand not found
const defaultImage =
  "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Laptop.jpg/640px-Laptop.jpg";

// map brand to image URLs
function getBrandImage(brand, id) {
  const images = {
    Acer: [
      "https://onxhuoxmggqudwfeedes.supabase.co/storage/v1/object/sign/laptop_pic/acer.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV85OWRmZGQzNS04YjQ3LTQ0YmEtOTkxYi0yZTg2ZThlYjZjYmMiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJsYXB0b3BfcGljL2FjZXIuanBnIiwiaWF0IjoxNzczMTQwMjQzLCJleHAiOjE4MDQ2NzYyNDN9.QV9DA4a0JcL7AW-f64Oew4RmJYL45bOQtCPxJb8GzLc",
      "https://technave.com/data/files/article/202601020152042327.jpg",
      "https://technave.com/data/files/article/202510270315107462.jpg",
    ],
    Apple: [
      "https://technave.com/data/files/mall/article/202012051306288171.jpg",
      "https://technave.com/data/files/article/202403050250111685.jpg",
      "https://technave.com/data/files/mall/article/202009070554371260.jpg",
    ],

    Asus: [
      "https://technave.com/data/files/article/202502190941278114.jpg",
      "https://technave.com/data/files/article/202407170640102270.jpg",
      "https://technave.com/data/files/article/202405100246011605.jpg",
    ],

    Avita: [
      "https://www.ect.my/image/ectmy/image/cache/data/all_product_images/product-12136/AVITA%20LIBER%20V14-i7%20GRY%202-850x850.jpg",
      "https://m.media-amazon.com/images/I/61UDGBWyGZL._AC_UF1000,1000_QL80_.jpg",
      "https://5.imimg.com/data5/SELLER/Default/2023/8/336395779/IA/SI/CZ/143558492/buy-new-avita-laptop-core-i3-10th-gen-4gb-ram-and-256gb-storage.png",
    ],

    AXL: [
      "https://axlworld.com/wp-content/uploads/2025/05/image-4-2-300x260.png",
      "https://5.imimg.com/data5/SELLER/Default/2023/5/312121289/JE/QU/IA/256711/laptop-15-inch-1-a-500x500.jpg",
    ],
    Chuwi: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpvaX52aKzHwklgF2N-wajXaJ6GO03t57QPg&s",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNZoQni_zVuPmLMMkn_ru-rtPw0QqkgSD6Jw&s",
    ],

    Colorful: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5VU06vRcgKQvXLEYmljbBFB0k2O8dsBv6Kg&s",
    ],

    Dell: [
      "https://technave.com/data/files/article/202602120140401702.jpg",
      "https://technave.com/data/files/article/202507070819344303.jpg",
      "https://technave.com/data/files/article/202503130727135300.jpg",
    ],

    Fujitsu: [
      "https://www.bhphotovideo.com/images/fb/fujitsu_spfc_e544_001_e544_i5_4210m_4gb_500gb_windows7p_windows8_1_14_1082600.jpg",
    ],
    Gigabyte: [
      "https://cdn1.npcdn.net/images/d7ca3336986a9caf62cf0362d98ec479_1711278978.webp?md5id=a390ff7af39b581d079075b5f848662e&new_width=1000&new_height=1000&w=1710472569&from=jpeg&type=9",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpALxY1qKHkMpsm-ZjH7GP5Bf0XdiL50jETQ&s",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThKYSfqIvcbcSWhiABSxJl0FCKoo1HSQuiNA&s",
    ],

    Honor: [
      "https://technave.com/data/files/article/202208250939384053.jpg",
      "https://technave.com/data/files/mall/article/202010060100122979.jpg",
      "https://technave.com/data/files/article/202506050946086303.jpg",
    ],

    HP: [
      "https://technave.com/data/files/article/202601270217115231.jpg",
      "https://technave.com/data/files/article/202511030522026781.jpg",
      "https://technave.com/data/files/article/202511030512427134.jpg",
    ],

    Huawei: [
      "https://technave.com/data/files/article/202107270210445397.jpg",
      "https://technave.com/data/files/mall/article/202009070747138301.jpg",
    ],
    iBall: [
      "https://static.toiimg.com/thumb/msid-52219876,imgsize-31686,width-400,resizemode-4/52219876.jpg",
    ],

    Infinix: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRk3tf-O8o3xhHS-tYZi3ZRZGENnQ_jLtpzJw&s",
      "https://technave.com/data/files/article/202405220716212373.png",
    ],

    Jio: [
      "https://technave.com/data/files/mall/article/202106080225107265.jpg",
      "https://technave.com/data/files/mall/article/202101120337025309.jpg",
    ],

    Lenovo: [
      "https://technave.com/data/files/article/202510090224406956.jpg",
      "https://technave.com/data/files/article/202505290713593385.jpg",
      "https://technave.com/data/files/article/202403290504101832.jpg",
    ],
    LG: [
      "https://5.imimg.com/data5/NI/YD/MY-64808542/lg-laptops-500x500.jpg",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkypSZh-mr_TLVQJ1OnhAduzvdKYywTkrsZQ&s",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvwX_Ao2diBGNgSi-yIR_LbL6LmPZsRtZIRQ&s",
    ],

    Microsoft: [
      "https://technave.com/data/files/mall/article/202010150855462934.jpg",
      "https://technave.com/data/files/mall/article/202011050642189223.jpg",
      "https://technave.com/data/files/article/202310190746484572.jpg",
    ],

    MSI: [
      "https://technave.com/data/files/article/202511110407541586.jpg",
      "https://technave.com/data/files/article/202509290737557721.jpg",
      "https://technave.com/data/files/article/202509290138229701.jpg",
    ],

    Ninkear: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKpdWtAt15lUAl1TAehORCn7z0wRCRaD7zJA&s",
    ],
    Primebook: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQL6124f_x4sdHCsn2DfgW5s2KcVHGjwbOx5w&s",
    ],

    Razer: [
      "https://exceldisc.com/_next/image?url=https%3A%2F%2Fapiv2.exceldisc.com%2Fmedia%2F121861%2Frazer-blade-15-advanced-edition-laptop-.jpeg&w=3840&q=75",
    ],

    Samsung: [
      "https://onxhuoxmggqudwfeedes.supabase.co/storage/v1/object/sign/laptop_pic/acer.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV85OWRmZGQzNS04YjQ3LTQ0YmEtOTkxYi0yZTg2ZThlYjZjYmMiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJsYXB0b3BfcGljL2FjZXIuanBnIiwiaWF0IjoxNzczMTQwMjQzLCJleHAiOjE4MDQ2NzYyNDN9.QV9DA4a0JcL7AW-f64Oew4RmJYL45bOQtCPxJb8GzLc",
      "https://img.global.news.samsung.com/my/wp-content/uploads/2019/01/Samsung-Notebook-Odyssey_main.jpg",
      "https://technave.com/data/files/article/202510270315107462.jpg",
    ],

    Tecno: [
      "https://technave.com/data/files/mall/article/202012051306288171.jpg",
      "https://example.com/apple2.jpg",
      "https://example.com/apple3.jpg",
    ],
    Ultimus: [
      "https://onxhuoxmggqudwfeedes.supabase.co/storage/v1/object/sign/laptop_pic/acer.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV85OWRmZGQzNS04YjQ3LTQ0YmEtOTkxYi0yZTg2ZThlYjZjYmMiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJsYXB0b3BfcGljL2FjZXIuanBnIiwiaWF0IjoxNzczMTQwMjQzLCJleHAiOjE4MDQ2NzYyNDN9.QV9DA4a0JcL7AW-f64Oew4RmJYL45bOQtCPxJb8GzLc",
      "https://technave.com/data/files/article/202601020152042327.jpg",
      "https://technave.com/data/files/article/202510270315107462.jpg",
    ],

    Walker: [
      "https://technave.com/data/files/mall/article/202012051306288171.jpg",
      "https://example.com/apple2.jpg",
      "https://example.com/apple3.jpg",
    ],
    Wings: [
      "https://onxhuoxmggqudwfeedes.supabase.co/storage/v1/object/sign/laptop_pic/acer.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV85OWRmZGQzNS04YjQ3LTQ0YmEtOTkxYi0yZTg2ZThlYjZjYmMiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJsYXB0b3BfcGljL2FjZXIuanBnIiwiaWF0IjoxNzczMTQwMjQzLCJleHAiOjE4MDQ2NzYyNDN9.QV9DA4a0JcL7AW-f64Oew4RmJYL45bOQtCPxJb8GzLc",
      "https://technave.com/data/files/article/202601020152042327.jpg",
      "https://technave.com/data/files/article/202510270315107462.jpg",
    ],

    Xiaomi: [
      "https://technave.com/data/files/article/small_202207060714402809.jpg",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZkwyhBMOs0iT9eOdP7khJdbxWjtZ3aVbHiQ&s",
      "https://www.giztop.com/media/catalog/product/cache/97cc1143d2e20f2b0c8ea91aaa12053c/x/i/xiaomi_mi_notebook_pro_15_2020_1.jpg",
    ],
    Zebronics: [
      "https://technave.com/data/files/mall/article/202012051306288171.jpg",
      "https://example.com/apple2.jpg",
      "https://example.com/apple3.jpg",
    ],
  };

  const brandImages = images[brand];

  if (!brandImages) return defaultImage;

  const index = id % brandImages.length;

  return brandImages[index];
}

async function fetchLaptops() {
  const { data } = await supabase.from("laptop").select("*");

  laptops.value = data;
  filteredLaptops.value = data;
}

function applyFilters() {
  filteredLaptops.value = laptops.value.filter((l) => {
    return (
      (!filters.value.brand || l.Brand === filters.value.brand) &&
      (!filters.value.gaming || l["Gaming?"] === filters.value.gaming) &&
      (!filters.value.cpuBrand || l["Cpu Brand"] === filters.value.cpuBrand) &&
      (!filters.value.cpuSeries ||
        l["Cpu Series"] === filters.value.cpuSeries) &&
      (!filters.value.os || l.OS === filters.value.os) &&
      (!filters.value.ram || l["RAM (filter)"] == filters.value.ram) &&
      (!filters.value.ssd || l["SSD (filter)"] == filters.value.ssd) &&
      (!filters.value.vram || l.VRAM == filters.value.vram) &&
      (!filters.value.gpu || l["Dedicated Gpu"] === filters.value.gpu) &&
      (!filters.value.priceMin || l["Price (RM)"] >= filters.value.priceMin) &&
      (!filters.value.priceMax || l["Price (RM)"] <= filters.value.priceMax) &&
      (!filters.value.displayInches ||
        parseFloat(l["Display (Inches)"]) ===
          parseFloat(filters.value.displayInches)) &&
      (!filters.value.pixel ||
        (l.Pixel &&
          l.Pixel.replace(/\s/g, "") ===
            filters.value.pixel.replace(/\s/g, ""))) &&
      (!filters.value.touch || l["Touch Screen?"] === filters.value.touch)
    );
  });
}

function toggleCompare(laptop) {
  const exist = selected.value.find((l) => l.id === laptop.id);

  if (exist) {
    selected.value = selected.value.filter((l) => l.id !== laptop.id);
  } else {
    if (selected.value.length >= 4) {
      alert("You can compare max 4 laptops");
      return;
    }

    selected.value.push(laptop);
  }
  // save selection
  localStorage.setItem("compareLaptops", JSON.stringify(selected.value));
}

function goCompare() {
  if (selected.value.length < 2) {
    alert("Select at least 2 laptops");
    return;
  }

  // save to localStorage
  localStorage.setItem("compareLaptops", JSON.stringify(selected.value));

  router.push("/compare-result");
}

function clearCompare() {
  selected.value = [];
  localStorage.removeItem("compareLaptops");
}

onMounted(() => {
  fetchLaptops();

  const saved = localStorage.getItem("compareLaptops");
  if (saved && saved !== "[]") {
    selected.value = JSON.parse(saved);
  }
});
</script>

<template>
  <Navbar>
    <div class="w-full p-6 md:p-10 bg-blue-200">
      <h1 class="text-3xl font-bold mb-6">Laptop Filter & Comparison</h1>

      <!-- FILTERS -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        <select v-model="filters.brand" class="border p-2 rounded">
          <option value="">Brand</option>
          <option>Acer</option>
          <option>Apple</option>
          <option>Asus</option>
          <option>Avita</option>
          <option>AXL</option>
          <option>Chuwi</option>
          <option>Colorful</option>
          <option>Dell</option>
          <option>Fujitsu</option>
          <option>Gigabyte</option>
          <option>Honor</option>
          <option>HP</option>
          <option>Huawei</option>
          <option>iBall</option>
          <option>Infinix</option>
          <option>Jio</option>
          <option>Lenovo</option>
          <option>LG</option>
          <option>Microsoft</option>
          <option>MSI</option>
          <option>Ninkear</option>
          <option>Primebook</option>
          <option>Razer</option>
          <option>Samsung</option>
          <option>Tecno</option>
          <option>Ultimus</option>
          <option>Walker</option>
          <option>Wings</option>
          <option>Xiaomi</option>
          <option>Zebronics</option>
        </select>

        <select v-model="filters.gaming" class="border p-2 rounded">
          <option value="">All</option>
          <option value="Yes">Gaming Laptop</option>
          <option value="No">Non Gaming Laptop</option>
        </select>

        <select v-model="filters.cpuBrand" class="border p-2 rounded">
          <option value="">CPU Brand</option>
          <option>Intel</option>
          <option>AMD</option>
          <option>Apple</option>
        </select>

        <select v-model="filters.ram" class="border p-2 rounded">
          <option value="">RAM</option>
          <option value="4">4GB</option>
          <option value="8">8GB</option>
          <option value="12">12GB</option>
          <option value="16">16GB</option>
          <option value="32">32GB</option>
          <option value="64">64GB</option>
        </select>

        <select v-model="filters.ssd" class="border p-2 rounded">
          <option value="">All</option>
          <option value="64 GB SSD">64 GB SSD</option>
          <option value="128 GB SSD">128 GB SSD</option>
          <option value="256 GB SSD">256 GB SSD</option>
          <option value="512 GB SSD">512 GB SSD</option>
          <option value="1 TB SSD">1 TB SSD</option>
          <option value="2 TB SSD">2 TB SSD</option>
          <option value="4 TB SSD">4 TB SSD</option>
          <option value="32 GB HDD">32 GB HDD</option>
          <option value="64 GB HDD">64 GB HDD</option>
          <option value="1 TB HDD">1 TB HDD</option>
        </select>

        <select v-model="filters.displayInches" class="border p-2 rounded">
          <option value="">Display (Inches)</option>
          <option value="11.6">11.6</option>
          <option value="12">12</option>
          <option value="12.4">12.4</option>
          <option value="12.6">12.6</option>
          <option value="13.3">13.3</option>
          <option value="13.4">13.4</option>
          <option value="13.5">13.5</option>
          <option value="13.6">13.6</option>
          <option value="14">14</option>
          <option value="14.1">14.1</option>
          <option value="14.2">14.2</option>
          <option value="14.5">14.5</option>
          <option value="15">15</option>
          <option value="15.3">15.3</option>
          <option value="15.6">15.6</option>
          <option value="15.75">15.75</option>
          <option value="16">16</option>
          <option value="16.1">16.1</option>
          <option value="16.2">16.2</option>
          <option value="17">17</option>
          <option value="17.3">17.3</option>
          <option value="18">18</option>
        </select>

        <select v-model="filters.pixel" class="border p-2 rounded">
          <option value="">Pixel</option>
          <option>1080 x 1920</option>
          <option>1200 x 1920</option>
          <option>1280 x 1024</option>
          <option>1366 x 720</option>
          <option>1366 x 768</option>
          <option>1440 x 2560</option>
          <option>1536 x 1024</option>
          <option>1600 x 2560</option>
          <option>1920 x 1080</option>
          <option>1920 x 1200</option>
          <option>1920 x 1280</option>
          <option>1920 x 2560</option>
          <option>2048 x 1536</option>
          <option>2160 x 1440</option>
          <option>2240 x 1400</option>
          <option>2256 x 1504</option>
          <option>2520 x 1680</option>
          <option>2560 x 1440</option>
          <option>2560 x 1600</option>
          <option>2560 x 1664</option>
          <option>2561 x 1600</option>
          <option>2880 x 1620</option>
          <option>2880 x 1800</option>
          <option>2880 x 1864</option>
          <option>3000 x 2000</option>
          <option>3024 x 1964</option>
          <option>3072 x 1920</option>
          <option>3200 x 1800</option>
          <option>3200 x 2000</option>
          <option>3456 x 2160</option>
          <option>3456 x 2234</option>
          <option>3840 x 2160</option>
          <option>3840 x 2400</option>
        </select>

        <select v-model="filters.touch" class="border p-2 rounded">
          <option value="">Touch Screen?</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>

        <select v-model="filters.vram" class="border p-2 rounded">
          <option value="">VRAM</option>
          <option value="2">2GB GPU</option>
          <option value="4">4GB GPU</option>
          <option value="6">6GB GPU</option>
          <option value="8">8GB GPU</option>
          <option value="12">12GB GPU</option>
          <option value="16">16GB GPU</option>
        </select>
        <input
          type="number"
          placeholder="Min Price"
          v-model="filters.priceMin"
          class="border p-2 rounded"
        />
        <input
          type="number"
          placeholder="Max Price"
          v-model="filters.priceMax"
          class="border p-2 rounded"
        />

        <button
          @click="applyFilters"
          class="bg-blue-500 text-white p-2 rounded col-span-1 sm:col-span-2 md:col-span-1"
        >
          Apply
        </button>
      </div>

      <!-- LAPTOP CARDS -->
      <div class="flex flex-wrap gap-2 justify-center">
        <div
          v-for="laptop in filteredLaptops"
          :key="laptop.id"
          class="bg-white border rounded-xl shadow hover:shadow-xl p-4 w-72 flex flex-col justify-between"
        >
          <!-- Laptop Image -->
          <img
            :src="getBrandImage(laptop.Brand, laptop.id)"
            class="w-full h-40 object-contain mb-3"
          />
          <div>
            <h2 class="font-bold text-lg mb-2">{{ laptop.Model }}</h2>
            <p class="text-gray-600 text-sm">
              Generation: {{ laptop.Generation }}
            </p>
            <p class="text-gray-600 text-sm">CPU: {{ laptop["Cpu Series"] }}</p>
            <p class="text-gray-600 text-sm">Core: {{ laptop.Core }}</p>

            <p class="text-gray-600 text-sm">RAM: {{ laptop.Ram }}</p>
            <p class="text-gray-600 text-sm">SSD: {{ laptop.SSD }}</p>

            <p class="text-gray-600 text-sm">Display: {{ laptop.Display }}</p>
            <p
              v-if="laptop['Dedicated Gpu'] === 'Yes'"
              class="text-gray-600 mb-1"
            >
              GPU: {{ laptop.Graphics }}
            </p>
          </div>
          <div class="mt-3 flex justify-between items-center">
            <span class="text-green-600 font-bold"
              >RM {{ laptop["Price (RM)"] }}</span
            >
            <button
              @click="toggleCompare(laptop)"
              class="text-blue-500 font-semibold hover:underline"
            >
              {{
                selected.find((l) => l.id === laptop.id)
                  ? "Remove"
                  : "Add to Compare"
              }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- FLOATING COMPARE BAR -->
    <div
      v-if="selected.length > 0"
      class="fixed bottom-0 left-0 right-0 bg-white shadow-lg p-4 flex flex-col md:flex-row justify-between items-center md:items-stretch gap-3 md:gap-0"
    >
      <div
        class="flex flex-wrap gap-2 md:gap-3 justify-center md:justify-start"
      >
        <span
          v-for="l in selected"
          :key="l.id"
          class="bg-gray-200 rounded px-3 py-1 text-sm font-medium"
        >
          {{ l.Brand }}
        </span>
      </div>

      <button
        @click="goCompare"
        class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
      >
        Compare ({{ selected.length }})
      </button>
      <button
        @click="clearCompare"
        class="bg-red-500 text-white px-4 py-2 rounded"
      >
        Clear
      </button>
    </div>
  </Navbar>
</template>
