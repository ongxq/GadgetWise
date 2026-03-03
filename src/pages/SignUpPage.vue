<script setup>
import { ref } from "vue";
import { supabase } from "../supabase";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref(""); // new username field
const email = ref("");
const password = ref("");
const message = ref("");
const showPassword = ref(false);

const signup = async () => {
  message.value = "";

  // Basic validation
  if (!username.value || !email.value || !password.value) {
    message.value = "Please fill in all fields.";
    return;
  }

  const { data, error } = await supabase.auth.signUp({
    email: email.value,
    password: password.value,
  });

  if (error) {
    message.value = error.message;
    return;
  }

  if (data?.user) {
    const { error: profileError } = await supabase.from("profiles").insert([
      {
        id: data.user.id,
        username: username.value, // insert username
        email: email.value,
        role: "user",
      },
    ]);

    if (profileError) {
      message.value = profileError.message;
      return;
    }
  }

  message.value = "Account created! Check your email to confirm.";
};
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-tr from-purple-400 to-pink-500 px-4"
  >
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
      <div class="flex justify-center mb-1">
        <img src="../assets/logo.png" class="h-36 w-36 object-contain" />
      </div>
      <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Sign Up</h2>

      <!-- Username Input -->
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        class="w-full px-4 py-3 mb-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
      />

      <!-- Email Input -->
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full px-4 py-3 mb-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
      />

      <!-- Password Input -->
      <div class="relative mb-4">
        <input
          :type="showPassword ? 'text' : 'password'"
          v-model="password"
          placeholder="Password"
          class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
        />
        <button
          type="button"
          @click="showPassword = !showPassword"
          class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-600 font-semibold hover:text-purple-500"
        >
          {{ showPassword ? "Hide" : "Show" }}
        </button>
      </div>

      <!-- Sign Up Button -->
      <button
        @click="signup"
        class="w-full bg-purple-400 hover:bg-purple-500 text-white py-3 rounded-lg font-semibold transition-colors"
      >
        Sign Up
      </button>

      <!-- Message -->
      <p class="text-red-500 text-sm mt-3 text-center">{{ message }}</p>

      <!-- Go to Login -->
      <p class="text-gray-600 text-sm mt-6 text-center">
        Already have an account?
        <button
          @click="router.push('/')"
          class="text-purple-500 font-semibold hover:underline ml-1"
        >
          Go to Login
        </button>
      </p>
    </div>
  </div>
</template>
