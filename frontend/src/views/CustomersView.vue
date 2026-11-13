
<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";

// Customer data
const customers = ref([]);
const loading = ref(false);
const saving = ref(false);

// Search
const searchQuery = ref("");

// Form visibility
const showForm = ref(false);
const editingCustomerId = ref(null);

// Messages
const success = ref("");
const error = ref("");

// Customer form
const emptyForm = () => ({
  name: "",
  email: "",
  phone: "",
  company: "",
});

const form = ref(emptyForm());

// Filter customers based on search input
const filteredCustomers = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();

  if (!query) {
    return customers.value;
  }

  return customers.value.filter((customer) => {
    return (
      customer.name.toLowerCase().includes(query) ||
      customer.email.toLowerCase().includes(query) ||
      customer.company.toLowerCase().includes(query)
    );
  });
});

// Retrieve customers from FastAPI
async function fetchCustomers() {
  loading.value = true;
  error.value = "";

  try {
    const response = await api.get("/customers");
    customers.value = response.data;
  } catch (err) {
    error.value = "Unable to retrieve customers. Check your backend connection.";
    console.error(err);
  } finally {
    loading.value = false;
  }
}

// Open the form for creating a customer
function openCreateForm() {
  editingCustomerId.value = null;
  form.value = emptyForm();
  showForm.value = true;
  success.value = "";
  error.value = "";
}

// Open the form with existing customer details
function openEditForm(customer) {
  editingCustomerId.value = customer.id;

  form.value = {
    name: customer.name,
    email: customer.email,
    phone: customer.phone,
    company: customer.company,
  };

  showForm.value = true;
  success.value = "";
  error.value = "";
}

// Close and reset the form
function closeForm() {
  showForm.value = false;
  editingCustomerId.value = null;
  form.value = emptyForm();
}

// Create or update a customer
async function saveCustomer() {
  saving.value = true;
  error.value = "";
  success.value = "";

  try {
    if (editingCustomerId.value === null) {
      await api.post("/customers", form.value);
      success.value = "Customer created successfully!";
    } else {
      await api.put(
        `/customers/${editingCustomerId.value}`,
        form.value
      );
      success.value = "Customer updated successfully!";
    }

    closeForm();
    await fetchCustomers();
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Unable to save customer.";

    console.error(err);
  } finally {
    saving.value = false;
  }
}

// Delete a customer
async function deleteCustomer(customerId) {
  const confirmed = window.confirm(
    "Are you sure you want to delete this customer?"
  );

  if (!confirmed) return;

  error.value = "";
  success.value = "";

  try {
    await api.delete(`/customers/${customerId}`);

    success.value = "Customer deleted successfully!";

    await fetchCustomers();
  } catch (err) {
    error.value = "Unable to delete customer.";
    console.error(err);
  }
}

// Load customers when the page opens
onMounted(() => {
  fetchCustomers();
});
</script>

<template>
  <section class="customers-page">

    <!-- Page heading -->
    <div class="customers-heading">
      <div>
        <h2>Customers</h2>
        <p>Manage and organize your customer information.</p>
      </div>

      <button class="primary-button" @click="openCreateForm">
        + Add Customer
      </button>
    </div>

    <!-- Success and error messages -->
    <p v-if="success" class="success-message">
      {{ success }}
    </p>

    <p v-if="error" class="error-message">
      {{ error }}
    </p>

    <!-- Customer form -->
    <div v-if="showForm" class="customer-form-panel">
      <div class="form-heading">
        <h3>
          {{ editingCustomerId === null ? "Add New Customer" : "Edit Customer" }}
        </h3>

        <button class="close-button" @click="closeForm">
          ×
        </button>
      </div>

      <form @submit.prevent="saveCustomer" class="customer-form">

        <div class="form-group">
          <label for="customer-name">Customer Name</label>
          <input
            id="customer-name"
            v-model="form.name"
            type="text"
            placeholder="Enter customer name"
            maxlength="100"
            required
          />
        </div>

        <div class="form-group">
          <label for="customer-email">Email Address</label>
          <input
            id="customer-email"
            v-model="form.email"
            type="email"
            placeholder="Enter email address"
            maxlength="255"
            required
          />
        </div>

        <div class="form-group">
          <label for="customer-phone">Phone Number</label>
          <input
            id="customer-phone"
            v-model="form.phone"
            type="text"
            placeholder="Enter phone number"
            maxlength="30"
            required
          />
        </div>

        <div class="form-group">
          <label for="customer-company">Company</label>
          <input
            id="customer-company"
            v-model="form.company"
            type="text"
            placeholder="Enter company name"
            maxlength="150"
            required
          />
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
                : editingCustomerId === null
                  ? "Create Customer"
                  : "Save Changes"
            }}
          </button>
        </div>

      </form>
    </div>

    <!-- Customer table panel -->
    <div class="customer-table-panel">

      <div class="table-toolbar">
        <div>
          <h3>Customer Directory</h3>
          <p>{{ filteredCustomers.length }} customers displayed</p>
        </div>

        <input
          v-model="searchQuery"
          type="search"
          class="search-input"
          placeholder="Search name, email or company..."
        />
      </div>

      <div v-if="loading" class="table-message">
        Loading customers...
      </div>

      <div
        v-else-if="filteredCustomers.length === 0"
        class="table-message"
      >
        {{
          customers.length === 0
            ? "No customers found. Add your first customer."
            : "No customers match your search."
        }}
      </div>

      <div v-else class="table-responsive">
        <table class="customer-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Company</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="customer in filteredCustomers"
              :key="customer.id"
            >
              <td>#{{ customer.id }}</td>

              <td class="customer-name-cell">
                {{ customer.name }}
              </td>

              <td>{{ customer.email }}</td>
              <td>{{ customer.phone }}</td>
              <td>{{ customer.company }}</td>

              <td>
                <div class="table-actions">
                  <button
                    class="edit-button"
                    @click="openEditForm(customer)"
                  >
                    Edit
                  </button>

                  <button
                    class="delete-button"
                    @click="deleteCustomer(customer.id)"
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
