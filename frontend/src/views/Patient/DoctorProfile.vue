<template>
  <div class="profile-page">
    <header class="page-header container-fluid px-4 px-lg-5 py-3">
      <div class="d-flex align-items-center gap-3">
        <img src="@/assets/logo.png" alt="Health Guardian+" class="header-logo" />
        <div>
          <p class="eyebrow mb-1">Patient care</p>
          <h1 class="mb-0">Doctor Profile & Booking</h1>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <router-link to="/patient/dashboard" class="btn btn-outline-secondary">Dashboard</router-link>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </header>

    <main class="container-fluid px-4 px-lg-5 pb-5">
      <section class="summary-strip">
        <div>
          <span class="summary-label">Doctor</span>
          <strong>{{ selectedDoctor?.Name || 'Choose a doctor' }}</strong>
        </div>
        <div>
          <span class="summary-label">Available slots</span>
          <strong>{{ filteredSlots.length }}</strong>
        </div>
        <div>
          <span class="summary-label">Quick filter</span>
          <select v-model="selectedDoctorId" class="form-select">
            <option value="">All doctors</option>
            <option v-for="doctor in doctors" :key="doctor.Doc_id" :value="String(doctor.Doc_id)">
              {{ doctor.Name }}
            </option>
          </select>
        </div>
      </section>

      <div v-if="loading" class="alert alert-info mt-4">Loading doctor information...</div>
      <div v-else-if="error" class="alert alert-danger mt-4">{{ error }}</div>

      <section class="profile-grid mt-4">
        <aside class="panel-card doctor-list-panel">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <p class="eyebrow mb-1">Directory</p>
              <h2 class="mb-0">Available doctors</h2>
            </div>
          </div>

          <div class="doctor-list">
            <button
              v-for="doctor in doctors"
              :key="doctor.Doc_id"
              class="doctor-chip"
              :class="doctor.Doc_id === selectedDoctorIdNumber ? 'active' : ''"
              @click="selectDoctor(doctor.Doc_id)"
            >
              <span>{{ doctor.Name }}</span>
              <small>Department {{ doctor.Department || 'n/a' }}</small>
            </button>
          </div>
        </aside>

        <section class="panel-card">
          <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-3">
            <div>
              <p class="eyebrow mb-1">Profile</p>
              <h2 class="mb-1">{{ selectedDoctor?.Name || 'Select a doctor to view availability' }}</h2>
              <p class="mb-0 text-muted">
                Book a slot directly from the doctor profile to keep your treatment journey moving.
              </p>
            </div>
            <button class="btn btn-primary" :disabled="!selectedDoctorId" @click="bookFirstAvailable">
              Book next slot
            </button>
          </div>

          <div class="profile-banner">
            <div>
              <span class="summary-label">Doctor ID</span>
              <strong>{{ selectedDoctorId || 'All' }}</strong>
            </div>
            <div>
              <span class="summary-label">Today + 7 days</span>
              <strong>{{ filteredSlots.length }}</strong>
            </div>
            <div>
              <span class="summary-label">Accessibility</span>
              <strong>Voice + visual ready</strong>
            </div>
          </div>

          <div class="table-responsive mt-4">
            <table class="table align-middle">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Doctor</th>
                  <th class="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="slot in filteredSlots" :key="slot.App_id">
                  <td>{{ slot.Date }}</td>
                  <td>{{ formatTime(slot.Time) }}</td>
                  <td>{{ slot.Doctor }}</td>
                  <td class="text-end">
                    <button class="btn btn-success btn-sm" @click="bookSlot(slot.App_id)">Book</button>
                  </td>
                </tr>
                <tr v-if="!filteredSlots.length">
                  <td colspan="4" class="text-center py-4 text-muted">No slots available for this doctor.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </section>
    </main>
  </div>
</template>

<script>
import { api, authHeaders, isUnauthorized } from '@/services/api'

