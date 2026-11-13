
<script setup>
defineProps({
  pageTitle: {
    type: String,
    default: "Dashboard",
  },
});
</script>

<template>
  <header class="topbar">
    <div class="topbar-heading">
      <h1>{{ pageTitle }}</h1>
      <p>Welcome back! Here's what's happening with your CRM.</p>
    </div>

    <div class="topbar-user">
      <div class="user-avatar">B</div>

      <div class="user-details">
        <strong>Admin User</strong>
        <span>Administrator</span>
      </div>
    </div>
  </header>
</template>
