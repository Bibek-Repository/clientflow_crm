
<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  description: {
    type: String,
    default: "",
  },
  icon: {
    type: String,
    default: "chart",
  },
});
</script>

<template>
  <div class="stat-card">
    <div class="stat-card-header">
      <span class="stat-title">{{ title }}</span>
      <span class="stat-icon">{{ icon }}</span>
    </div>

    <h2 class="stat-value">{{ value }}</h2>

    <p class="stat-description">{{ description }}</p>
  </div>
</template>
