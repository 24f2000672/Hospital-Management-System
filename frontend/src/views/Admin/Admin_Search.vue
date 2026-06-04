<template>
    <!-- Header -->
    <header
      style="background-color: white"
      class="navbar d-flex justify-content-between align-items-center px-4"
    >
      <div class="logo-section">
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>
      <div class="brand-center text-center">
        <h1>Vardha Hospital</h1>
      </div>
      <nav class="nav-links" style="display: flex; gap: 30px">
        <b><router-link to="/" class="btn btn-outline-danger">Logout</router-link></b>
      </nav>
    </header>

    <!-- Flash Messages -->
    <div class="container mt-3">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['alert', `alert-${message.category}`, 'alert-dismissible', 'fade', 'show']"
        role="alert"
      >
        {{ message.text }}
        <button
          type="button"
          class="btn-close"
          @click="removeMessage(index)"
          aria-label="Close"
        ></button>
      </div>
    </div>

    <!-- Search Results -->
    <div class="container mt-5">
      <h2>🔍 Search Results for "{{ searchQuery }}"</h2>
      <hr />

      <h4>Doctors</h4>
      <div v-if="doctorResults.length > 0" class="list-group">
        <div
          v-for="doctor in doctorResults"
          :key="doctor.id"
          class="list-group-item list-group-item-action"
        >
          <div class="d-flex justify-content-between">
            <strong>{{ doctor.first_name }} {{ doctor.last_name }}</strong>
            <span class="badge bg-success">Dr.</span>
          </div>
          <small class="text-muted"
            >Department: {{ doctor.department }} | ID: {{ doctor.id }}</small
          >
        </div>
      </div>
      <div v-else>
        <p class="text-muted">No doctors found.</p>
      </div>

      <h4 class="mt-5">Patients</h4>
      <div v-if="patientResults.length > 0" class="list-group">
        <div
          v-for="patient in patientResults"
          :key="patient.id"
          class="list-group-item list-group-item-action"
        >
          <div class="d-flex justify-content-between">
            <strong>{{ patient.first_name }} {{ patient.last_name }}</strong>
            <span class="badge bg-info">Patient</span>
          </div>
          <small class="text-muted">Email: {{ patient.email }} | ID: {{ patient.id }}</small>
        </div>
      </div>
      <div v-else>
        <p class="text-muted">No patients found.</p>
      </div>

      <router-link to="/admin/dashboard" class="btn btn-secondary mt-3"
        >⬅️ Back to Dashboard</router-link
      >
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminSearch',
  data() {
    return {
      searchQuery: '',
      doctorResults: [],
      patientResults: [],
      messages: [],
      loading: false,
    }
  },
  mounted() {
    // Get search query from route params
    this.searchQuery = this.$route.query.query || ''
    if (this.searchQuery) {
      this.performSearch()
    }
  },
  methods: {
    async performSearch() {
      if (!this.searchQuery.trim()) {
        this.doctorResults = []
        this.patientResults = []
        return
      }

      this.loading = true
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get('http://127.0.0.1:5000/search', {
          params: { query: this.searchQuery },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        this.doctorResults = response.data.doctors || []
        this.patientResults = response.data.patients || []
      } catch (error) {
        console.error('Search error:', error)
        this.addMessage('Error performing search', 'danger')
      } finally {
        this.loading = false
      }
    },
    addMessage(text, category = 'info') {
      this.messages.push({ text, category })
      setTimeout(() => {
        this.removeMessage(0)
      }, 5000)
    },
    removeMessage(index) {
      this.messages.splice(index, 1)
    },
  },
}
</script>

<style scoped>
.search-results-page {
  padding: 20px;
}

header {
  margin-bottom: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
}

h1 {
  margin: 0;
  color: #333;
  font-weight: 600;
  letter-spacing: 1px;
}

h2 {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 20px;
}

h4 {
  color: #34495e;
  font-weight: 600;
  margin-top: 30px;
  margin-bottom: 15px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.logo-section {
  flex-shrink: 0;
}

.brand-center {
  flex-grow: 1;
}

.list-group-item {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
  padding: 15px;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateX(5px);
}

.badge {
  font-size: 0.75rem;
  padding: 5px 10px;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.alert {
  border-radius: 6px;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.text-muted {
  color: #7f8c8d !important;
}

small {
  display: block;
  margin-top: 5px;
}
</style>
