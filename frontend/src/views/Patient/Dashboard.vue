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
        this.availableSlots = slotsResp.data.available_slots || []
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
  },
  mounted() {
    this.loadDashboard()
  },
}
</script>

<style scoped>
.patient-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>

