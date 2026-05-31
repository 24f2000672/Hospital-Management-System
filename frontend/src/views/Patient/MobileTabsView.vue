<template>
  <div class="tabs-page">
    <header class="tabs-header container-fluid px-4 px-lg-5 py-3">
      <div class="d-flex align-items-center gap-3">
        <img src="@/assets/logo.png" alt="Health Guardian+" class="header-logo" />
        <div>
          <p class="eyebrow mb-1">Mobile tabs</p>
          <h1 class="mb-0">Health Guardian+ Tabs</h1>
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
          <span class="summary-label">Health score</span>
          <strong>{{ healthScore }}/100</strong>
        </div>
        <div>
          <span class="summary-label">Reminders</span>
          <strong>{{ reminders.length }}</strong>
        </div>
        <div>
          <span class="summary-label">Emergency contacts</span>
          <strong>{{ contacts.length }}</strong>
        </div>
      </section>

      <section class="tab-shell mt-4">
        <div class="tab-bar">
          <button v-for="tab in tabs" :key="tab.key" class="tab-button" :class="activeTab === tab.key ? 'active' : ''" @click="activeTab = tab.key">
            {{ tab.label }}
          </button>
        </div>

        <div class="tab-panel">
          <section v-if="activeTab === 'home'" class="tab-section">
            <div class="panel-hero">
              <div>
                <p class="eyebrow mb-1">Today</p>
                <h2 class="mb-2">Your care snapshot</h2>
                <p class="text-muted mb-0">A quick view of appointments, reminders, and emergency readiness.</p>
              </div>
              <router-link to="/patient/appointment-booking" class="btn btn-primary">Book appointment</router-link>
            </div>

            <div class="feature-grid mt-4">
              <article class="feature-card">
                <strong>Upcoming appointments</strong>
                <p>{{ upcomingAppointments.length }}</p>
              </article>
              <article class="feature-card">
                <strong>Medicine reminders</strong>
                <p>{{ reminders.length }}</p>
              </article>
              <article class="feature-card">
                <strong>Emergency contacts</strong>
                <p>{{ contacts.length }}</p>
              </article>
            </div>

            <div class="list-card mt-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="mb-0">Upcoming appointments</h3>
                <router-link to="/patient/my-appointments" class="btn btn-outline-primary btn-sm">View all</router-link>
              </div>
              <div v-if="upcomingAppointments.length" class="stack-list">
                <div v-for="appointment in upcomingAppointments.slice(0, 3)" :key="appointment.App_id" class="stack-item">
                  <strong>{{ appointment.Date }}</strong>
                  <span>{{ appointment.Time }} · {{ appointment.Doctor }}</span>
                </div>
              </div>
              <p v-else class="mb-0 text-muted">No upcoming appointments.</p>
            </div>
          </section>

          <section v-else-if="activeTab === 'emergency'" class="tab-section">
            <div class="panel-hero">
              <div>
                <p class="eyebrow mb-1">Emergency</p>
                <h2 class="mb-2">SOS, contacts, and GPS</h2>
                <p class="text-muted mb-0">Use the emergency tab to trigger a live alert quickly.</p>
              </div>
              <button class="btn btn-danger" :disabled="sosLoading" @click="triggerSOS">{{ sosLoading ? 'Sending...' : 'Trigger SOS' }}</button>
            </div>

            <div class="grid-two mt-4">
              <div class="list-card">
                <h3 class="mb-3">GPS location</h3>
                <div class="coords-grid">
                  <input v-model="sosForm.latitude" class="form-control" placeholder="Latitude" />
                  <input v-model="sosForm.longitude" class="form-control" placeholder="Longitude" />
                </div>
                <button class="btn btn-outline-primary mt-3" @click="captureLocation">Use current location</button>
              </div>

              <div class="list-card">
                <h3 class="mb-3">Emergency contacts</h3>
                <div v-if="contacts.length" class="stack-list">
                  <div v-for="contact in contacts" :key="contact.id" class="stack-item">
                    <strong>{{ contact.contact_name }}</strong>
                    <span>{{ contact.relationship || 'Contact' }} · {{ contact.phone_number }}</span>
                  </div>
                </div>
                <p v-else class="mb-0 text-muted">No emergency contacts yet.</p>
              </div>
            </div>
          </section>

          <section v-else class="tab-section">
            <div class="panel-hero">
              <div>
                <p class="eyebrow mb-1">Health AI</p>
                <h2 class="mb-2">Symptom checker and accessibility</h2>
                <p class="text-muted mb-0">Check symptoms and tune accessibility from the same mobile-friendly tab set.</p>
              </div>
              <router-link to="/patient/accessibility" class="btn btn-outline-primary">Accessibility settings</router-link>
            </div>

            <div class="grid-two mt-4">
              <div class="list-card">
                <h3 class="mb-3">Symptom checker</h3>
                <textarea v-model="symptoms" class="form-control mb-3" rows="4" placeholder="Describe symptoms"></textarea>
                <button class="btn btn-primary" :disabled="aiLoading" @click="checkSymptoms">{{ aiLoading ? 'Analyzing...' : 'Check symptoms' }}</button>
                <p v-if="aiResult" class="mt-3 mb-0"><strong>Suggestion:</strong> {{ aiResult }}</p>
              </div>

              <div class="list-card">
                <h3 class="mb-3">Accessibility controls</h3>
                <label v-for="item in accessibilityOptions" :key="item.key" class="check-row">
                  <input v-model="accessibility[item.key]" type="checkbox" />
                  <span>{{ item.label }}</span>
                </label>
                <button class="btn btn-outline-primary mt-3" :disabled="savingAccessibility" @click="saveAccessibility">
                  {{ savingAccessibility ? 'Saving...' : 'Save accessibility' }}
                </button>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { api, authHeaders, isUnauthorized } from '@/services/api'

