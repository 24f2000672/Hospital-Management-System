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
      Configure next week slots so patients can book without delays.
    </marquee>

    <div class="container py-4">
      <h3 class="mb-3">Manage Appointment Slots</h3>

      <div class="mb-3">
        <button class="btn btn-primary" :disabled="saving || selectedSlots.length === 0" @click="saveSlots">
          {{ saving ? 'Saving...' : `Add Selected Slots (${selectedSlots.length})` }}
        </button>
      </div>

      <div v-if="loading" class="alert alert-info">Loading slots...</div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-else>
        <div v-for="day in dates" :key="day" class="card mb-3 shadow-sm">
          <div class="card-header bg-primary text-white">{{ day }}</div>
          <div class="card-body">
            <div v-for="timeKey in timeOptions" :key="`${day}-${timeKey}`" class="d-flex align-items-center mb-2">
              <template v-if="slotMap[slotKey(day, timeKey)]">
                <span class="me-2">
                  {{ slotLabels[timeKey] || timeKey }} -
                  <strong>{{ slotMap[slotKey(day, timeKey)].Status }}</strong>
                </span>
                <button
                  v-if="slotMap[slotKey(day, timeKey)].Status === 'Available'"
                  class="btn btn-outline-danger btn-sm"
                  :disabled="saving"
                  @click="cancelSlot(slotMap[slotKey(day, timeKey)].App_id)"
                >
                  Remove Slot
                </button>
              </template>
              <template v-else>
                <input
                  :id="`slot-${day}-${timeKey}`"
                  v-model="selectedSlotSet"
                  class="form-check-input me-2"
                  type="checkbox"
                  :value="slotKey(day, timeKey)"
                />
                <label :for="`slot-${day}-${timeKey}`" class="form-check-label">
                  {{ slotLabels[timeKey] || timeKey }} (Add)
                </label>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DoctorManageSlots',
  data() {
    return {
      loading: true,
      saving: false,
      error: '',
      docId: null,
      dates: [],
      timeOptions: [],
      slotLabels: {},
      slots: [],
      selectedSlotSet: [],
    }
  },
  computed: {
    selectedSlots() {
      return this.selectedSlotSet.map((value) => {
        const [dateValue, timeValue] = value.split('|')
        return { date: dateValue, time: timeValue }
      })
    },
    slotMap() {
      const mapping = {}
      this.slots.forEach((s) => {
        mapping[this.slotKey(s.Date, s.Time)] = s
      })
      return mapping
    },
  },
  methods: {
    slotKey(day, time) {
      return `${day}|${time}`
    },
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
    async loadSlots() {
      this.loading = true
      this.error = ''
      const token = this.getToken()
      if (!token) {
        this.$router.push('/login')
        return
      }

      const routeDocId = Number(this.$route.params.doc_id)
      if (!routeDocId) {
        this.error = 'Invalid doctor id.'
        this.loading = false
        return
      }

      this.docId = routeDocId

      try {
        const resp = await axios.get(`http://127.0.0.1:5000/doctor/slots/${this.docId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })

        this.dates = resp.data.dates || []
        this.timeOptions = resp.data.time_options || []
        this.slotLabels = resp.data.slot_labels || {}
        this.slots = resp.data.slots || []
      } catch (err) {
        console.error(err)
        this.error = 'Unable to load slots.'
      } finally {
        this.loading = false
      }
    },
    async saveSlots() {
      if (!this.selectedSlots.length || !this.docId) {
        return
      }

      this.saving = true
      try {
        const token = this.getToken()
        await axios.post(
          `http://127.0.0.1:5000/doctor/slots/${this.docId}`,
          { slots: this.selectedSlots },
          { headers: { Authorization: `Bearer ${token}` } },
        )

        this.selectedSlotSet = []
        await this.loadSlots()
      } catch (err) {
        console.error(err)
        alert('Failed to add selected slots.')
      } finally {
        this.saving = false
      }
    },
    async cancelSlot(slotId) {
      this.saving = true
      try {
        const token = this.getToken()
        await axios.delete(`http://127.0.0.1:5000/doctor/slots/cancel/${slotId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        await this.loadSlots()
      } catch (err) {
        console.error(err)
        alert('Failed to remove slot.')
      } finally {
        this.saving = false
      }
    },
  },
  mounted() {
    this.loadSlots()
  },
}
</script>

<style scoped>
.doctor-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>
