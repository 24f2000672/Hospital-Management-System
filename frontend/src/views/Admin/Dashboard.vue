<template>
  <div class="admin-page">

    <!-- Navbar -->
    <header class="glass-navbar d-flex justify-content-between align-items-center px-4 py-3">

      <div class="d-flex align-items-center gap-3">
        <img src="@/assets/logo.png" height="70" width="70" alt="Logo" />
        <div>
          <h5 class="mb-0 text-white">HEALTH GUARDIAN+</h5>
          <small class="text-light">Admin Control Center</small>
        </div>
      </div>

      <button class="btn btn-outline-light" @click="logout">
        Logout
      </button>

    </header>

    <div class="container-fluid mt-4">

      <h1 class="dashboard-title mb-4">
        🏥 Admin Dashboard
      </h1>

      <!-- Metrics -->
      <div class="row mb-4">

        <div class="col-md-4">
          <div class="metric-card">
            <h2>{{ doctorCount }}</h2>
            <p>Total Doctors</p>
          </div>
        </div>

        <div class="col-md-4">
          <div class="metric-card">
            <h2>{{ patientCount }}</h2>
            <p>Total Patients</p>
          </div>
        </div>

        <div class="col-md-4">
          <div class="metric-card">
            <h2>{{ appointmentCount }}</h2>
            <p>Appointments</p>
          </div>
        </div>

      </div>

      <!-- Search -->
      <div class="glass-card mb-4">

        <form @submit.prevent="searchUser">

          <div class="input-group">

            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search Doctor or Patient"
            />

            <button class="btn btn-primary">
              Search
            </button>

          </div>

        </form>

      </div>

      <!-- Quick Actions -->

      <div class="glass-card mb-4">

        <h4 class="mb-3">⚡ Quick Actions</h4>

        <div class="d-flex flex-wrap gap-2">

          <router-link to="/admin/manage-doctors" class="btn btn-outline-light">
            Doctors
          </router-link>

          <router-link to="/admin/manage-patients" class="btn btn-outline-light">
            Patients
          </router-link>

          <router-link to="/admin/departments" class="btn btn-outline-light">
            Departments
          </router-link>

          <router-link to="/admin/analytics" class="btn btn-outline-light">
            Analytics
          </router-link>

          <router-link to="/admin/billing" class="btn btn-outline-light">
            Billing
          </router-link>

          <router-link to="/admin/rooms" class="btn btn-outline-light">
            Rooms
          </router-link>

          <router-link to="/admin/admissions" class="btn btn-outline-light">
            Admissions
          </router-link>

          <router-link to="/admin/emergency-monitor" class="btn btn-outline-light">
            Emergency
          </router-link>

        </div>

      </div>

      <!-- Doctors -->

      <div class="glass-card mb-4">

        <div class="d-flex justify-content-between">

          <h3>👨‍⚕️ Doctors</h3>

          <button
            class="btn btn-success"
            @click="addDoctor"
          >
            Add Doctor
          </button>

        </div>

        <div
          v-for="doctor in doctors"
          :key="doctor.id"
          class="user-card"
        >

          <div>
            <strong>
              {{ doctor.first_name }}
              {{ doctor.last_name }}
            </strong>
          </div>

          <div class="d-flex gap-2">

            <button
              class="btn btn-warning btn-sm"
              @click="updateDoctor(doctor)"
            >
              Update
            </button>

            <button
              class="btn btn-danger btn-sm"
              @click="removeDoctor(doctor)"
            >
              Remove
            </button>

          </div>

        </div>

      </div>

      <!-- Patients -->

      <div class="glass-card mb-4">

        <h3>🧑 Patients</h3>

        <div
          v-for="patient in patients"
          :key="patient.id"
          class="user-card"
        >

          <div>
            <strong>
              {{ patient.first_name }}
              {{ patient.last_name }}
            </strong>
          </div>

          <div class="d-flex gap-2">

            <button
              class="btn btn-warning btn-sm"
              @click="updatePatient(patient)"
            >
              Update
            </button>

            <button
              class="btn btn-danger btn-sm"
              @click="removePatient(patient)"
            >
              Remove
            </button>

          </div>

        </div>

      </div>

      <!-- Appointments -->

      <div class="glass-card">

        <h3>📅 Appointments</h3>

        <table class="table table-dark table-hover">

          <thead>
            <tr>
              <th>ID</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
              <th>Doctor</th>
              <th>Patient</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="a in availableAppointments"
              :key="a.id"
            >

              <td>{{ a.id }}</td>
              <td>{{ a.date }}</td>
              <td>{{ a.time }}</td>
              <td>{{ a.status }}</td>
              <td>{{ a.doctor_name }}</td>
              <td>{{ a.patient_name }}</td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',

  data() {
    return {
      doctors: [],
      patients: [],
      availableAppointments: [],
      pastAppointments: [],
      doctorCount: 0,
      patientCount: 0,
      appointmentCount: 0,
      searchQuery: '',
    }
  },

  async mounted() {
    const token = localStorage.getItem('access_token')

    if (!token) {
      console.error('No access token found')
      alert('Session expired. Please login again.')
      this.$router.push('/login')
      return
    }

    try {
      const response = await axios.get('http://127.0.0.1:5000/admin/dashboard', {
        headers: { Authorization: `Bearer ${token}` },
      })

      this.doctors = response.data.doctors || []
      this.patients = response.data.patients || []
      this.availableAppointments = response.data.available_appointments || []
      this.pastAppointments = response.data.past_appointments || []

      this.doctorCount = response.data.doctor_count || 0
      this.patientCount = response.data.patient_count || 0
      this.appointmentCount = response.data.appointment_count || 0
    } catch (error) {
      console.error('Admin Dashboard Error:', error)

      if (error.response) {
        console.error('Status:', error.response.status)
        console.error('Data:', error.response.data)

        if (error.response.status === 401) {
          alert('Unauthorized. Please login again.')
          localStorage.removeItem('access_token')
          this.$router.push('/login')
        } else if (error.response.status === 403) {
          alert('You do not have admin access.')
          this.$router.push('/')
        }
      }
    }
  },

  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    searchUser() {
      if (this.searchQuery.trim()) {
        this.$router.push({ path: '/admin/search', query: { query: this.searchQuery } })
      }
    },
    addDoctor() {
      // navigate to the Add Doctor view defined in the router
      this.$router.push({ name: 'admin-doctors' })
    },
    updateDoctor(doctor) {
      // Navigate to update doctor details page
      this.$router.push(`/admin/update-doctor?id=${doctor.id}`)
    },
    removeDoctor(doctor) {
      if (
        confirm(`Are you sure you want to remove doctor ${doctor.first_name} ${doctor.last_name}?`)
      ) {
        // Call API to remove doctor
        axios
          .delete(`http://127.0.0.1:5000/delete_doctor/${doctor.id}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
          })
          .then(() => {
            alert('Doctor removed successfully')
            // Refresh the dashboard
            location.reload()
          })
          .catch((error) => {
            console.error('Error removing doctor:', error)
            alert('Failed to remove doctor')
          })
      }
    },
    toggleBlacklistDoctor(doctor) {
      const action = doctor.is_blacklisted ? 'unblacklist' : 'blacklist'
      const message = doctor.is_blacklisted
        ? `Are you sure you want to unblacklist doctor ${doctor.first_name} ${doctor.last_name}?`
        : `Are you sure you want to blacklist doctor ${doctor.first_name} ${doctor.last_name}?`

      if (confirm(message)) {
        const endpoint = doctor.is_blacklisted
          ? `http://127.0.0.1:5000/remove_blacklist_doctor/${doctor.id}`
          : `http://127.0.0.1:5000/blacklist_doctor/${doctor.id}`

        axios
          .post(
            endpoint,
            {},
            {
              headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
            },
          )
          .then(() => {
            alert(`Doctor ${action}ed successfully`)
            // Toggle the status locally
            doctor.is_blacklisted = !doctor.is_blacklisted
          })
          .catch((error) => {
            console.error(`Error ${action}ing doctor:`, error)
            alert(`Failed to ${action} doctor`)
          })
      }
    },
    updatePatient(patient) {
      // Navigate to update patient details page
      this.$router.push(`/admin/update-patient?id=${patient.id}`)
    },
    removePatient(patient) {
      if (
        confirm(
          `Are you sure you want to remove patient ${patient.first_name} ${patient.last_name}?`,
        )
      ) {
        // Call API to remove patient
        axios
          .delete(`http://127.0.0.1:5000/delete_patient/${patient.id}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
          })
          .then(() => {
            alert('Patient removed successfully')
            // Refresh the dashboard
            location.reload()
          })
          .catch((error) => {
            console.error('Error removing patient:', error)
            alert('Failed to remove patient')
          })
      }
    },
    toggleBlacklistPatient(patient) {
      const action = patient.is_blacklisted ? 'unblacklist' : 'blacklist'
      const message = patient.is_blacklisted
        ? `Are you sure you want to unblacklist patient ${patient.first_name} ${patient.last_name}?`
        : `Are you sure you want to blacklist patient ${patient.first_name} ${patient.last_name}?`

      if (confirm(message)) {
        const endpoint = patient.is_blacklisted
          ? `http://127.0.0.1:5000/remove_blacklist_patient/${patient.id}`
          : `http://127.0.0.1:5000/blacklist_patient/${patient.id}`

        axios
          .post(
            endpoint,
            {},
            {
              headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
            },
          )
          .then(() => {
            alert(`Patient ${action}ed successfully`)
            // Toggle the status locally
            patient.is_blacklisted = !patient.is_blacklisted
          })
          .catch((error) => {
            console.error(`Error ${action}ing patient:`, error)
            alert(`Failed to ${action} patient`)
          })
      }
    },
  },
}
</script>

<style scoped>

.admin-page {
  min-height: 100vh;
  background: linear-gradient(
    135deg,
    #021b3a,
    #032d5a,
    #061a33
  );
  color: white;
}

.glass-navbar {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.15);
}

.dashboard-title {
  font-weight: bold;
}

.glass-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  padding: 20px;
}

.metric-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 25px;
  text-align: center;
}

.metric-card h2 {
  font-size: 2rem;
  font-weight: bold;
}

.user-card {
  display: flex;
  justify-content: space-between;
  align-items: center;

  background: rgba(255,255,255,0.05);

  border-radius: 12px;
  padding: 15px;
  margin-top: 10px;
}

.table {
  color: white;
}

</style>
