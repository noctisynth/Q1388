import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/home.vue";
import ProfileView from "@/views/profile.vue";
import CartView from "@/views/cart.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/cart",
      name: "cart",
      component: CartView,
    },
  ],
});

export default router;
