
<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import StatCard from "../components/StatCard.vue";

const totalCustomers = ref(0);
const loading = ref(true);
const error = ref("");

async function fetchDashboardData() {
  try {
    const response = await api.get("/customers");
    totalCustomers.value = response.data.length;
  } catch (err) {
    error.value = "Unable to load dashboard statistics.";
    console.error(err);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchDashboardData();
});
</script>

<template>
  <section class="dashboard-page">
    <div class="welcome-section">
      <h2>Welcome to ClientFlow CRM</h2>
      <p>Here's an overview of your customer management system.</p>
    </div>

    <p v-if="error" class="error-message">{{ error }}</p>

    <div class="stats-grid">
      <StatCard
        title="Total Customers"
        :value="loading ? '...' : totalCustomers"
        description="Customers registered in your CRM"
        icon="👥"
      />

      <StatCard
        title="Active Leads"
        value="Coming soon"
        description="Lead management will be added next"
        icon="🎯"
      />

      <StatCard
        title="Sales Pipeline"
        value="Coming soon"
        description="Track your sales opportunities"
        icon="📊"
      />
    </div>
  </section>
</template>
