<template>
  <div
    style="
      background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
      min-height: 100vh;
    "
  >
    <!-- HEADER -->
    <header
      class="navbar d-flex align-items-center justify-content-between shadow px-4"
      style="background: white"
    >
      <div>
        <img src="@/assets/logo.png" height="70" width="70" />
      </div>

      <div class="text-center">
        <h1>Vardha Hospital</h1>
      </div>

      <div>
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </div>
    </header>

    <marquee style="background: black; color: white; padding: 5px">
      Every patient you heal is a story of hope — thank you for being the heart of care.
    </marquee>

    <div class="container mt-4">
      <h2 class="text-center mb-4">Welcome Doctor</h2>

      <!-- TODAY APPOINTMENTS -->
      <div class="card shadow mb-4">
        <div class="card-header bg-primary text-white">
          <h4>Today's Appointments</h4>
        </div>

        <div class="card-body">
          <ul v-if="todaysAppointments.length" class="list-group">
            <li
              v-for="a in todaysAppointments"
              :key="a.id"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <strong>{{ a.time }}</strong> — <strong>Patient:</strong> {{ a.patient_name }}
              </div>

              <div>
                <button
                  class="btn btn-success btn-sm me-2"
                  @click="updateStatus(a.id, 'Completed')"
                >
                  Complete
                </button>

                <button class="btn btn-danger btn-sm" @click="updateStatus(a.id, 'Cancelled')">
                  Cancel
                </button>
              </div>
            </li>
          </ul>

          <p v-else>No appointments scheduled for today.</p>
        </div>
      </div>

      <!-- UPCOMING -->
      <div class="card shadow mb-4">
        <div class="card-header bg-warning">
          <h4>Upcoming Appointments (Next 7 Days)</h4>
        </div>

        <div class="card-body">
          <ul v-if="upcomingAppointments.length" class="list-group">
            <li
              v-for="a in upcomingAppointments"
              :key="a.id"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <strong>Date:</strong> {{ a.date }} | <strong>Time:</strong> {{ a.time }} —
                <strong>Patient:</strong> {{ a.patient_name }}
              </div>

              <div>
                <button
                  class="btn btn-success btn-sm me-2"
                  @click="updateStatus(a.id, 'Completed')"
                >
                  Complete
                </button>

                <button class="btn btn-danger btn-sm" @click="updateStatus(a.id, 'Cancelled')">
                  Cancel
                </button>
              </div>
            </li>
          </ul>

          <p v-else>No upcoming appointments.</p>
        </div>
      </div>

      <!-- PAST -->
      <div class="card shadow mb-4">
        <div class="card-header bg-secondary text-white">
          <h4>Past Appointments</h4>
        </div>

        <div class="card-body">
          <ul v-if="pastAppointments.length" class="list-group">
            <li
              v-for="a in pastAppointments"
              :key="a.id"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <strong>{{ a.date }}</strong> | <strong>{{ a.time }}</strong> —
                <strong>Patient:</strong> {{ a.patient_name }}
              </div>

              <div class="d-flex gap-2">
                <button class="btn btn-info btn-sm" @click="addTreatment(a.id)">
                  Add Treatment
                </button>

                <button class="btn btn-danger btn-sm" @click="updateStatus(a.id, 'Cancelled')">
                  Cancel
                </button>
              </div>
            </li>
          </ul>

          <p v-else>No past appointments.</p>
        </div>
      </div>

      <!-- PATIENTS -->
      <div class="card shadow mb-4">
        <div class="card-header bg-dark text-white">
          <h4>My Patients</h4>
        </div>

        <div class="card-body">
          <ul v-if="patients.length" class="list-group">
            <li
              v-for="p in patients"
              :key="p.id"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <strong>{{ p.first_name }} {{ p.last_name }}</strong>
                — {{ p.email }}
              </div>

              <button class="btn btn-primary btn-sm" @click="viewHistory(p.id)">
                View History
              </button>
            </li>
          </ul>

          <p v-else>No patients assigned yet.</p>
        </div>
      </div>

      <!-- SLOT REMINDER -->
      <div class="card shadow mb-4">
        <div class="card-header bg-success text-white">
          <h4>Slot Availability Reminder</h4>
        </div>

        <div class="card-body">
          <div v-if="missingDates.length">
            <p>You haven't added slots for:</p>

            <ul>
              <li v-for="d in missingDates" :key="d">
                {{ d }}
              </li>
            </ul>

            <router-link to="/doctor/manage-slots" class="btn btn-primary">
              Manage Slots
            </router-link>
          </div>

          <div v-else>
            <p class="text-success fw-bold">✅ All slots created for the next 7 days.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      todaysAppointments: [],
      upcomingAppointments: [],
      pastAppointments: [],
      patients: [],
      slots: [],
      missingDates: [],
    }
  },

  methods: {
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/')
    },

    getToken() {
      const token = localStorage.getItem('access_token')

      if (!token) {
        this.$router.push('/')
        return null
      }

      return token
    },

    async fetchDashboard() {
      try {
        const token = this.getToken()
        if (!token) return

        const res = await axios.get('http://127.0.0.1:5000/doctor/dashboard', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        this.todaysAppointments = res.data.todays || []
        this.upcomingAppointments = res.data.upcoming || []
        this.pastAppointments = res.data.past || []
        this.patients = res.data.patients || []
      } catch (err) {
        console.log('Dashboard error:', err.response?.data || err)
      }
    },

    async fetchSlots() {
      try {
        const token = this.getToken()
        if (!token) return

        const res = await axios.get('http://127.0.0.1:5000/manage_slots', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        // ✅ Ensure slots is always an array
        if (Array.isArray(res.data.slots)) {
          this.slots = res.data.slots
        } else {
          this.slots = []
        }

        this.calculateMissingDates()
      } catch (err) {
        console.log('Fetch slots error:', err.response?.data || err)
        this.slots = []
      }
    },

    calculateMissingDates() {
      const today = new Date()
      let next7 = []

      for (let i = 0; i < 7; i++) {
        let d = new Date()
        d.setDate(today.getDate() + i)

        next7.push(d.toISOString().split('T')[0])
      }

      // ✅ protect against map error
      const slotDates = (this.slots || []).map((s) => new Date(s.date).toISOString().split('T')[0])

      this.missingDates = next7.filter((d) => !slotDates.includes(d))
    },

    async updateStatus(id, status) {
      try {
        const token = this.getToken()
        if (!token) return

        await axios.put(
          `http://127.0.0.1:5000/appointment/${id}/${status}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )

        this.fetchDashboard()
      } catch (err) {
        console.log('Update error:', err.response?.data || err)
      }
    },

    addTreatment(id) {
      this.$router.push(`/doctor/treatment/${id}`)
    },

    viewHistory(id) {
      this.$router.push(`/patient/history/${id}`)
    },
  },

  mounted() {
    this.fetchDashboard()
    this.fetchSlots()
  },
}
</script>