export default {
  name: 'MobileTabsView',
  data() {
    return {
      activeTab: 'home',
      loading: false,
      upcomingAppointments: [],
      reminders: [],
      contacts: [],
      healthScore: 0,
      symptoms: '',
      aiResult: '',
      aiLoading: false,
      savingAccessibility: false,
      sosLoading: false,
      sosForm: {
        latitude: '',
        longitude: '',
      },
      accessibility: {
        voice_mode: false,
        high_contrast: false,
        large_text: false,
        sign_language_mode: false,
        vibration_alerts: false,
      },
      tabs: [
        { key: 'home', label: 'Home' },
        { key: 'emergency', label: 'Emergency' },
        { key: 'ai', label: 'Health AI' },
      ],
      accessibilityOptions: [
        { key: 'voice_mode', label: 'Voice Navigation' },
        { key: 'high_contrast', label: 'High Contrast' },
        { key: 'large_text', label: 'Large Text' },
        { key: 'sign_language_mode', label: 'Sign Language Mode' },
        { key: 'vibration_alerts', label: 'Vibration Alerts' },
      ],
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    async loadData() {
      this.loading = true

      try {
        const [dashboardResponse, remindersResponse, contactsResponse, accessibilityResponse] = await Promise.all([
          api.get('/patient/dashboard', { headers: authHeaders() }),
          api.get('/patient/medicine-reminders', { headers: authHeaders() }),
          api.get('/patient/emergency-contacts', { headers: authHeaders() }),
          api.get('/patient/accessibility-settings', { headers: authHeaders() }).catch(() => ({ data: {} })),
        ])

        this.upcomingAppointments = dashboardResponse.data.upcoming_appointments || []
        this.reminders = remindersResponse.data.reminders || []
        this.contacts = contactsResponse.data.contacts || []
        this.healthScore = Math.min(100, 55 + this.upcomingAppointments.length * 6 + this.reminders.length * 4 + this.contacts.length * 3)
        this.accessibility = {
          voice_mode: Boolean(accessibilityResponse.data.voice_mode),
          high_contrast: Boolean(accessibilityResponse.data.high_contrast),
          large_text: Boolean(accessibilityResponse.data.large_text),
          sign_language_mode: Boolean(accessibilityResponse.data.sign_language_mode),
          vibration_alerts: Boolean(accessibilityResponse.data.vibration_alerts),
        }
      } catch (error) {
        console.error(error)
        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    captureLocation() {
      if (!navigator.geolocation) {
        alert('Geolocation is not available in this browser.')
        return
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.sosForm.latitude = String(position.coords.latitude)
          this.sosForm.longitude = String(position.coords.longitude)
        },
        () => {
          alert('Unable to read your current location.')
        },
      )
    },
    async triggerSOS() {
      if (!this.sosForm.latitude || !this.sosForm.longitude) {
        alert('Enter or capture latitude and longitude first.')
        return
      }

      this.sosLoading = true

      try {
        await api.post(
          '/patient/sos-logs',
          {
            latitude: Number(this.sosForm.latitude),
            longitude: Number(this.sosForm.longitude),
            alert_type: 'SOS',
          },
          { headers: authHeaders() },
        )
        alert('SOS alert sent successfully.')
        await this.loadData()
      } catch (error) {
        console.error(error)
        alert(error?.response?.data?.message || 'Unable to send SOS alert.')
        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.sosLoading = false
      }
    },
    async checkSymptoms() {
      if (!this.symptoms.trim()) {
        alert('Enter symptoms first.')
        return
      }

      this.aiLoading = true

      try {
        const response = await api.post(
          '/patient/symptom-checks',
          { symptoms: this.symptoms.trim() },
          { headers: authHeaders() },
        )
        this.aiResult = response.data.prediction || 'Symptoms recorded.'
      } catch (error) {
        console.error(error)
        this.aiResult = error?.response?.data?.message || 'Unable to analyze symptoms.'
        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.aiLoading = false
      }
    },
    async saveAccessibility() {
      this.savingAccessibility = true

      try {
        await api.put('/patient/accessibility-settings', this.accessibility, { headers: authHeaders() })
        alert('Accessibility settings saved.')
      } catch (error) {
        console.error(error)
        alert(error?.response?.data?.message || 'Unable to save accessibility settings.')
        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.savingAccessibility = false
      }
    },
  },
}
</script>

<style scoped>
.tabs-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(20, 184, 166, 0.16), transparent 32%),
    radial-gradient(circle at top right, rgba(249, 115, 22, 0.14), transparent 30%),
    linear-gradient(180deg, #f7fbff 0%, #edf5fb 100%);
}

.tabs-header,
.summary-strip,
.tab-shell {
  margin: 0 auto;
  max-width: 1320px;
}

.tabs-header {
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
.tab-panel,
.tab-bar,
.list-card,
.feature-card {
  border-radius: 28px;
  background: var(--health-surface);
  border: 1px solid var(--health-border);
  box-shadow: var(--health-shadow);
}

.summary-strip > div {
  padding: 1rem 1.2rem;
}

.summary-strip strong {
  display: block;
  margin-top: 0.35rem;
  font-size: 1.6rem;
}

.tab-shell {
  display: grid;
  grid-template-columns: 160px minmax(0, 1fr);
  gap: 1rem;
}

.tab-bar {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  position: sticky;
  top: 1rem;
  height: fit-content;
}

.tab-button {
  border: 0;
  border-radius: 20px;
  padding: 0.9rem 1rem;
  text-align: left;
  background: rgba(15, 118, 110, 0.06);
  color: var(--health-text);
  font-weight: 700;
}

.tab-button.active {
  background: rgba(15, 118, 110, 0.16);
  color: var(--health-primary-strong);
}

.tab-panel {
  padding: 1.25rem;
}

.panel-hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.feature-grid,
.grid-two,
.coords-grid {
  display: grid;
  gap: 1rem;
}

.feature-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.grid-two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.feature-card,
.list-card {
  padding: 1rem;
}

.feature-card strong {
  display: block;
  margin-bottom: 0.4rem;
}

.feature-card p {
  margin-bottom: 0;
  font-size: 1.6rem;
}

.stack-list {
  display: grid;
  gap: 0.75rem;
}

.stack-item {
  border-radius: 20px;
  padding: 1rem;
  background: rgba(15, 118, 110, 0.04);
  border: 1px solid rgba(16, 32, 51, 0.08);
}

.stack-item strong,
.stack-item span {
  display: block;
}

.stack-item span,
.text-muted {
  color: var(--health-muted);
}

.check-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0;
}

.coords-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

@media (max-width: 992px) {
  .tabs-header,
  .tab-shell,
  .feature-grid,
  .grid-two,
  .coords-grid,
  .summary-strip {
    grid-template-columns: 1fr;
  }

  .tabs-header,
  .panel-hero {
    flex-direction: column;
    align-items: stretch;
  }

  .tab-bar {
    position: static;
    flex-direction: row;
    overflow-x: auto;
  }

  .tab-button {
    white-space: nowrap;
    min-width: 120px;
  }
}
</style>