
<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import StatCard from "../components/StatCard.vue";

// Dashboard statistics
const totalCustomers = ref(0);
const totalLeads = ref(0);
const qualifiedLeads = ref(0);
const wonLeads = ref(0);

// Loading and error states
const loading = ref(true);
const error = ref("");

// Fetch dashboard statistics from FastAPI
async function fetchDashboardData() {
  loading.value = true;
  error.value = "";

  try {
    const response = await api.get("/dashboard/stats");

    totalCustomers.value = response.data.total_customers;
    totalLeads.value = response.data.total_leads;
    qualifiedLeads.value = response.data.qualified_leads;
    wonLeads.value = response.data.won_leads;

  } catch (err) {
    error.value = "Unable to load dashboard statistics.";
    console.error(err);

  } finally {
    loading.value = false;
  }
}

// Load statistics when dashboard opens
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

    <p v-if="error" class="error-message">
      {{ error }}
    </p>

    <div class="stats-grid">

      <StatCard
        title="Total Customers"
        :value="loading ? '...' : totalCustomers"
        description="Customers registered in your CRM"
        icon="👥"
      />

      <StatCard
        title="Total Leads"
        :value="loading ? '...' : totalLeads"
        description="Potential customers in your CRM"
        icon="🎯"
      />

      <StatCard
        title="Qualified Leads"
        :value="loading ? '...' : qualifiedLeads"
        description="Leads ready for sales"
        icon="⭐"
      />

      <StatCard
        title="Won Leads"
        :value="loading ? '...' : wonLeads"
        description="Successfully converted leads"
        icon="🏆"
      />

    </div>

  </section>
</template>
