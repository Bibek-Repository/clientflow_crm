
<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <h2>ClientFlow</h2>
      <span>CRM PLATFORM</span>
    </div>

    <nav class="sidebar-navigation">
      <p class="nav-heading">MAIN MENU</p>

      <RouterLink to="/" class="nav-link">
        <span>Dashboard</span>
      </RouterLink>

      <RouterLink to="/customers" class="nav-link">
        <span>Customers</span>
      </RouterLink>
    </nav>

    <div class="sidebar-footer">
      <p>ClientFlow CRM</p>
      <small>Version 1.0.0</small>
    </div>
  </aside>
</template>