export default {
  name: 'PatientDoctorProfile',
  data() {
    return {
      loading: true,
      error: '',
      selectedDoctorId: '',
      doctors: [],
      availableSlots: [],
    }
  },
  computed: {
    selectedDoctorIdNumber() {
      return this.selectedDoctorId ? Number(this.selectedDoctorId) : null
    },
    selectedDoctor() {
      if (!this.selectedDoctorIdNumber) {
        return null
      }

      return this.doctors.find((doctor) => doctor.Doc_id === this.selectedDoctorIdNumber) || null
    },
    filteredSlots() {
      if (!this.selectedDoctorIdNumber) {
        return this.availableSlots
      }

      return this.availableSlots.filter((slot) => Number(slot.Doctor_id) === this.selectedDoctorIdNumber)
    },
  },
  mounted() {
    const routeDoctorId = this.$route.params.id
    if (routeDoctorId) {
      this.selectedDoctorId = String(routeDoctorId)
    }

    this.loadDoctorData()
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    formatTime(value) {
      return value ? value.slice(0, 5) : '-'
    },
    async loadDoctorData() {
      this.loading = true
      this.error = ''

      try {
        const [dashboardResp, slotsResp] = await Promise.all([
          api.get('/patient/dashboard', { headers: authHeaders() }),
          api.get('/patient/available-slots', { headers: authHeaders() }),
        ])

        this.doctors = dashboardResp.data.doctors || []
        const rawSlots = Array.isArray(slotsResp.data)
          ? slotsResp.data[0]?.available_slots || []
          : slotsResp.data?.available_slots || []
        this.availableSlots = rawSlots

        if (!this.selectedDoctorId && this.doctors.length) {
          this.selectedDoctorId = String(this.doctors[0].Doc_id)
        }
      } catch (error) {
        console.error(error)
        this.error = error?.response?.data?.message || 'Unable to load doctor profile.'

        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    selectDoctor(doctorId) {
      this.selectedDoctorId = String(doctorId)
      this.$router.replace({ name: 'patient-doctor-profile', params: { id: doctorId } })
    },
    async bookSlot(slotId) {
      try {
        await api.post(`/patient/book-slot/${slotId}`, {}, { headers: authHeaders() })
        await this.loadDoctorData()
      } catch (error) {
        console.error(error)
        alert(error?.response?.data?.message || 'Unable to book slot.')
      }
    },
    async bookFirstAvailable() {
      const firstSlot = this.filteredSlots[0]
      if (!firstSlot) {
        return
      }

      await this.bookSlot(firstSlot.App_id)
    },
  },
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
}

.page-header,
.panel-card,
.summary-strip {
  margin: 0 auto;
  max-width: 1320px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.header-logo {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 18px;
}

.eyebrow,
.summary-label {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.72rem;
  color: var(--health-muted);
}

.summary-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.25rem;
}

.summary-strip > div,
.panel-card,
.doctor-chip {
  border-radius: 28px;
  background: var(--health-surface);
  backdrop-filter: blur(16px);
  border: 1px solid var(--health-border);
  box-shadow: var(--health-shadow);
}

.summary-strip > div {
  padding: 1rem 1.2rem;
}

.summary-strip strong {
  display: block;
  margin-top: 0.35rem;
  font-size: 1.25rem;
}

.profile-grid {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  gap: 1rem;
}

.panel-card {
  padding: 1.25rem;
}

.doctor-list {
  display: grid;
  gap: 0.85rem;
}

.doctor-chip {
  text-align: left;
  padding: 1rem 1.1rem;
  color: inherit;
}

.doctor-chip.active {
  border-color: rgba(15, 118, 110, 0.45);
  background: rgba(15, 118, 110, 0.1);
}

.doctor-chip span {
  display: block;
  font-weight: 700;
}

.doctor-chip small {
  color: var(--health-muted);
}

.profile-banner {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.profile-banner > div {
  padding: 1rem 1.1rem;
  border-radius: 20px;
  background: rgba(15, 118, 110, 0.06);
}

.profile-banner strong {
  display: block;
  margin-top: 0.35rem;
}

@media (max-width: 992px) {
  .page-header,
  .profile-grid {
    grid-template-columns: 1fr;
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 768px) {
  .summary-strip,
  .profile-banner {
    grid-template-columns: 1fr;
  }
}
</style>
