<template>
  <div class="patient-page">

    <!-- Header -->
    <header class="dashboard-header">
      <div class="logo-section">
        <img
          src="@/assets/logo.png"
          height="70"
          width="70"
          alt="Vardha Hospital Logo"
        />
      </div>

      <div class="title-section">
        <h2>Welcome to Vardha Hospital</h2>
        <p>
          Access all your healthcare services from one place.
        </p>
      </div>

      <div class="action-section">
        <button
          class="btn btn-primary"
          @click="$router.push('/patient/tabs')"
        >
          📱 Mobile Tabs
        </button>

        <button
          class="btn btn-danger"
          @click="logout"
        >
          🚪 Logout
        </button>
      </div>
    </header>

    <!-- Notice -->
    <marquee style="background:#000;color:#fff;padding:10px;">
      Good health starts with awareness - welcome to your dashboard.
    </marquee>

    <div class="container py-4">

      <h2 class="mb-4 text-primary">Patient Dashboard</h2>

      <!-- Quick Access -->
      <div class="card shadow-sm mb-4">
        <div class="card-body bg-light text-black">

          <div
            class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3"
          >
            <div>
              <h5 class="mb-1 text-primary">Quick Access</h5>
              <p class="mb-0 text-muted">
                Open the main Health Guardian+ patient modules.
              </p>
            </div>

            <router-link
              to="/patient/tabs"
              class="btn btn-primary btn-sm"
            >
              Open Mobile Tabs
            </router-link>
          </div>

          <div class="d-flex flex-wrap gap-2">
            <router-link
              to="/patient/profile"
              class="btn btn-outline-secondary btn-sm"
            >
              Profile
            </router-link>

            <router-link
              to="/patient/medical-records"
              class="btn btn-outline-secondary btn-sm"
            >
              Medical Records
            </router-link>

            <router-link
              to="/patient/reports"
              class="btn btn-outline-secondary btn-sm"
            >
              Reports
            </router-link>

            <router-link
              to="/patient/appointment-booking"
              class="btn btn-outline-secondary btn-sm"
            >
              Book Appointment
            </router-link>

            <router-link
              to="/patient/my-appointments"
              class="btn btn-outline-secondary btn-sm"
            >
              My Appointments
            </router-link>

            <router-link
              to="/patient/medicine-reminder"
              class="btn btn-outline-secondary btn-sm"
            >
              Medicine Reminder
            </router-link>

            <router-link
              to="/patient/emergency-sos"
              class="btn btn-outline-secondary btn-sm"
            >
              Emergency SOS
            </router-link>

            <router-link
              to="/patient/ai-health-assistant"
              class="btn btn-outline-secondary btn-sm"
            >
              AI Assistant
            </router-link>

            <router-link
              to="/patient/accessibility"
              class="btn btn-outline-secondary btn-sm"
            >
              Accessibility
            </router-link>

            <router-link
              to="/patient/health-card"
              class="btn btn-outline-secondary btn-sm"
            >
              Health Card
            </router-link>
          </div>

        </div>
      </div>

      <!-- Loading/Error -->
      <div
        v-if="loading"
        class="alert alert-info"
      >
        Loading dashboard...
      </div>

      <div
        v-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>

      <!-- Health Summary -->
      <div class="row g-3 mb-4">

        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <p class="text-muted mb-1">Health Score</p>
              <h3>{{ healthScore }}/100</h3>
              <p class="text-muted mb-0">
                A simple readiness score based on profile,
                appointments and reminders.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <p class="text-muted mb-1">Reminder Count</p>
              <h3>{{ reminderCount }}</h3>
              <p class="text-muted mb-0">
                Active medicine reminders.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <p class="text-muted mb-1">Emergency Ready</p>
              <h3>{{ emergencyReady ? 'Yes' : 'No' }}</h3>
              <p class="text-muted mb-0">
                Based on contacts and accessibility settings.
              </p>
            </div>
          </div>
        </div>

      </div>

      <!-- Upcoming Appointments -->
      <div class="card mb-4 shadow">

        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">My Upcoming Appointments</h5>
        </div>

        <div class="card-body">

          <div
            v-if="upcomingAppointments.length"
            class="table-responsive"
          >
            <table class="table table-bordered">

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
                <tr
                  v-for="app in upcomingAppointments"
                  :key="app.App_id"
                >
                  <td>{{ app.Date }}</td>
                  <td>{{ formatTime(app.Time) }}</td>
                  <td>{{ app.Doctor || '-' }}</td>

                  <td>
                    <span
                      class="badge"
                      :class="badgeClass(app.Status)"
                    >
                      {{ app.Status }}
                    </span>
                  </td>

                  <td>
                    <button
                      v-if="app.Status === 'Booked'"
                      class="btn btn-danger btn-sm"
                      @click="cancelAppointment(app.App_id)"
                    >
                      Cancel
                    </button>
                  </td>

                </tr>
              </tbody>

            </table>
          </div>

          <p v-else>
            No upcoming appointments found.
          </p>

        </div>
      </div>

      <!-- Treatment History -->
      <div class="card mb-4 shadow">

        <div class="card-header bg-secondary text-white">
          <h5 class="mb-0">Treatment History</h5>
        </div>

        <div class="card-body">

          <button
            class="btn btn-outline-primary btn-sm mb-3"
            :disabled="exporting"
            @click="startExport"
          >
            {{
              exporting
                ? 'Export in progress...'
                : 'Export Treatment History (CSV)'
            }}
          </button>

          <div
            v-if="treatmentHistory.length"
            class="table-responsive"
          >
            <table class="table table-bordered">

              <thead>
                <tr>
                  <th>Date</th>
                  <th>Doctor</th>
                  <th>Prescription</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="t in treatmentHistory"
                  :key="t.Treatment_id"
                >
                  <td>{{ t.Date }}</td>
                  <td>{{ t.Doctor }}</td>
                  <td>{{ t.Prescription || '-' }}</td>
                </tr>
              </tbody>

            </table>
          </div>

          <p v-else>
            No treatment history found.
          </p>

        </div>
      </div>

      <!-- Available Slots -->
      <div class="card mb-4 shadow">

        <div class="card-header bg-info text-dark">
          <h5 class="mb-0">
            Available Slots (Today + Next 7 Days)
          </h5>
        </div>

        <div class="card-body">

          <div class="row g-2 mb-3">

            <div class="col-md-5">
              <label class="form-label">
                Filter by Doctor
              </label>

              <select
                v-model="selectedDoctorId"
                class="form-select"
              >
                <option value="">
                  All doctors
                </option>

                <option
                  v-for="doc in doctors"
                  :key="doc.Doc_id"
                  :value="String(doc.Doc_id)"
                >
                  {{ doc.Name }}
                </option>
              </select>
            </div>

            <div class="col-md-4 d-flex align-items-end">
              <button
                class="btn btn-outline-primary w-100"
                @click="openDoctorProfile"
                :disabled="!selectedDoctorId"
              >
                Open Doctor Profile
              </button>
            </div>

          </div>

          <p v-if="!filteredSlots.length">
            No available slots right now.
          </p>

        </div>

      </div>

      <!-- Departments -->
      <div class="card shadow">

        <div class="card-header bg-secondary text-white">
          <h5 class="mb-0">Departments</h5>
        </div>

        <div class="card-body">

          <ul class="list-group">

            <li
              v-for="dep in departments"
              :key="dep.Dept_id"
              class="list-group-item"
            >
              {{ dep.Dept_name }}
            </li>

            <li
              v-if="!departments.length"
              class="list-group-item text-danger"
            >
              No departments found.
            </li>

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
      medicineReminders: [],
      emergencyContacts: [],
      accessibilitySettings: null,
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
    healthScore() {
      let score = 50
      score += Math.min(this.upcomingAppointments.length * 8, 20)
      score += Math.min(this.medicineReminders.length * 4, 15)
      score += Math.min(this.emergencyContacts.length * 3, 10)
      return Math.max(0, Math.min(100, score))
    },
    reminderCount() {
      return this.medicineReminders.length
    },
    emergencyReady() {
      return this.emergencyContacts.length > 0 && Boolean(this.accessibilitySettings)
    },
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
        const [dashboardResp, slotsResp, remindersResp, contactsResp, accessibilityResp] = await Promise.all([
          axios.get('http://127.0.0.1:5000/patient/dashboard', {
            headers: this.tokenHeaders(),
          }),
          axios.get('http://127.0.0.1:5000/patient/available-slots', {
            headers: this.tokenHeaders(),
          }),
          axios.get('http://127.0.0.1:5000/patient/medicine-reminders', {
            headers: this.tokenHeaders(),
          }),
          axios.get('http://127.0.0.1:5000/patient/emergency-contacts', {
            headers: this.tokenHeaders(),
          }),
          axios.get('http://127.0.0.1:5000/patient/accessibility-settings', {
            headers: this.tokenHeaders(),
          }).catch(() => ({ data: null })),
        ])

        this.upcomingAppointments = dashboardResp.data.upcoming_appointments || []
        this.treatmentHistory = dashboardResp.data.treatment_history || []
        this.doctors = dashboardResp.data.doctors || []
        this.departments = dashboardResp.data.departments || []
        this.availableSlots = this.normalizeAvailableSlotsResponse(slotsResp.data)
        this.medicineReminders = remindersResp.data?.reminders || []
        this.emergencyContacts = contactsResp.data?.contacts || []
        this.accessibilitySettings = accessibilityResp.data || null
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
/* ==========================
   PAGE
========================== */

