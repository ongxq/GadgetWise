<script setup>
import { ref, onMounted } from "vue";
import { UserCircleIcon } from "@heroicons/vue/24/outline";
import { supabase } from "../supabase";
import { useRouter } from "vue-router";

const router = useRouter();
const isOpen = ref(true); // Sidebar open
const dropdownOpen = ref(false); // Profile dropdown
const user = ref({ username: "", email: "" });

// Toggle sidebar
const toggleSidebar = () => {
  isOpen.value = !isOpen.value;
};

// Toggle profile dropdown
const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

// Logout
const logout = async () => {
  await supabase.auth.signOut();
  router.push("/");
};

// Fetch user profile (Supabase v2)
onMounted(async () => {
  const {
    data: { user: currentUser },
    error: authError,
  } = await supabase.auth.getUser();
  if (authError) {
    console.error(authError.message);
    return;
  }
  if (currentUser) {
    const { data, error } = await supabase
      .from("profiles")
      .select("username,email")
      .eq("id", currentUser.id)
      .single();
    if (error) {
      console.error(error.message);
      return;
    }
    if (data) user.value = data;
  }
});
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <!-- ================= TOP NAVBAR ================= -->
    <header
      class="fixed top-0 left-0 right-0 h-16 bg-white shadow flex items-center justify-between px-6 z-50"
    >
      <!-- Logo + Title (CLICK TO TOGGLE SIDEBAR) -->
      <div
        class="flex items-center space-x-3 cursor-pointer"
        @click="toggleSidebar"
      >
        <img src="../assets/image_1.jpg" class="h-8 w-8" />
        <span class="text-xl font-bold text-indigo-600">GadgetWise</span>
      </div>

      <!-- Profile Icon + Dropdown -->
      <div class="relative">
        <UserCircleIcon
          @click="toggleDropdown"
          class="h-8 w-8 text-gray-600 cursor-pointer hover:text-indigo-600 transition"
        />
        <!-- Dropdown Box -->
        <div
          v-if="dropdownOpen"
          class="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded shadow-lg z-50"
        >
          <div class="px-4 py-3 border-b">
            <p class="font-semibold text-gray-700 truncate">
              {{ user.username }}
            </p>
            <p class="text-sm text-gray-500 truncate">{{ user.email }}</p>
          </div>
          <button
            @click="logout"
            class="w-full text-left px-4 py-2 hover:bg-gray-100 text-gray-700 font-medium"
          >
            Log Out
          </button>
        </div>
      </div>
    </header>

    <!-- ================= SIDEBAR ================= -->
    <aside
      :class="[
        'fixed top-16 left-0 h-[calc(100%-4rem)] bg-white shadow-lg transition-all duration-300',
        isOpen ? 'w-60' : 'w-20',
      ]"
    >
      <nav class="flex flex-col mt-6 space-y-2">
        <router-link
          to="/dashboard/ai-recommendation"
          class="flex items-center px-4 py-3 hover:bg-gray-100 transition"
        >
          <span class="text-xl">🏠</span>
          <span v-if="isOpen" class="ml-4">AI Recommendation</span>
        </router-link>

        <router-link
          to="/dashboard/visualization"
          class="flex items-center px-4 py-3 hover:bg-gray-100 transition"
        >
          <span class="text-xl">📊</span>
          <span v-if="isOpen" class="ml-4">Visualization</span>
        </router-link>

        <router-link
          to="/dashboard/chatbot"
          class="flex items-center px-4 py-3 hover:bg-gray-100 transition"
        >
          <span class="text-xl">💬</span>
          <span v-if="isOpen" class="ml-4">Chatbot</span>
        </router-link>

        <router-link
          to="/dashboard/ordering"
          class="flex items-center px-4 py-3 hover:bg-gray-100 transition"
        >
          <span class="text-xl">🛒</span>
          <span v-if="isOpen" class="ml-4">Ordering</span>
        </router-link>
      </nav>
    </aside>

    <!-- ================= MAIN CONTENT ================= -->
    <main
      class="pt-16 p-8 transition-all duration-300"
      :class="isOpen ? 'ml-64' : 'ml-20'"
    >
      <router-view />
    </main>
  </div>
</template>
