// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { supabase } from "./supabase";

// Pages
import LoginPage from "./pages/LoginPage.vue";
import SignupPage from "./pages/SignUpPage.vue";
import DashboardPage from "./pages/DashboardPage.vue";
import AdminDashboard from "./pages/AdminDashboard.vue";
import AIRecommendation from "./pages/AIRecommendation.vue";
import Visualization from "./pages/Visualization.vue";
import Chatbot from "./pages/Chatbot.vue";
import Ordering from "./pages/Ordering.vue";
import AdminOrder from "./pages/AdminOrder.vue";

const routes = [
  { path: "/", name: "Login", component: LoginPage },
  { path: "/signup", component: SignupPage },

  // ---------------- USER DASHBOARD (Nested) ----------------
  {
    path: "/dashboard",
    component: DashboardPage,
    meta: { requiresAuth: true },
    children: [
      { path: "ai-recommendation", component: AIRecommendation },
      { path: "visualization", component: Visualization },
      { path: "chatbot", component: Chatbot },
      { path: "ordering", component: Ordering },
    ],
  },

  // ---------------- ADMIN ----------------
  {
    path: "/admin-dashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: "visualization", component: Visualization }, // same component as user
      { path: "ai-recommendation", component: AIRecommendation }, // same component
      { path: "chatbot", component: Chatbot }, // same component as user
      {
        path: "ordering",
        component: AdminOrder,
        meta: { requiresAdmin: true },
      }, // optional admin version
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ------------------------
// Global Navigation Guard
// ------------------------
router.beforeEach(async (to, from, next) => {
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (to.meta.requiresAuth && !user) return next("/");

  let profile = null;
  if (user) {
    const { data } = await supabase
      .from("profiles")
      .select("role")
      .eq("id", user.id)
      .single();
    profile = data;
  }

  // Admin routes
  if (to.meta.requiresAdmin && profile?.role !== "admin")
    return next("/dashboard");

  // User-only routes
  if (to.meta.requiresUser && profile?.role === "admin")
    return next("/admin-dashboard");

  next();
});

export default router;
