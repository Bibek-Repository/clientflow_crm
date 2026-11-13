
import { createRouter, createWebHistory } from "vue-router";

import DashboardLayout from "../layouts/DashboardLayout.vue";
import DashboardView from "../views/DashboardView.vue";
import CustomersView from "../views/CustomersView.vue";

const routes = [
  {
    path: "/",
    component: DashboardLayout,
    children: [
      {
        path: "",
        name: "Dashboard",
        component: DashboardView,
        meta: {
          title: "Dashboard",
        },
      },
      {
        path: "customers",
        name: "Customers",
        component: CustomersView,
        meta: {
          title: "Customers",
        },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
