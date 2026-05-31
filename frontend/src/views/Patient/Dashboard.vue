<template>
  <div class="patient-page">
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
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </nav>
    </header>

    <marquee style="background-color: black; color: white">
      Good health starts with awareness - welcome to your dashboard.
    </marquee>

    <div class="container py-4">
      <h2 class="mb-4">Patient Dashboard</h2>

      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3">
            <div>
              <h5 class="mb-1">Quick Access</h5>
              <p class="mb-0 text-muted">Open the main Health Guardian+ patient modules.</p>
            </div>
          </div>
          <div class="d-flex flex-wrap gap-2">
            <router-link to="/patient/profile" class="btn btn-outline-secondary btn-sm">Profile</router-link>
            <router-link to="/patient/medical-records" class="btn btn-outline-secondary btn-sm">Medical Records</router-link>
            <router-link to="/patient/reports" class="btn btn-outline-secondary btn-sm">Reports</router-link>
            <router-link to="/patient/appointment-booking" class="btn btn-outline-secondary btn-sm">Book Appointment</router-link>
            <router-link to="/patient/my-appointments" class="btn btn-outline-secondary btn-sm">My Appointments</router-link>
            <router-link to="/patient/medicine-reminder" class="btn btn-outline-secondary btn-sm">Medicine Reminder</router-link>
            <router-link to="/patient/emergency-sos" class="btn btn-outline-secondary btn-sm">Emergency SOS</router-link>
            <router-link to="/patient/ai-health-assistant" class="btn btn-outline-secondary btn-sm">AI Assistant</router-link>
            <router-link to="/patient/accessibility" class="btn btn-outline-secondary btn-sm">Accessibility</router-link>
            <router-link to="/patient/health-card" class="btn btn-outline-secondary btn-sm">Health Card</router-link>
          </div>
        </div>
      </div>

      <div v-if="loading" class="alert alert-info">Loading dashboard...</div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div class="card mb-4 shadow">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">My Upcoming Appointments</h5>
        </div>
        <div class="card-body">
          <div v-if="upcomingAppointments.length" class="table-responsive">
            <table class="table table-bordered mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Doctor</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in upcomingAppointments" :key="app.App_id">
                  <td>{{ app.Date }}</td>
                  <td>{{ formatTime(app.Time) }}</td>
                  <td>{{ app.Doctor || '-' }}</td>
                  <td>
                    <span class="badge" :class="badgeClass(app.Status)">{{ app.Status }}</span>
                  </td>
                  <td>
                    <button
                      v-if="app.Status === 'Booked'"
                      class="btn btn-danger btn-sm"
                      :disabled="loading"
                      @click="cancelAppointment(app.App_id)"
                    >
                      Cancel
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="mb-0">No upcoming appointments found.</p>
        </div>
      </div>

      <div class="card mb-4 shadow">
        <div class="card-header bg-secondary text-white">
          <h5 class="mb-0">Treatment History</h5>
        </div>
        <div class="card-body">
          <div class="d-flex flex-wrap gap-2 mb-3">
            <button class="btn btn-outline-primary btn-sm" :disabled="exporting" @click="startExport">
              {{ exporting ? 'Export in progress...' : 'Export Treatment History (CSV)' }}
            </button>
            <button
              v-if="exportDownloadUrl"
              class="btn btn-success btn-sm"
              @click="downloadExport"
            >
              Download CSV
            </button>
          </div>
          <p v-if="exportStatus" class="mb-2"><strong>Export Status:</strong> {{ exportStatus }}</p>
          <p v-if="exportMessage" class="text-success mb-2">{{ exportMessage }}</p>
          <p v-if="exportError" class="text-danger mb-2">{{ exportError }}</p>

          <div v-if="treatmentHistory.length" class="table-responsive">
            <table class="table table-bordered mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Doctor</th>
                  <th>Prescription</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in treatmentHistory" :key="t.Treatment_id">
                  <td>{{ t.Date }}</td>
                  <td>{{ t.Doctor }}</td>
                  <td>{{ t.Prescription || '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="mb-0">No treatment history found.</p>
        </div>
      </div>

      <div class="card mb-4 shadow">
        <div class="card-header bg-info text-dark">
          <h5 class="mb-0">Available Slots (Today + Next 7 Days)</h5>
        </div>
        <div class="card-body">
          <div class="row g-2 mb-3">
            <div class="col-md-5">
              <label class="form-label">Filter by Doctor</label>
              <select v-model="selectedDoctorId" class="form-select">
                <option value="">All doctors</option>
                <option v-for="doc in doctors" :key="doc.Doc_id" :value="String(doc.Doc_id)">
                  {{ doc.Name }}
                </option>
              </select>
            </div>
            <div class="col-md-4 d-flex align-items-end">
              <button
                class="btn btn-outline-primary w-100"
                :disabled="!selectedDoctorId"
                @click="openDoctorProfile"
              >
                Open Doctor Profile
              </button>
            </div>
          </div>

          <div v-if="filteredSlots.length" class="table-responsive">
            <table class="table table-bordered mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Doctor</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="slot in filteredSlots" :key="slot.App_id">
                  <td>{{ slot.Date }}</td>
                  <td>{{ formatTime(slot.Time) }}</td>
                  <td>{{ slot.Doctor }}</td>
                  <td>
                    <button class="btn btn-success btn-sm" :disabled="loading" @click="bookSlot(slot.App_id)">
                      Book
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="mb-0">No available slots right now.</p>
        </div>
      </div>

      <div class="card shadow">
        <div class="card-header bg-light">
          <h5 class="mb-0">Departments</h5>
        </div>
        <div class="card-body">
          <ul class="list-group">
            <li v-for="dep in departments" :key="dep.Dept_id" class="list-group-item">
              {{ dep.Dept_name }}
            </li>
            <li v-if="!departments.length" class="list-group-item text-danger">No departments found.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PatientDashboard',
  data() {
    return {
      loading: false,
      error: '',
      selectedDoctorId: '',
      upcomingAppointments: [],
      treatmentHistory: [],
      doctors: [],
      departments: [],
      availableSlots: [],
      exporting: false,
      exportStatus: '',
      exportJobId: null,
      exportDownloadUrl: '',
      exportMessage: '',
      exportError: '',
      exportPoller: null,
    }
  },
  computed: {
    filteredSlots() {
      if (!this.selectedDoctorId) {
        return this.availableSlots
      }
      return this.availableSlots.filter((s) => String(s.Doctor_id) === this.selectedDoctorId)
    },
  },
  methods: {
    normalizeAvailableSlotsResponse(payload) {
      if (Array.isArray(payload) && payload.length) {
        return payload[0]?.available_slots || []
      }
      return payload?.available_slots || []
    },
    tokenHeaders() {
      const token = localStorage.getItem('access_token')
      return { Authorization: `Bearer ${token}` }
    },
    formatTime(value) {
      return value ? value.slice(0, 5) : ''
    },
    badgeClass(status) {
      if (status === 'Booked') return 'bg-success'
      if (status === 'Cancelled') return 'bg-danger'
      if (status === 'Completed') return 'bg-info text-dark'
      return 'bg-secondary'
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    },
    openDoctorProfile() {
      if (!this.selectedDoctorId) {
        return
      }

      this.$router.push({ name: 'patient-doctor-profile', params: { id: this.selectedDoctorId } })
    },
    async loadDashboard() {
      const token = localStorage.getItem('access_token')
      if (!token) {
        this.$router.push('/login')
        return
      }

      this.loading = true
      this.error = ''
      try {
        const [dashboardResp, slotsResp] = await Promise.all([
          axios.get('http://127.0.0.1:5000/patient/dashboard', {
            headers: this.tokenHeaders(),
          }),
          axios.get('http://127.0.0.1:5000/patient/available-slots', {
            headers: this.tokenHeaders(),
          }),
        ])

        this.upcomingAppointments = dashboardResp.data.upcoming_appointments || []
        this.treatmentHistory = dashboardResp.data.treatment_history || []
        this.doctors = dashboardResp.data.doctors || []
        this.departments = dashboardResp.data.departments || []
        this.availableSlots = this.normalizeAvailableSlotsResponse(slotsResp.data)
      } catch (err) {
        console.error(err)
        this.error = 'Unable to load patient dashboard data.'
      } finally {
        this.loading = false
      }
    },
    async bookSlot(slotId) {
      this.loading = true
      try {
        await axios.post(
          `http://127.0.0.1:5000/patient/book-slot/${slotId}`,
          {},
          { headers: this.tokenHeaders() },
        )
        await this.loadDashboard()
      } catch (err) {
        console.error(err)
        alert('Failed to book slot.')
        this.loading = false
      }
    },
    async cancelAppointment(appId) {
      this.loading = true
      try {
        await axios.post(
          `http://127.0.0.1:5000/patient/cancel-slot/${appId}`,
          {},
          { headers: this.tokenHeaders() },
        )
        await this.loadDashboard()
      } catch (err) {
        console.error(err)
        alert('Failed to cancel appointment.')
        this.loading = false
      }
    },
    async startExport() {
      this.exporting = true
      this.exportStatus = 'QUEUED'
      this.exportError = ''
      this.exportMessage = ''
      this.exportDownloadUrl = ''

      try {
        const resp = await axios.post(
          'http://127.0.0.1:5000/patient/export-treatment-history',
          {},
          { headers: this.tokenHeaders() },
        )
        this.exportJobId = resp.data.job_id
        this.exportStatus = resp.data.status || 'QUEUED'
        this.startExportPolling()
      } catch (err) {
        console.error(err)
        this.exporting = false
        this.exportError = err?.response?.data?.message || 'Failed to start export job.'
      }
    },
    startExportPolling() {
      if (this.exportPoller) {
        clearInterval(this.exportPoller)
      }
      this.exportPoller = setInterval(this.pollExportStatus, 2000)
    },
    async pollExportStatus() {
      if (!this.exportJobId) {
        return
      }

      try {
        const resp = await axios.get(
          `http://127.0.0.1:5000/patient/export-treatment-history/${this.exportJobId}`,
          { headers: this.tokenHeaders() },
        )

        this.exportStatus = resp.data.status || ''
        if (resp.data.status === 'COMPLETED') {
          this.exporting = false
          this.exportMessage = 'Export completed. You can download the CSV now.'
          this.exportDownloadUrl = `http://127.0.0.1:5000${resp.data.download_url}`
          if (this.exportPoller) {
            clearInterval(this.exportPoller)
            this.exportPoller = null
          }
        } else if (resp.data.status === 'FAILED') {
          this.exporting = false
          this.exportError = resp.data.error || 'Export failed.'
          if (this.exportPoller) {
            clearInterval(this.exportPoller)
            this.exportPoller = null
          }
        }
      } catch (err) {
        console.error(err)
        this.exporting = false
        this.exportError = 'Unable to fetch export status.'
        if (this.exportPoller) {
          clearInterval(this.exportPoller)
          this.exportPoller = null
        }
      }
    },
    downloadExport() {
      if (!this.exportDownloadUrl) {
        return
      }
      axios
        .get(this.exportDownloadUrl, {
          headers: this.tokenHeaders(),
          responseType: 'blob',
        })
        .then((resp) => {
          const blobUrl = window.URL.createObjectURL(new Blob([resp.data]))
          const link = document.createElement('a')
          link.href = blobUrl
          link.setAttribute('download', `treatment_history_${this.exportJobId || 'export'}.csv`)
          document.body.appendChild(link)
          link.click()
          link.remove()
          window.URL.revokeObjectURL(blobUrl)
        })
        .catch((err) => {
          console.error(err)
          this.exportError = err?.response?.data?.message || 'Failed to download export file.'
        })
    },
  },
  mounted() {
    this.loadDashboard()
  },
  beforeUnmount() {
    if (this.exportPoller) {
      clearInterval(this.exportPoller)
      this.exportPoller = null
    }
  },
}
</script>

<style scoped>
.patient-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>

