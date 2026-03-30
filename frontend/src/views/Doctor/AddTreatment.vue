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

      <nav style="display: flex; gap: 20px">
        <button class="btn btn-outline-secondary" @click="goBack">Dashboard</button>
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </nav>
    </header>

    <marquee style="background-color: black; color: white">
      Record diagnosis and treatment so patient history stays accurate.
    </marquee>

    <div class="container py-4">
      <h3 class="mb-3">Add Treatment Details</h3>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="success" class="alert alert-success">{{ success }}</div>

      <div class="card shadow">
        <div class="card-body">
          <div class="mb-3">
            <label class="form-label">Appointment ID</label>
            <input class="form-control" :value="bookingId" disabled />
          </div>

          <div class="mb-3">
            <label class="form-label">Diagnosis</label>
            <input v-model="form.diagnosis" class="form-control" placeholder="Enter diagnosis" />
          </div>

          <div class="mb-3">
            <label class="form-label">Prescription</label>
            <input
              v-model="form.prescription"
              class="form-control"
              placeholder="Enter prescription"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Progress</label>
            <select v-model="form.progress" class="form-select">
              <option value="">Select progress</option>
              <option value="Improving">Improving</option>
              <option value="Stable">Stable</option>
              <option value="Critical">Critical</option>
              <option value="Recovered">Recovered</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Notes</label>
            <textarea
              v-model="form.notes"
              class="form-control"
              rows="4"
              placeholder="Additional clinical notes"
            ></textarea>
          </div>

          <button class="btn btn-success" :disabled="saving" @click="saveTreatment">
            {{ saving ? 'Saving...' : 'Save Treatment' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DoctorAddTreatment',
  data() {
    return {
      saving: false,
      error: '',
      success: '',
      form: {
        diagnosis: '',
        prescription: '',
        progress: '',
        notes: '',
      },
    }
  },
  computed: {
    bookingId() {
      return Number(this.$route.params.id)
    },
  },
  methods: {
    getToken() {
      return localStorage.getItem('access_token')
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    },
    goBack() {
      this.$router.push('/doctor/dashboard')
    },
    async saveTreatment() {
      this.error = ''
      this.success = ''

      if (!this.bookingId) {
        this.error = 'Invalid appointment id.'
        return
      }

      if (!this.form.diagnosis || !this.form.prescription || !this.form.progress) {
        this.error = 'Diagnosis, prescription and progress are required.'
        return
      }

      const token = this.getToken()
      if (!token) {
        this.$router.push('/login')
        return
      }

      this.saving = true
      try {
        const resp = await axios.post(
          `http://127.0.0.1:5000/doctor/add-treatment/${this.bookingId}`,
          this.form,
          { headers: { Authorization: `Bearer ${token}` } },
        )
        this.success = resp?.data?.message || 'Treatment saved successfully.'
      } catch (err) {
        console.error(err)
        this.error = err?.response?.data?.message || 'Failed to save treatment.'
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style scoped>
.doctor-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>
