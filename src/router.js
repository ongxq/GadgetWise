// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { supabase } from "./supabase";

// Pages
import LoginPage from "./pages/LoginPage.vue";
import SignupPage from "./pages/SignUpPage.vue";
//import DashboardPage from "./pages/DashboardPage.vue";
//import AdminDashboard from "./pages/AdminDashboard.vue";
import AIRecommendation from "./pages/AIRecommendation.vue";
import Visualization from "./pages/Visualization.vue";
import Chatbot from "./pages/Chatbot.vue";
import Ordering from "./pages/Ordering.vue";
import AdminOrder from "./pages/AdminOrder.vue";
import Comparison from "./pages/Comparison.vue";
import CompareResult from "./pages/CompareResult.vue";

const routes = [
  // ---------------- PUBLIC ----------------
  { path: "/", name: "Login", component: LoginPage },
  { path: "/signup", component: SignupPage },

  // ---------------- USER ROUTES ----------------
  // {
  //   path: "/dashboard",
  //   component: DashboardPage,
  //   meta: { requiresAuth: true },
  // },
  {
    path: "/ai-recommendation",
    component: AIRecommendation,
    meta: { requiresAuth: true },
  },
  {
    path: "/visualization",
    component: Visualization,
    meta: { requiresAuth: true },
  },
  { path: "/comparison", component: Comparison, meta: { requiresAuth: true } },
  {
    path: "/compare-result",
    component: CompareResult,
    meta: { requiresAuth: true },
  },
  { path: "/chatbot", component: Chatbot, meta: { requiresAuth: true } },
  { path: "/ordering", component: Ordering, meta: { requiresAuth: true } },

  // ---------------- ADMIN ROUTES ----------------
  // {
  //   path: "/admin-dashboard",
  //   component: AdminDashboard,
  //   meta: { requiresAuth: true, requiresAdmin: true },
  // },
  {
    path: "/admin-ai-recommendation",
    component: AIRecommendation,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin-visualization",
    component: Visualization,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin-comparison",
    component: Comparison,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin-chatbot",
    component: Chatbot,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin-ordering",
    component: AdminOrder,
    meta: { requiresAuth: true, requiresAdmin: true },
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

  next();
});

export default router;
