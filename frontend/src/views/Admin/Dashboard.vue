<template>
  <div class="admin-page">
    <!-- Header -->
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
        <b>
          <button class="btn btn-outline-danger" @click="logout">Logout</button>
        </b>
      </nav>
    </header>

    <!-- Marquee -->
    <marquee style="background-color: black; color: white">
      Welcome Admin, Behind every successful hospital is an admin team that cares as deeply as the
      doctors heal.
    </marquee>

    <div class="container mt-5">
      <h2 class="mb-4">🏥 Vardha Hospital - Admin Dashboard</h2>

      <div class="card shadow-sm mb-4">
        <div class="card-body d-flex flex-wrap gap-2">
          <router-link to="/admin/manage-doctors" class="btn btn-outline-secondary btn-sm">Manage Doctors</router-link>
          <router-link to="/admin/manage-patients" class="btn btn-outline-secondary btn-sm">Manage Patients</router-link>
          <router-link to="/admin/departments" class="btn btn-outline-secondary btn-sm">Departments</router-link>
          <router-link to="/admin/analytics" class="btn btn-outline-secondary btn-sm">Analytics</router-link>
          <router-link to="/admin/emergency-monitor" class="btn btn-outline-secondary btn-sm">Emergency Monitor</router-link>
          <router-link to="/admin/rooms" class="btn btn-outline-secondary btn-sm">Rooms</router-link>
          <router-link to="/admin/admissions" class="btn btn-outline-secondary btn-sm">Admissions</router-link>
          <router-link to="/admin/billing" class="btn btn-outline-secondary btn-sm">Billing</router-link>
          <router-link to="/admin/appointments" class="btn btn-outline-secondary btn-sm">Appointments</router-link>
        </div>
      </div>

      <!-- 🔎 Search -->
      <form @submit.prevent="searchUser" class="d-flex justify-content-center">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control w-50 me-2"
          placeholder="Search Doctor or Patient"
          required
        />
        <button type="submit" class="btn btn-primary">Search</button>
      </form>

      <br />

      <!-- Counts -->
      <div class="card p-4 shadow-sm">
        <h4 class="border p-2 text-success">Total Doctors: {{ doctorCount }}</h4>
        <h4 class="border p-2 text-danger">Total Patients: {{ patientCount }}</h4>
        <h4 class="border p-2 text-primary">Total Appointments: {{ appointmentCount }}</h4>
      </div>

      <!-- Doctors -->
      <div class="mt-4">
        <h3>Doctors available are:</h3>
        <div class="doctor-list">
          <div v-for="d in doctors" :key="d.id" class="doctor-card">
            <div class="doctor-info">
              <strong>{{ d.first_name }} {{ d.last_name }}</strong> (ID: {{ d.id }})
            </div>
            <div class="action-buttons">
              <button class="btn btn-sm btn-warning" @click="updateDoctor(d)">Update</button>
              <button class="btn btn-sm btn-danger" @click="removeDoctor(d)">Remove</button>
              <button
                class="btn btn-sm"
                :class="d.is_blacklisted ? 'btn-success' : 'btn-dark'"
                @click="toggleBlacklistDoctor(d)"
              >
                {{ d.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <hr />
      <button class="btn btn-primary mt-3" @click="addDoctor">✚ Add New Doctor</button>
      <hr />

      <!-- Patients -->
      <div class="mt-4">
        <h3>Patients available are:</h3>
        <div class="patient-list">
          <div v-for="p in patients" :key="p.id" class="patient-card">
            <div class="patient-info">
              <strong>{{ p.first_name }} {{ p.last_name }}</strong> (ID: {{ p.id }})
            </div>
            <div class="action-buttons">
              <button class="btn btn-sm btn-warning" @click="updatePatient(p)">Update</button>
              <button class="btn btn-sm btn-danger" @click="removePatient(p)">Remove</button>
              <button
                class="btn btn-sm"
                :class="p.is_blacklisted ? 'btn-success' : 'btn-dark'"
                @click="toggleBlacklistPatient(p)"
              >
                {{ p.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <hr />

      <!-- Upcoming Appointments -->
      <h3 class="mt-4">Upcoming / Available Appointments</h3>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>App ID</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Doctor</th>
            <th>Patient</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="a in availableAppointments" :key="a.id">
            <td>{{ a.id }}</td>
            <td>{{ a.date }}</td>
            <td>{{ a.time }}</td>
            <td>{{ a.status }}</td>
            <td>{{ a.doctor_name }}</td>
            <td>{{ a.patient_name }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Past Appointments -->
      <h3 class="mt-5">Past Appointments</h3>
      <table class="table table-bordered table-hover">
        <thead>
          <tr>
            <th>App ID</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Doctor</th>
            <th>Patient</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="a in pastAppointments" :key="a.id">
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

<style>
.admin-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}

.doctor-list,
.patient-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.doctor-card,
.patient-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.doctor-info,
.patient-info {
  flex: 1;
  font-size: 15px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
}
</style>
