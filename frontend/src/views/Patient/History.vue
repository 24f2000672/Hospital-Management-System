<template>
  <div class="history-page">
    <header
      style="background-color: white"
      class="navbar d-flex justify-content-between align-items-center px-4"
    >
      <div>
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>

      <div class="text-center">
        <h1>Vardha Hospital</h1>
      </div>

      <nav style="display: flex; gap: 20px">
        <button class="btn btn-outline-secondary" @click="goBack">Dashboard</button>
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </nav>
    </header>

    <div class="container py-4">
      <h3 class="mb-3">Patient History</h3>

      <div v-if="loading" class="alert alert-info">Loading history...</div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="patient" class="card mb-4 shadow-sm">
        <div class="card-body">
          <h5 class="mb-1">{{ patient.Name }}</h5>
          <p class="mb-0 text-muted">{{ patient.Email }}</p>
        </div>
      </div>

      <div class="card mb-4 shadow">
        <div class="card-header bg-secondary text-white">
          <h5 class="mb-0">Appointment Timeline</h5>
        </div>
        <div class="card-body">
          <div v-if="appointments.length" class="table-responsive">
            <table class="table table-bordered mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in appointments" :key="a.App_id">
                  <td>{{ a.Date }}</td>
                  <td>{{ formatTime(a.Time) }}</td>
                  <td>{{ a.Status }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="mb-0">No appointments found.</p>
        </div>
      </div>

      <div class="card shadow">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">Treatment Records</h5>
        </div>
        <div class="card-body">
          <div v-if="treatments.length" class="table-responsive">
            <table class="table table-bordered mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Diagnosis</th>
                  <th>Prescription</th>
                  <th>Progress</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in treatments" :key="t.Treatment_id">
                  <td>{{ t.Date }}</td>
                  <td>{{ formatTime(t.Time) }}</td>
                  <td>{{ t.Diagnosis || '-' }}</td>
                  <td>{{ t.Prescription || '-' }}</td>
                  <td>{{ t.Progress || '-' }}</td>
                  <td>{{ t.Notes || '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="mb-0">No treatment records found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PatientHistoryView',
  data() {
    return {
      loading: false,
      error: '',
      patient: null,
      appointments: [],
      treatments: [],
    }
  },
  computed: {
    patientId() {
      return Number(this.$route.params.id)
    },
  },
  methods: {
    getToken() {
      return localStorage.getItem('access_token')
    },
    formatTime(value) {
      return value ? value.slice(0, 5) : ''
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    },
    goBack() {
      this.$router.push('/doctor/dashboard')
    },
    async loadHistory() {
      this.loading = true
      this.error = ''

      const token = this.getToken()
      if (!token) {
        this.$router.push('/login')
        return
      }

      if (!this.patientId) {
        this.error = 'Invalid patient id.'
        this.loading = false
        return
      }

      try {
        const resp = await axios.get(
          `http://127.0.0.1:5000/doctor/patient-history/${this.patientId}`,
          { headers: { Authorization: `Bearer ${token}` } },
        )

        this.patient = resp.data.patient || null
        this.appointments = resp.data.appointments || []
        this.treatments = resp.data.treatments || []
      } catch (err) {
        console.error(err)
        this.error = err?.response?.data?.message || 'Unable to load patient history.'
      } finally {
        this.loading = false
      }
    },
  },
  mounted() {
    this.loadHistory()
  },
}
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>
