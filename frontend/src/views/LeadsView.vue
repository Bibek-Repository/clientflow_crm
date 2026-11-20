
<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";

// Lead data
const leads = ref([]);
const loading = ref(false);
const saving = ref(false);

// Search
const searchQuery = ref("");

// Form visibility
const showForm = ref(false);
const editingLeadId = ref(null);

// Messages
const success = ref("");
const error = ref("");

// Available lead statuses
const leadStatuses = [
  "New",
  "Contacted",
  "Qualified",
  "Proposal",
  "Won",
  "Lost",
];

// Empty lead form
const emptyForm = () => ({
  name: "",
  email: "",
  phone: "",
  company: "",
  source: "",
  status: "New",
});

const form = ref(emptyForm());

// Filter leads
const filteredLeads = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();

  if (!query) {
    return leads.value;
  }

  return leads.value.filter((lead) => {
    return (
      lead.name.toLowerCase().includes(query) ||
      lead.email.toLowerCase().includes(query) ||
      lead.company.toLowerCase().includes(query) ||
      lead.source.toLowerCase().includes(query) ||
      lead.status.toLowerCase().includes(query)
    );
  });
});

// Retrieve leads from FastAPI
async function fetchLeads() {
  loading.value = true;
  error.value = "";

  try {
    const response = await api.get("/leads");
    leads.value = response.data;
  } catch (err) {
    error.value = "Unable to retrieve leads. Check your backend connection.";
    console.error(err);
  } finally {
    loading.value = false;
  }
}

// Open create form
function openCreateForm() {
  editingLeadId.value = null;
  form.value = emptyForm();
  showForm.value = true;
  success.value = "";
  error.value = "";
}

// Open edit form
function openEditForm(lead) {
  editingLeadId.value = lead.id;

  form.value = {
    name: lead.name,
    email: lead.email,
    phone: lead.phone,
    company: lead.company,
    source: lead.source,
    status: lead.status,
  };

  showForm.value = true;
  success.value = "";
  error.value = "";
}

// Close form
function closeForm() {
  showForm.value = false;
  editingLeadId.value = null;
  form.value = emptyForm();
}

// Create or update lead
async function saveLead() {
  saving.value = true;
  error.value = "";
  success.value = "";

  try {
    if (editingLeadId.value === null) {
      await api.post("/leads", form.value);
      success.value = "Lead created successfully!";
    } else {
      await api.put(
        `/leads/${editingLeadId.value}`,
        form.value
      );

      success.value = "Lead updated successfully!";
    }

    closeForm();
    await fetchLeads();
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Unable to save lead.";

    console.error(err);
  } finally {
    saving.value = false;
  }
}

// Delete lead
async function deleteLead(leadId) {
  const confirmed = window.confirm(
    "Are you sure you want to delete this lead?"
  );

  if (!confirmed) return;

  error.value = "";
  success.value = "";

  try {
    await api.delete(`/leads/${leadId}`);

    success.value = "Lead deleted successfully!";

    await fetchLeads();
  } catch (err) {
    error.value = "Unable to delete lead.";
    console.error(err);
  }
}

// Load leads when page opens
onMounted(() => {
  fetchLeads();
});
</script>

<template>
  <section class="customers-page">

    <!-- Page heading -->
    <div class="customers-heading">
      <div>
        <h2>Leads</h2>
        <p>Track, manage and organize your potential customers.</p>
      </div>

      <button class="primary-button" @click="openCreateForm">
        + Add Lead
      </button>
    </div>

    <!-- Success and error messages -->
    <p v-if="success" class="success-message">
      {{ success }}
    </p>

    <p v-if="error" class="error-message">
      {{ error }}
    </p>

    <!-- Lead form -->
    <div v-if="showForm" class="customer-form-panel">

      <div class="form-heading">
        <h3>
          {{ editingLeadId === null ? "Add New Lead" : "Edit Lead" }}
        </h3>

        <button class="close-button" @click="closeForm">
          ×
        </button>
      </div>

      <form @submit.prevent="saveLead" class="customer-form">

        <div class="form-group">
          <label for="lead-name">Lead Name</label>
          <input
            id="lead-name"
            v-model="form.name"
            type="text"
            placeholder="Enter lead name"
            minlength="2"
            maxlength="100"
            required
          />
        </div>

        <div class="form-group">
          <label for="lead-email">Email Address</label>
          <input
            id="lead-email"
            v-model="form.email"
            type="email"
            placeholder="Enter email address"
            maxlength="255"
            required
          />
        </div>

        <div class="form-group">
          <label for="lead-phone">Phone Number</label>
          <input
            id="lead-phone"
            v-model="form.phone"
            type="text"
            placeholder="Enter phone number"
            minlength="5"
            maxlength="30"
            required
          />
        </div>

        <div class="form-group">
          <label for="lead-company">Company</label>
          <input
            id="lead-company"
            v-model="form.company"
            type="text"
            placeholder="Enter company name"
            minlength="2"
            maxlength="150"
            required
          />
        </div>

        <div class="form-group">
          <label for="lead-source">Lead Source</label>
          <select
            id="lead-source"
            v-model="form.source"
            required
          >
            <option value="" disabled>Select source</option>
            <option value="Website">Website</option>
            <option value="Referral">Referral</option>
            <option value="Social Media">Social Media</option>
            <option value="Advertisement">Advertisement</option>
            <option value="Email Campaign">Email Campaign</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="form-group">
          <label for="lead-status">Lead Status</label>
          <select
            id="lead-status"
            v-model="form.status"
            required
          >
            <option
              v-for="item in leadStatuses"
              :key="item"
              :value="item"
            >
              {{ item }}
            </option>
          </select>
        </div>

        <div class="form-actions">

          <button
            type="button"
            class="secondary-button"
            @click="closeForm"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="primary-button"
            :disabled="saving"
          >
            {{
              saving
                ? "Saving..."
                : editingLeadId === null
                  ? "Create Lead"
                  : "Save Changes"
            }}
          </button>

        </div>

      </form>
    </div>

    <!-- Lead table -->
    <div class="customer-table-panel">

      <div class="table-toolbar">
        <div>
          <h3>Lead Directory</h3>
          <p>{{ filteredLeads.length }} leads displayed</p>
        </div>

        <input
          v-model="searchQuery"
          type="search"
          class="search-input"
          placeholder="Search leads..."
        />
      </div>

      <div v-if="loading" class="table-message">
        Loading leads...
      </div>

      <div
        v-else-if="filteredLeads.length === 0"
        class="table-message"
      >
        {{
          leads.length === 0
            ? "No leads found. Add your first lead."
            : "No leads match your search."
        }}
      </div>

      <div v-else class="table-responsive">

        <table class="customer-table">

          <thead>
            <tr>
              <th>ID</th>
              <th>Lead</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Company</th>
              <th>Source</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="lead in filteredLeads"
              :key="lead.id"
            >
              <td>#{{ lead.id }}</td>

              <td class="customer-name-cell">
                {{ lead.name }}
              </td>

              <td>{{ lead.email }}</td>
              <td>{{ lead.phone }}</td>
              <td>{{ lead.company }}</td>
              <td>{{ lead.source }}</td>
              <td>{{ lead.status }}</td>

              <td>
                <div class="table-actions">

                  <button
                    class="edit-button"
                    @click="openEditForm(lead)"
                  >
                    Edit
                  </button>

                  <button
                    class="delete-button"
                    @click="deleteLead(lead.id)"
                  >
                    Delete
                  </button>

                </div>
              </td>
            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </section>
</template>
