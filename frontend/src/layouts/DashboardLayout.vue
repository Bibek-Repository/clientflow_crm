
<script setup>
import { useRoute } from "vue-router";
import Sidebar from "../components/Sidebar.vue";
import Topbar from "../components/Topbar.vue";

const route = useRoute();
</script>

<template>
  <div class="dashboard-layout">
    <Sidebar />

    <div class="main-area">
      <Topbar :pageTitle="route.meta.title || 'Dashboard'" />

      <main class="page-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
