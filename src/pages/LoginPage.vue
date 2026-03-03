<script setup>
import { ref } from "vue";
import { supabase } from "../supabase";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const password = ref("");
const message = ref("");
const showPassword = ref(false);

const login = async () => {
  message.value = "";

  const { data, error } = await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value,
  });

  if (error) {
    message.value = error.message;
    return;
  }

  const { data: profile, error: profileError } = await supabase
    .from("profiles")
    .select("role")
    .eq("id", data.user.id)
    .single();

  if (profileError) {
    message.value = profileError.message;
    return;
  }

  if (profile.role === "admin") {
    router.push("/admin-dashboard/ordering");
  } else {
    router.push("/dashboard/ai-recommendation");
  }
};
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-tr from-teal-400 to-blue-500 px-4"
  >
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
      <!-- Logo -->
      <div class="flex justify-center mb-1">
        <img src="../assets/logo.png" class="h-36 w-36 object-contain" />
      </div>
      <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Login</h2>

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full px-4 py-3 mb-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-400"
      />

      <div class="relative mb-4">
        <input
          :type="showPassword ? 'text' : 'password'"
          v-model="password"
          placeholder="Password"
          class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
        <button
          type="button"
          @click="showPassword = !showPassword"
          class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-600 font-semibold hover:text-teal-500"
        >
          {{ showPassword ? "Hide" : "Show" }}
        </button>
      </div>

      <button
        @click="login"
        class="w-full bg-teal-400 hover:bg-teal-500 text-white py-3 rounded-lg font-semibold transition-colors"
      >
        Login
      </button>

      <p class="text-red-500 text-sm mt-3 text-center">{{ message }}</p>

      <p class="text-gray-600 text-sm mt-6 text-center">
        Don't have an account?
        <button
          @click="router.push('/signup')"
          class="text-teal-500 font-semibold hover:underline ml-1"
        >
          Sign Up
        </button>
      </p>
    </div>
  </div>
</template>
