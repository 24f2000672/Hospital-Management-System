<template>
  <div
    style="
      background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
      min-height: 100vh;
    "
  >
    <!-- Navbar -->
    <nav style="background-color: white" class="navbar d-flex align-items-center">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
          <img src="@/assets/logo.png" height="70" width="70" />
        </div>
        <div>
          <h1 class="text-center">Vardha Hospital</h1>
        </div>
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </div>
    </nav>

    <marquee style="background-color: black; color: white">
      Every patient you heal is a story of hope — thank you for being the heart of care.
    </marquee>

    <div class="container mt-3" v-if="flashMessage">
      <div class="alert alert-info alert-dismissible fade show">
        {{ flashMessage }}
        <button class="btn-close" @click="flashMessage = null"></button>
      </div>
    </div>

    <div v-if="loading" class="text-center mt-5">
      <h4>Loading slots...</h4>
    </div>

    <div v-else class="container mt-3">
      <h3 class="text-center mb-4">Manage Appointment Slots</h3>

      <form @submit.prevent="updateSlots">
        <div v-for="day in dates" :key="day" class="card mb-3">
          <div class="card-header bg-primary text-white">
            {{ formatDate(day) }}
          </div>

          <div class="card-body d-flex flex-wrap gap-2">
            <div
              v-for="slot in slots[day]"
              :key="slot.time_key"
              class="slot-box p-2 text-center"
              :class="{
                booked: slot.status === 'Booked',
                available: slot.status === 'Available',
                notcreated: slot.status === 'Not Created',
              }"
            >
              <div v-if="slot.status === 'Booked'">
                {{ slot.label }}
                <span class="badge bg-success ms-1">Booked</span>
                <button
                  type="button"
                  class="btn btn-sm btn-outline-danger mt-1"
                  @click="cancelSlot(day, slot.time_key)"
                >
                  Cancel
                </button>
              </div>

              <div v-else-if="slot.status === 'Available'">
                {{ slot.label }}
                <span class="badge bg-primary ms-1">Available</span>
              </div>

              <div v-else>
                <input
                  type="checkbox"
                  class="form-check-input me-1"
                  :value="`${day}|${slot.time_key}`"
                  v-model="selectedSlots"
                />
                {{ slot.label }}
                <span class="badge bg-secondary ms-1">Not Created</span>
              </div>
            </div>
          </div>
        </div>

        <div class="text-center mb-4 mt-3">
          <button class="btn btn-info" :disabled="!selectedSlots.length">Add Selected Slots</button>
          <button type="button" class="btn btn-secondary ms-2" @click="goDashboard">
            Return to Dashboard
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ManageSlots',
  data() {
    return {
      dates: [],
      slots: {},
      selectedSlots: [],
      flashMessage: null,
      loading: false,
    }
  },
  mounted() {
    this.fetchSlots()
  },
  methods: {
    formatDate(date) {
      return new Date(date).toDateString()
    },
    getToken() {
      const token = localStorage.getItem('access_token')
      if (!token) {
        alert('Session expired. Please login again.')
        this.$router.push('/login')
        return null
      }
      return token
    },
    async fetchSlots() {
      this.loading = true
      try {
        const token = this.getToken()
        if (!token) return

        const res = await axios.get('http://127.0.0.1:5000/manage_slots', {
          headers: { Authorization: `Bearer ${token}` },
        })

        this.dates = res.data.dates || []
        this.slots = res.data.slots || {}
      } catch (err) {
        console.error('Fetch Slots Error:', err.response?.data || err)
        if (err.response?.status === 401) this.$router.push('/login')
      } finally {
        this.loading = false
      }
    },
    async updateSlots() {
      if (!this.selectedSlots.length) {
        alert('Please select slots to add')
        return
      }
      try {
        const token = this.getToken()
        if (!token) return

        const res = await axios.post(
          'http://127.0.0.1:5000/manage_slots',
          { slots: this.selectedSlots },
          { headers: { Authorization: `Bearer ${token}` } },
        )

        this.flashMessage = res.data.message
        this.selectedSlots = []
        await this.fetchSlots()
      } catch (err) {
        console.error('Update Slots Error:', err.response?.data || err)
      }
    },
    async cancelSlot(day, time_key) {
      if (!confirm(`Cancel slot on ${day} at ${time_key}?`)) return

      try {
        const token = this.getToken()
        if (!token) return

        const res = await axios.post(
          'http://127.0.0.1:5000/cancel_slot',
          { day, time: time_key },
          { headers: { Authorization: `Bearer ${token}` } },
        )

        this.flashMessage = res.data.message
        await this.fetchSlots()
      } catch (err) {
        console.error('Cancel Slot Error:', err.response?.data || err)
      }
    },
    goDashboard() {
      this.$router.push('/doctor/dashboard')
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
.slot-box {
  width: 120px;
  border-radius: 6px;
  padding: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

/* Status colors */
.booked {
  background-color: #d4edda;
  border: 1px solid #28a745;
  color: #155724;
}

.available {
  background-color: #cce5ff;
  border: 1px solid #004085;
  color: #004085;
}

.notcreated {
  background-color: #f8f9fa;
  border: 1px solid #6c757d;
  color: #6c757d;
}

/* Hover effect */
.slot-box:hover {
  transform: scale(1.05);
}
</style>
