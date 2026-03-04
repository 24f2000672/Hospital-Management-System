<template>
  <div class="doctor-page">
    <!-- Header (same style as admin for consistency) -->
    <header
      style="background-color: white"
      class="navbar d-flex justify-content-between align-items-center px-4">
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

      <!-- Today's Appointments -->
      <div class="card mb-4 shadow">
        <div class="card-header bg-primary text-white">
          <h4>Today's Appointments</h4>
        </div>
        <div class="card-body">
          <template v-if="todaysAppointments.length">
            <ul class="list-group">
              <li v-for="appt in todaysAppointments":key="appt.App_id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ formatTime(appt.Time) }}</strong> —
                  <strong>Patient:</strong> {{ appt.patient_name }}
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
                  <strong>Date:</strong> {{ appt.Date }} |
                  <strong>Time:</strong> {{ formatTime(appt.Time) }} —
                  <strong>Patient:</strong> {{ appt.patient_name }}
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
                  <strong>{{ appt.Date }}</strong> |
                  <strong>{{ formatTime(appt.Time) }}</strong> —
                  <strong>Patient:</strong> {{ appt.patient_name }}
                </div>

                <div class="d-flex gap-2">
                  <button
                    class="btn btn-info btn-sm"
                    @click="addTreatment(appt.App_id)"
                  >
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
                <button
                  class="btn btn-primary btn-sm"
                  @click="viewHistory(p.Pat_id)"
                >
                  View History
                </button>
              </li>
            </ul>
          </template>
          <p v-else>No patients assigned yet.</p>
        </div>
      </div>

      <!-- Slot Availability Reminder -->
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
    }
  },
  methods: {
    formatTime(t) {
      return t ? t.slice(0,5) : ''
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
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
        this.todaysAppointments = resp.data.todays_appointments || []
        this.upcomingAppointments = resp.data.upcoming_appointments || []
        this.pastAppointments = resp.data.past_appointments || []
        this.assignedPatients = resp.data.assigned_patients || []
        this.missingDates = resp.data.missing_dates || []
        this.docId = resp.data.doc_id || null
      } catch (err) {
        console.error(err)
        alert('Unable to load dashboard data.')
      }
    },
    async changeStatus(appId, status) {
      try {
        const token = localStorage.getItem('access_token')
        await axios.post(
          `http://127.0.0.1:5000/update_status/${appId}`,
          { status },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.loadDashboard()
      } catch (err) {
        console.error(err)
        alert('Failed to update appointment status.')
      }
    },
    addTreatment(appId) {
      this.$router.push({ name: 'AddTreatment', params: { booking_id: appId } })
    },
    viewHistory(patId) {
      this.$router.push({ name: 'PatientHistory', params: { pat_id: patId } })
    },
    manageSlots() {
      if (this.docId) {
        this.$router.push({ name: 'ManageSlots', params: { doc_id: this.docId } })
      }
    },
  },
  mounted() {
    this.loadDashboard()
  },
}
</script>

<style scoped>
.doctor-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>