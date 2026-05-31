<template>
  <div class="management-page">
    <header class="page-header container-fluid px-4 px-lg-5 py-3">
      <div class="d-flex align-items-center gap-3">
        <img src="@/assets/logo.png" alt="Health Guardian+" class="header-logo" />
        <div>
          <p class="eyebrow mb-1">Administrator</p>
          <h1 class="mb-0">Appointment Monitoring</h1>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <router-link to="/admin/dashboard" class="btn btn-outline-secondary">Dashboard</router-link>
        <router-link to="/admin/patients" class="btn btn-outline-primary">Patients</router-link>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </header>

    <main class="container-fluid px-4 px-lg-5 pb-5">
      <section class="summary-strip">
        <div>
          <span class="summary-label">Upcoming</span>
          <strong>{{ upcomingAppointments.length }}</strong>
        </div>
        <div>
          <span class="summary-label">Past</span>
          <strong>{{ pastAppointments.length }}</strong>
        </div>
        <div>
          <span class="summary-label">Filter</span>
          <select v-model="statusFilter" class="form-select">
            <option value="all">All statuses</option>
            <option value="Booked">Booked</option>
            <option value="Completed">Completed</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>
      </section>

      <div v-if="loading" class="alert alert-info">Loading appointments...</div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <section class="panel-card">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3">
          <div>
            <p class="eyebrow mb-1">Active queue</p>
            <h2 class="mb-0">Upcoming / available appointments</h2>
          </div>
          <button class="btn btn-outline-primary" @click="refresh">Refresh</button>
        </div>

        <div class="table-responsive">
          <table class="table align-middle">
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Time</th>
                <th>Doctor</th>
                <th>Patient</th>
                <th>Status</th>
                <th class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appointment in filteredUpcoming" :key="appointment.id">
                <td>{{ appointment.id }}</td>
                <td>{{ appointment.date }}</td>
                <td>{{ formatTime(appointment.time) }}</td>
                <td>{{ appointment.doctor_name || '-' }}</td>
                <td>{{ appointment.patient_name || '-' }}</td>
                <td>
                  <span class="status-chip" :class="statusClass(appointment.status)">
                    {{ appointment.status || 'Unknown' }}
                  </span>
                </td>
                <td>
                  <div class="d-flex justify-content-end gap-2 flex-wrap">
                    <select v-model="statusDraft[appointment.id]" class="form-select form-select-sm w-auto">
                      <option value="Booked">Booked</option>
                      <option value="Completed">Completed</option>
                      <option value="Cancelled">Cancelled</option>
                    </select>
                    <button class="btn btn-primary btn-sm" @click="updateStatus(appointment.id)">
                      Update
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!filteredUpcoming.length">
                <td colspan="7" class="text-center py-4 text-muted">No appointments to show.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="panel-card mt-4">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3">
          <div>
            <p class="eyebrow mb-1">History</p>
            <h2 class="mb-0">Past appointments</h2>
          </div>
        </div>

        <div class="table-responsive">
          <table class="table align-middle table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Time</th>
                <th>Doctor</th>
                <th>Patient</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appointment in filteredPast" :key="appointment.id">
                <td>{{ appointment.id }}</td>
                <td>{{ appointment.date }}</td>
                <td>{{ formatTime(appointment.time) }}</td>
                <td>{{ appointment.doctor_name || '-' }}</td>
                <td>{{ appointment.patient_name || '-' }}</td>
                <td>
                  <span class="status-chip" :class="statusClass(appointment.status)">
                    {{ appointment.status || 'Unknown' }}
                  </span>
                </td>
              </tr>
              <tr v-if="!filteredPast.length">
                <td colspan="6" class="text-center py-4 text-muted">No past appointments found.</td>
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
  name: 'AdminAppointments',
  data() {
    return {
      loading: true,
      error: '',
      statusFilter: 'all',
      upcomingAppointments: [],
      pastAppointments: [],
      statusDraft: {},
    }
  },
  computed: {
    filteredUpcoming() {
      if (this.statusFilter === 'all') {
        return this.upcomingAppointments
      }

      return this.upcomingAppointments.filter((appointment) => appointment.status === this.statusFilter)
    },
    filteredPast() {
      if (this.statusFilter === 'all') {
        return this.pastAppointments
      }

      return this.pastAppointments.filter((appointment) => appointment.status === this.statusFilter)
    },
  },
  mounted() {
    this.loadAppointments()
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    formatTime(value) {
      return value ? value.slice(0, 5) : '-'
    },
    statusClass(status) {
      if (status === 'Completed') return 'success'
      if (status === 'Cancelled') return 'danger'
      if (status === 'Booked') return 'primary'
      return 'muted'
    },
    async loadAppointments() {
      this.loading = true
      this.error = ''

      try {
        const response = await api.get('/admin/dashboard', { headers: authHeaders() })
        this.upcomingAppointments = (response.data.available_appointments || []).map((appointment) => ({
          id: appointment.id,
          date: appointment.date,
          time: appointment.time,
          status: appointment.status,
          doctor_name: appointment.doctor_name,
          patient_name: appointment.patient_name,
        }))
        this.pastAppointments = (response.data.past_appointments || []).map((appointment) => ({
          id: appointment.id,
          date: appointment.date,
          time: appointment.time,
          status: appointment.status,
          doctor_name: appointment.doctor_name,
          patient_name: appointment.patient_name,
        }))

        this.statusDraft = {
          ...this.statusDraft,
          ...Object.fromEntries(
            [...this.upcomingAppointments, ...this.pastAppointments].map((appointment) => [
              appointment.id,
              appointment.status || 'Booked',
            ]),
          ),
        }
      } catch (error) {
        console.error(error)
        this.error = error?.response?.data?.message || 'Unable to load appointments.'

        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    refresh() {
      this.loadAppointments()
    },
    async updateStatus(appointmentId) {
      try {
        await api.post(
          `/update_status/${appointmentId}`,
          { status: this.statusDraft[appointmentId] || 'Booked' },
          { headers: authHeaders() },
        )
        await this.loadAppointments()
      } catch (error) {
        console.error(error)
        alert(error?.response?.data?.message || 'Unable to update appointment status.')
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

.status-chip.primary {
  background: rgba(21, 94, 117, 0.12);
  color: var(--health-primary-strong);
}

.status-chip.muted {
  background: rgba(92, 111, 130, 0.12);
  color: var(--health-muted);
}

@media (max-width: 992px) {
  .page-header {
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