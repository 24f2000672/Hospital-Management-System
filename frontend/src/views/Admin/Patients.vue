<template>
  <div class="management-page">
    <header class="page-header container-fluid px-4 px-lg-5 py-3">
      <div class="d-flex align-items-center gap-3">
        <img src="@/assets/logo.png" alt="Health Guardian+" class="header-logo" />
        <div>
          <p class="eyebrow mb-1">Administrator</p>
          <h1 class="mb-0">Patient Management</h1>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <router-link to="/admin/dashboard" class="btn btn-outline-secondary">Dashboard</router-link>
        <router-link to="/admin/appointments" class="btn btn-outline-primary">Appointments</router-link>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </header>

    <main class="container-fluid px-4 px-lg-5 pb-5">
      <section class="summary-strip">
        <div>
          <span class="summary-label">Patients</span>
          <strong>{{ filteredPatients.length }}</strong>
        </div>
        <div>
          <span class="summary-label">Blacklisted</span>
          <strong>{{ blacklistedCount }}</strong>
        </div>
        <div>
          <span class="summary-label">Search</span>
          <input v-model="searchTerm" type="search" class="form-control" placeholder="Filter by name" />
        </div>
      </section>

      <div v-if="loading" class="alert alert-info">Loading patients...</div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <section class="panel-card">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3">
          <div>
            <p class="eyebrow mb-1">Roster</p>
            <h2 class="mb-0">Registered patients</h2>
          </div>
          <button class="btn btn-outline-primary" @click="refresh">Refresh</button>
        </div>

        <div class="table-responsive">
          <table class="table align-middle">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Status</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="patient in filteredPatients" :key="patient.id">
                <td>{{ patient.id }}</td>
                <td>
                  <strong>{{ patient.first_name }} {{ patient.last_name }}</strong>
                </td>
                <td>
                  <span class="status-chip" :class="patient.is_blacklisted ? 'danger' : 'success'">
                    {{ patient.is_blacklisted ? 'Blacklisted' : 'Active' }}
                  </span>
                </td>
                <td>
                  <div class="d-flex justify-content-end flex-wrap gap-2">
                    <button class="btn btn-outline-primary btn-sm" @click="editPatient(patient.id)">
                      Update
                    </button>
                    <button
                      class="btn btn-sm"
                      :class="patient.is_blacklisted ? 'btn-success' : 'btn-dark'"
                      @click="toggleBlacklist(patient)"
                    >
                      {{ patient.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
                    </button>
                    <button class="btn btn-outline-danger btn-sm" @click="deletePatient(patient)">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!filteredPatients.length">
                <td colspan="4" class="text-center py-4 text-muted">No patients match your filter.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { api, authHeaders, isUnauthorized } from '@/services/api'

export default {
  name: 'AdminPatients',
  data() {
    return {
      loading: true,
      error: '',
      searchTerm: '',
      patients: [],
    }
  },
  computed: {
    filteredPatients() {
      const term = this.searchTerm.trim().toLowerCase()

      if (!term) {
        return this.patients
      }

      return this.patients.filter((patient) => {
        const fullName = `${patient.first_name} ${patient.last_name}`.toLowerCase()
        return fullName.includes(term)
      })
    },
    blacklistedCount() {
      return this.patients.filter((patient) => patient.is_blacklisted).length
    },
  },
  mounted() {
    this.loadPatients()
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    async loadPatients() {
      this.loading = true
      this.error = ''

      try {
        const response = await api.get('/admin/dashboard', { headers: authHeaders() })
        this.patients = response.data.patients || []
      } catch (error) {
        console.error(error)
        this.error = error?.response?.data?.message || 'Unable to load patients.'

        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    refresh() {
      this.loadPatients()
    },
    editPatient(patientId) {
      this.$router.push({ path: '/admin/update-patient', query: { id: patientId } })
    },
    async toggleBlacklist(patient) {
      const endpoint = patient.is_blacklisted
        ? `/remove_blacklist_patient/${patient.id}`
        : `/blacklist_patient/${patient.id}`

      try {
        await api.post(endpoint, {}, { headers: authHeaders() })
        await this.loadPatients()
      } catch (error) {
        console.error(error)
        alert(error?.response?.data?.message || 'Unable to update blacklist status.')
      }
    },
    async deletePatient(patient) {
      const confirmed = window.confirm(
        `Delete ${patient.first_name} ${patient.last_name}? This cannot be undone.`,
      )

      if (!confirmed) {
        return
      }

      try {
        await api.delete(`/delete_patient/${patient.id}`, { headers: authHeaders() })
        await this.loadPatients()
      } catch (error) {
        console.error(error)
        alert(error?.response?.data?.message || 'Unable to delete patient.')
      }
    },
  },
}
</script>

<style scoped>
.management-page {
  min-height: 100vh;
}

.page-header,
.panel-card,
.summary-strip {
  margin: 0 auto;
  max-width: 1320px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.header-logo {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 18px;
}

.eyebrow,
.summary-label {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.72rem;
  color: var(--health-muted);
}

.summary-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.25rem;
}

.summary-strip > div,
.panel-card {
  border-radius: 28px;
  background: var(--health-surface);
  backdrop-filter: blur(16px);
  border: 1px solid var(--health-border);
  box-shadow: var(--health-shadow);
}

.summary-strip > div {
  padding: 1rem 1.2rem;
}

.summary-strip strong {
  display: block;
  margin-top: 0.35rem;
  font-size: 1.75rem;
}

.panel-card {
  margin-top: 1.5rem;
  padding: 1.25rem;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  font-size: 0.78rem;
  font-weight: 700;
}

.status-chip.success {
  background: rgba(22, 163, 74, 0.12);
  color: var(--health-success);
}

.status-chip.danger {
  background: rgba(220, 38, 38, 0.12);
  color: var(--health-danger);
}

@media (max-width: 992px) {
  .page-header,
  .summary-strip {
    grid-template-columns: 1fr;
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 768px) {
  .summary-strip {
    grid-template-columns: 1fr;
  }
}
</style>