.patient-page {
  min-height: 100vh;
  background: #f4f7fc;
  padding-bottom: 30px;
}

/* ==========================
   HEADER
========================== */

.dashboard-header {
  background: linear-gradient(135deg, #062b57, #0b4b94);
  color: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.logo-section img {
  border-radius: 50%;
  background: white;
  padding: 5px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.2);
}

/* ==========================
   BANNER
========================== */

.dashboard-banner {
  flex: 1;
}

.dashboard-banner h2 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: white;
}

.dashboard-banner p {
  margin-top: 6px;
  color: rgba(255,255,255,0.9);
  font-size: 0.95rem;
}

.action-section {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* ==========================
   MARQUEE
========================== */

.notice-bar {
  background: #062b57;
  color: white;
  padding: 10px;
  font-weight: 500;
  text-align: center;
}

/* ==========================
   CONTAINER
========================== */

.container {
  margin-top: 25px;
}

/* ==========================
   CARDS
========================== */

.card {
  border: none;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  background: white;
}

.card:hover {
  transform: translateY(-4px);
}

.card-body {
  color: #212529;
}

.card-body p,
.card-body span,
.card-body label,
.card-body li {
  color: #495057;
}

/* ==========================
   CARD HEADERS
========================== */

.card-header {
  border: none;
  font-weight: 600;
  padding: 15px 20px;
}

.bg-primary {
  background: linear-gradient(135deg, #0d6efd, #0b5ed7) !important;
}

.bg-secondary {
  background: linear-gradient(135deg, #6c757d, #495057) !important;
}

.bg-info {
  background: linear-gradient(135deg, #17a2b8, #0dcaf0) !important;
  color: white !important;
}

.department-header {
  background: linear-gradient(135deg, #062b57, #0b4b94);
  color: white;
}

/* ==========================
   QUICK ACCESS
========================== */

.router-link-active {
  font-weight: 600;
}

/* ==========================
   HEALTH CARDS
========================== */

.row .card h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #0b4b94;
}

.text-muted {
  color: #6c757d !important;
}

/* ==========================
   TABLES
========================== */

.table {
  margin-bottom: 0;
}

.table thead {
  background: #eef4ff;
}

.table th {
  color: #062b57 !important;
  font-weight: 700;
  border-bottom: 2px solid #dbe7ff;
}

.table td {
  color: #212529 !important;
  vertical-align: middle;
}

.table tbody tr:hover {
  background: #f8fbff;
}

/* ==========================
   BADGES
========================== */

.badge {
  padding: 8px 10px;
  font-size: 0.8rem;
  border-radius: 20px;
}

/* ==========================
   BUTTONS
========================== */

.btn {
  border-radius: 10px;
  font-weight: 600;
  transition: 0.3s;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  background: #0b4b94;
  border-color: #0b4b94;
}

.btn-primary:hover {
  background: #08366b;
  border-color: #08366b;
}

/* ==========================
   DROPDOWN
========================== */

.form-select {
  border-radius: 10px;
  padding: 10px;
  border: 1px solid #ced4da;
}

.form-label {
  color: #062b57;
  font-weight: 600;
}

/* ==========================
   LIST GROUP
========================== */

.list-group {
  border-radius: 10px;
  overflow: hidden;
}

.list-group-item {
  background: #ffffff;
  color: #062b57 !important;
  font-weight: 600;
  border: none;
  border-bottom: 1px solid #e5e7eb;
  padding: 15px 18px;
}

.list-group-item:last-child {
  border-bottom: none;
}

.list-group-item:hover {
  background: #f1f7ff;
}

/* ==========================
   ALERTS
========================== */

.alert {
  border-radius: 10px;
  font-weight: 500;
}

.alert-info {
  background: #e8f4fd;
  color: #0c5460;
}

.alert-danger {
  background: #fdeaea;
  color: #842029;
}

/* ==========================
   EMPTY DATA
========================== */

.card-body p {
  color: #495057 !important;
}

.no-data {
  text-align: center;
  color: #6c757d;
  padding: 20px;
  font-style: italic;
}

/* ==========================
   SCROLLBAR
========================== */

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #eef3fb;
}

::-webkit-scrollbar-thumb {
  background: #0b4b94;
  border-radius: 10px;
}

/* ==========================
   MOBILE
========================== */

@media (max-width: 768px) {

  .dashboard-header {
    flex-direction: column;
    text-align: center;
  }

  .dashboard-banner h2 {
    font-size: 1.5rem;
  }

  .dashboard-banner p {
    font-size: 0.9rem;
  }

  .action-section {
    width: 100%;
    justify-content: center;
  }

  .row .card h3 {
    font-size: 1.6rem;
  }

  .table {
    font-size: 0.9rem;
  }

  .btn {
    width: 100%;
  }
}
</style>

