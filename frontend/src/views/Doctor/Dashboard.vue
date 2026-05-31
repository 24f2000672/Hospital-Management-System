<template>
  <div class="doctor-page">
    
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

      <nav style="display: flex; gap: 30px">
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </nav>
    </header>

    <marquee style="background-color: black; color: white">
      Every patient you heal is a story of hope — thank you for being the heart of care.
    </marquee>

    <div class="container mt-5">
      <h2 class="mb-4">👨‍⚕️ Doctor Dashboard</h2>

      <div class="card shadow-sm mb-4">
        <div class="card-body d-flex flex-wrap gap-2">
          <button class="btn btn-outline-secondary btn-sm" @click="manageSlots">Manage Slots</button>
          <router-link to="/doctor/patient-history" class="btn btn-outline-secondary btn-sm">Patient History</router-link>
          <router-link to="/doctor/monthly-reports" class="btn btn-outline-secondary btn-sm">Monthly Reports</router-link>
          <router-link to="/doctor/telemedicine" class="btn btn-outline-secondary btn-sm">Telemedicine</router-link>
        </div>
      </div>

      <!-- Today's Appointments -->
      <div class="card mb-4 shadow">
        <div class="card-header bg-primary text-white">
          <h4>Today's Appointments</h4>
        </div>
        <div class="card-body">
          <template v-if="todaysAppointments.length">
            <ul class="list-group">
              <li
                v-for="appt in todaysAppointments"
                :key="appt.App_id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <strong>{{ formatTime(appt.Time) }}</strong> — <strong>Patient:</strong>
                  {{ appt.patient_name }}
                </div>

                <div>
                  <button
                    class="btn btn-success btn-sm"
                    @click="changeStatus(appt.App_id, 'Completed')"
                  >
                    Complete
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    @click="changeStatus(appt.App_id, 'Cancelled')"
                  >
                    Cancel
                  </button>
                </div>
              </li>
            </ul>
          </template>
          <p v-else>No appointments scheduled for today.</p>
        </div>
      </div>

      <!-- Upcoming Appointments -->
      <div class="card mb-4 shadow">
        <div class="card-header bg-warning text-dark">
          <h4 class="mb-0">Upcoming Appointments (Next 7 Days)</h4>
        </div>
        <div class="card-body">
          <template v-if="upcomingAppointments.length">
            <ul class="list-group">
              <li
                v-for="appt in upcomingAppointments"
                :key="appt.App_id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <strong>Date:</strong> {{ appt.Date }} | <strong>Time:</strong>
                  {{ formatTime(appt.Time) }} — <strong>Patient:</strong> {{ appt.patient_name }}
                </div>

                <div>
                  <button
                    class="btn btn-success btn-sm"
                    @click="changeStatus(appt.App_id, 'Completed')"
                  >
                    Complete
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    @click="changeStatus(appt.App_id, 'Cancelled')"
                  >
                    Cancel
                  </button>
                </div>
              </li>
            </ul>
          </template>
          <p v-else>No upcoming appointments.</p>
        </div>
      </div>

      <!-- Past Appointments -->
      <div class="card mb-4 shadow">
        <div class="card-header bg-secondary text-white">
          <h4>Past Appointments</h4>
        </div>
        <div class="card-body">
          <template v-if="pastAppointments.length">
            <ul class="list-group">
              <li
                v-for="appt in pastAppointments"
                :key="appt.App_id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <strong>{{ appt.Date }}</strong> | <strong>{{ formatTime(appt.Time) }}</strong> —
                  <strong>Patient:</strong> {{ appt.patient_name }}
                </div>

                <div class="d-flex gap-2">
                  <button class="btn btn-info btn-sm" @click="addTreatment(appt.App_id)">
                    Add Treatment Details
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    @click="changeStatus(appt.App_id, 'Cancelled')"
                  >
                    Cancel
                  </button>
                </div>
              </li>
            </ul>
          </template>
          <p v-else>No past appointments found.</p>
        </div>
      </div>

      <!-- Assigned Patients -->
      <div class="card mb-4 shadow">
        <div class="card-header bg-dark text-white">
          <h4>My Patients</h4>
        </div>
        <div class="card-body">
          <template v-if="assignedPatients.length">
            <ul class="list-group">
              <li
                v-for="p in assignedPatients"
                :key="p.Pat_id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <strong>{{ p.First_Name }} {{ p.Last_Name }}</strong> — {{ p.Email }}
                </div>
                <button class="btn btn-primary btn-sm" @click="viewHistory(p.Pat_id)">
                  View History
                </button>
              </li>
            </ul>
          </template>
          <p v-else>No patients assigned yet.</p>
        </div>
      </div>

      
      <div class="card shadow mb-4">
        <div class="card-header bg-success text-white">
          <h4>Slot Availability Reminder</h4>
        </div>
        <div class="card-body">
          <template v-if="missingDates.length">
            <p>You haven't added slots for:</p>
            <ul>
              <li v-for="day in missingDates" :key="day">{{ day }}</li>
            </ul>
            <button class="btn btn-primary" @click="manageSlots">Manage Slots</button>
          </template>
          <p v-else class="text-success">All slots created for next week.</p>
        </div>
      </div>

      
      <div class="card shadow mb-4">
        <div class="card-header bg-info text-white d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Monthly Reports</h4>
          <small>Auto job runs on 1st of every month</small>
        </div>
        <div class="card-body">
          <div class="row g-2 align-items-end mb-3">
            <div class="col-md-4">
              <label class="form-label">Report Month</label>
              <input v-model="reportMonth" type="month" class="form-control" />
            </div>
            <div class="col-md-4">
              <button class="btn btn-primary" :disabled="exportingReport" @click="generateMonthlyReport">
                {{ exportingReport ? 'Generating...' : 'Export Report' }}
              </button>
            </div>
          </div>

          <p v-if="reportMessage" class="text-success mb-3">{{ reportMessage }}</p>

          <template v-if="monthlyReports.length">
            <ul class="list-group">
              <li
                v-for="report in monthlyReports"
                :key="report.month"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <strong>{{ formatMonth(report.month) }}</strong>
                  <div class="small text-muted">Generated: {{ formatDateTime(report.generated_at) }}</div>
                </div>
                <button class="btn btn-outline-primary btn-sm" @click="downloadMonthlyReport(report.month)">
                  Download HTML
                </button>
              </li>
            </ul>
          </template>
          <p v-else class="mb-0">No monthly reports yet. Export one to get started.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DoctorDashboard',
  data() {
    return {
      todaysAppointments: [],
      upcomingAppointments: [],
      pastAppointments: [],
      assignedPatients: [],
      missingDates: [],
      docId: null,
      reportMonth: '',
      monthlyReports: [],
      exportingReport: false,
      reportMessage: '',
    }
  },
  methods: {
    formatTime(t) {
      return t ? t.slice(0, 5) : ''
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    },
    getDefaultReportMonth() {
      const now = new Date()
      now.setDate(1)
      now.setMonth(now.getMonth() - 1)
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      return `${year}-${month}`
    },
    formatMonth(monthLabel) {
      const [year, month] = monthLabel.split('-')
      const d = new Date(Number(year), Number(month) - 1, 1)
      return d.toLocaleString(undefined, { month: 'long', year: 'numeric' })
    },
    formatDateTime(value) {
      if (!value) return '-'
      const d = new Date(value)
      if (Number.isNaN(d.getTime())) return value
      return d.toLocaleString()
    },
    async loadDashboard() {
      const token = localStorage.getItem('access_token')
      if (!token) {
        alert('Session expired. Please login again.')
        this.$router.push('/login')
        return
      }
      try {
        const resp = await axios.get('http://127.0.0.1:5000/doctor/dashboard', {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.todaysAppointments = (resp.data.todays_appointments || []).map((appt) => ({
          ...appt,
          patient_name: appt.patient_name || appt.Patient_Name || '',
        }))
        this.upcomingAppointments = (resp.data.upcoming_appointments || []).map((appt) => ({
          ...appt,
          patient_name: appt.patient_name || appt.Patient_Name || '',
        }))
        this.pastAppointments = (resp.data.past_appointments || []).map((appt) => ({
          ...appt,
          patient_name: appt.patient_name || appt.Patient_Name || '',
        }))
        this.assignedPatients = (resp.data.assigned_patients || []).map((p) => ({
          ...p,
          First_Name: p.First_Name || (p.Name ? p.Name.split(' ')[0] : ''),
          Last_Name: p.Last_Name || (p.Name ? p.Name.split(' ').slice(1).join(' ') : ''),
          Email: p.Email || p.email || '',
        }))
        this.missingDates =
          resp.data.missing_dates || resp.data.missing_availability_dates || []
        this.docId = resp.data.doc_id || null
      } catch (err) {
        console.error(err)
        alert('Unable to load dashboard data.')
      }
    },
    async loadMonthlyReports() {
      try {
        const token = localStorage.getItem('access_token')
        const resp = await axios.get('http://127.0.0.1:5000/doctor/monthly-reports', {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.monthlyReports = resp.data.reports || []
      } catch (err) {
        console.error(err)
      }
    },
    async generateMonthlyReport() {
      try {
        this.exportingReport = true
        this.reportMessage = ''
        const token = localStorage.getItem('access_token')
        const month = this.reportMonth || this.getDefaultReportMonth()
        const resp = await axios.post(
          'http://127.0.0.1:5000/doctor/monthly-reports',
          { month },
          { headers: { Authorization: `Bearer ${token}` } },
        )
        this.reportMessage = `Report for ${this.formatMonth(resp.data.month)} is ready.`
        await this.loadMonthlyReports()
      } catch (err) {
        console.error(err)
        const backendMsg = err?.response?.data?.message
        alert(backendMsg || 'Failed to generate monthly report.')
      } finally {
        this.exportingReport = false
      }
    },
    async downloadMonthlyReport(month) {
      try {
        const token = localStorage.getItem('access_token')
        const resp = await axios.get(
          `http://127.0.0.1:5000/doctor/monthly-reports/${month}/download`,
          {
            headers: { Authorization: `Bearer ${token}` },
            responseType: 'blob',
          },
        )

        const url = window.URL.createObjectURL(new Blob([resp.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `doctor_report_${month}.html`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
      } catch (err) {
        console.error(err)
        const backendMsg = err?.response?.data?.message
        alert(backendMsg || 'Unable to download report.')
      }
    },
    async changeStatus(appId, status) {
      try {
        const token = localStorage.getItem('access_token')
        await axios.post(
          `http://127.0.0.1:5000/update_status/${appId}`,
          { status },
          { headers: { Authorization: `Bearer ${token}` } },
        )
        await this.loadDashboard()
      } catch (err) {
        console.error(err)
        const backendMsg = err?.response?.data?.message
        alert(backendMsg || 'Failed to update appointment status.')
      }
    },
    addTreatment(appId) {
      this.$router.push({ name: 'doctor-treatment', params: { id: appId } })
    },
    viewHistory(patId) {
      this.$router.push({ name: 'patient-history', params: { id: patId } })
    },
    manageSlots() {
      if (this.docId) {
        this.$router.push({ name: 'doctor-manage-slots', params: { doc_id: this.docId } })
      }
    },
  },
  mounted() {
    this.reportMonth = this.getDefaultReportMonth()
    this.loadDashboard()
    this.loadMonthlyReports()
  },
}
</script>

<style scoped>
.doctor-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>
