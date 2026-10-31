<script setup>
import { ref, onMounted } from "vue";
import api from "./services/api";

// Store customer records
const customers = ref([]);

// Store form information
const form = ref({
    name: "",
    email: "",
    phone: "",
    company: "",
});

// Track loading and errors
const loading = ref(false);
const saving = ref(false);
const error = ref("");
const success = ref("");

// Retrieve all customers from FastAPI
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

// Create a new customer
async function createCustomer() {
    saving.value = true;
    error.value = "";
    success.value = "";

    try {
        const response = await api.post("/customers", form.value);

        customers.value.push(response.data);

        form.value = {
            name: "",
            email: "",
            phone: "",
            company: "",
        };

        success.value = "Customer created successfully!";
    } catch (err) {
        error.value =
            err.response?.data?.detail ||
            "Unable to create customer.";

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

    try {
        await api.delete(`/customers/${customerId}`);

        customers.value = customers.value.filter(
            customer => customer.id !== customerId
        );

        success.value = "Customer deleted successfully!";
        error.value = "";
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
    <div class="app-container">

        <header class="topbar">
            <div class="brand">
                <h2>ClientFlow CRM</h2>
                <span>Customer Management System</span>
            </div>
        </header>

        <main class="main-content">

            <section class="page-heading">
                <div>
                    <h1>Customer Management</h1>
                    <p>Manage your customers in one place.</p>
                </div>

                <div class="customer-count">
                    <strong>{{ customers.length }}</strong>
                    <span>Total Customers</span>
                </div>
            </section>

            <section class="content-grid">

                <!-- Customer creation form -->
                <div class="panel">
                    <h2>Add New Customer</h2>

                    <form @submit.prevent="createCustomer">

                        <label>Customer Name</label>
                        <input
                            v-model="form.name"
                            type="text"
                            placeholder="Enter customer name"
                            required
                        />

                        <label>Email Address</label>
                        <input
                            v-model="form.email"
                            type="email"
                            placeholder="Enter email address"
                            required
                        />

                        <label>Phone Number</label>
                        <input
                            v-model="form.phone"
                            type="text"
                            placeholder="Enter phone number"
                            required
                        />

                        <label>Company</label>
                        <input
                            v-model="form.company"
                            type="text"
                            placeholder="Enter company name"
                            required
                        />

                        <button type="submit" :disabled="saving">
                            {{ saving ? "Saving..." : "Add Customer" }}
                        </button>

                    </form>
                </div>

                <!-- Customer list -->
                <div class="panel">
                    <div class="list-heading">
                        <h2>Customers</h2>

                        <button
                            class="refresh-button"
                            @click="fetchCustomers"
                            :disabled="loading"
                        >
                            Refresh
                        </button>
                    </div>

                    <p v-if="loading">Loading customers...</p>

                    <p v-else-if="customers.length === 0">
                        No customers found. Add your first customer.
                    </p>

                    <div v-else class="customer-list">

                        <div
                            v-for="customer in customers"
                            :key="customer.id"
                            class="customer-card"
                        >
                            <div>
                                <h3>{{ customer.name }}</h3>
                                <p>{{ customer.email }}</p>
                                <p>{{ customer.company }}</p>
                                <small>Customer ID: {{ customer.id }}</small>
                            </div>

                            <button
                                class="delete-button"
                                @click="deleteCustomer(customer.id)"
                            >
                                Delete
                            </button>
                        </div>

                    </div>
                </div>

            </section>

            <p v-if="success" class="success-message">
                {{ success }}
            </p>

            <p v-if="error" class="error-message">
                {{ error }}
            </p>

        </main>
    </div>
</template>