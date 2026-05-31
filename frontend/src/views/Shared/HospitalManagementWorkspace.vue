<template>
  <div class="workspace-page">
    <header class="workspace-header container-fluid px-4 px-lg-5 py-3">
      <div class="d-flex align-items-center gap-3">
        <img src="@/assets/logo.png" alt="Health Guardian+" class="header-logo" />
        <div>
          <p class="eyebrow mb-1">Hospital operations</p>
          <h1 class="mb-0">{{ title }}</h1>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <router-link to="/admin/dashboard" class="btn btn-outline-secondary">Dashboard</router-link>
        <router-link to="/admin/manage-patients" class="btn btn-outline-primary">Patients</router-link>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </header>

    <main class="container-fluid px-4 px-lg-5 pb-5">
      <section class="hero-strip">
        <div>
          <span class="summary-label">Module</span>
          <strong>{{ moduleLabel }}</strong>
        </div>
        <div>
          <span class="summary-label">Focus</span>
          <strong>{{ focusText }}</strong>
        </div>
        <div>
          <span class="summary-label">State</span>
          <strong>{{ loading ? 'Loading records' : 'Ready for action' }}</strong>
        </div>
      </section>

      <div v-if="error" class="alert alert-danger mt-4 mb-0">{{ error }}</div>
      <div v-if="success" class="alert alert-success mt-4 mb-0">{{ success }}</div>

      <section v-if="isCrudModule" class="workspace-grid mt-4">
        <article class="panel-card accent-card">
          <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap">
            <div>
              <p class="eyebrow mb-1">Overview</p>
              <h2 class="mb-2">{{ descriptionTitle }}</h2>
              <p class="text-muted mb-0">{{ description }}</p>
            </div>
            <button class="btn btn-outline-primary" :disabled="loading" @click="loadWorkspace">Refresh</button>
          </div>

          <div class="metrics-grid mt-4">
            <div v-for="item in metrics" :key="item.label" class="metric-card">
              <span>{{ item.label }}</span>
              <strong>{{ item.value }}</strong>
            </div>
          </div>

          <div class="flow-grid mt-4">
            <div v-for="step in flowSteps" :key="step.title" class="flow-step">
              <strong>{{ step.title }}</strong>
              <p>{{ step.text }}</p>
            </div>
          </div>
        </article>

        <article class="panel-card">
          <div class="d-flex justify-content-between align-items-center gap-3 flex-wrap mb-3">
            <div>
              <p class="eyebrow mb-1">{{ editingId ? 'Edit' : 'Create' }}</p>
              <h2 class="mb-0">{{ formHeading }}</h2>
            </div>
            <button class="btn btn-outline-secondary btn-sm" type="button" @click="resetForm">Clear</button>
          </div>

          <form class="workspace-form" @submit.prevent="saveRecord">
            <template v-if="moduleKey === 'rooms'">
              <div>
                <label class="form-label">Room number</label>
                <input v-model.trim="form.room_number" class="form-control" placeholder="A-101" required />
              </div>
              <div>
                <label class="form-label">Type</label>
                <input v-model.trim="form.type" class="form-control" placeholder="ICU, Ward, Private" required />
              </div>
              <div>
                <label class="form-label">Status</label>
                <select v-model="form.status" class="form-select">
                  <option value="AVAILABLE">AVAILABLE</option>
                  <option value="OCCUPIED">OCCUPIED</option>
                  <option value="MAINTENANCE">MAINTENANCE</option>
                </select>
              </div>
              <div>
                <label class="form-label">Notes</label>
                <textarea v-model.trim="form.notes" class="form-control" rows="3" placeholder="Optional room notes"></textarea>
              </div>
            </template>

            <template v-else-if="moduleKey === 'admissions'">
              <div>
                <label class="form-label">Patient</label>
                <select v-model="form.patient_id" class="form-select" required>
                  <option value="">Select patient</option>
                  <option v-for="patient in patients" :key="patient.id" :value="String(patient.id)">
                    {{ patient.first_name }} {{ patient.last_name }} - {{ patient.email }}
                  </option>
                </select>
              </div>
              <div>
                <label class="form-label">Room</label>
                <select v-model="form.room_id" class="form-select" required>
                  <option value="">Select room</option>
                  <option v-for="room in rooms" :key="room.id" :value="String(room.id)">
                    {{ room.room_number }} - {{ room.type }} ({{ room.status }})
                  </option>
                </select>
              </div>
              <div>
                <label class="form-label">Admission date</label>
                <input v-model="form.admission_date" type="datetime-local" class="form-control" />
              </div>
              <div>
                <label class="form-label">Discharge date</label>
                <input v-model="form.discharge_date" type="datetime-local" class="form-control" />
              </div>
              <div>
                <label class="form-label">Status</label>
                <select v-model="form.status" class="form-select">
                  <option value="ADMITTED">ADMITTED</option>
                  <option value="DISCHARGED">DISCHARGED</option>
                  <option value="TRANSFERRED">TRANSFERRED</option>
                  <option value="CANCELLED">CANCELLED</option>
                </select>
              </div>
              <div class="helper-card">
                <strong>Room assignment rule</strong>
                <p class="mb-0">Admissions mark the selected room occupied until the stay is discharged or deleted.</p>
              </div>
            </template>

            <template v-else>
              <div>
                <label class="form-label">Patient</label>
                <select v-model="form.patient_id" class="form-select" required>
                  <option value="">Select patient</option>
                  <option v-for="patient in patients" :key="patient.id" :value="String(patient.id)">
                    {{ patient.first_name }} {{ patient.last_name }} - {{ patient.email }}
                  </option>
                </select>
              </div>
              <div>
                <label class="form-label">Admission</label>
                <select v-model="form.admission_id" class="form-select">
                  <option value="">Optional: link admission</option>
                  <option v-for="admission in admissions" :key="admission.id" :value="String(admission.id)">
                    #{{ admission.id }} - {{ admission.patient_name }} - {{ admission.room_number || 'Room N/A' }}
                  </option>
                </select>
              </div>
              <div>
                <label class="form-label">Consultation fees</label>
                <input v-model.number="form.consultation_fees" type="number" min="0" step="0.01" class="form-control" @input="syncTotalAmount" />
              </div>
              <div>
                <label class="form-label">Medicine fees</label>
                <input v-model.number="form.medicine_fees" type="number" min="0" step="0.01" class="form-control" @input="syncTotalAmount" />
              </div>
              <div>
                <label class="form-label">Total amount</label>
                <input v-model.number="form.total_amount" type="number" min="0" step="0.01" class="form-control" />
              </div>
              <div>
                <label class="form-label">Status</label>
                <select v-model="form.status" class="form-select">
                  <option value="PENDING">PENDING</option>
                  <option value="PARTIAL">PARTIAL</option>
                  <option value="PAID">PAID</option>
                  <option value="CANCELLED">CANCELLED</option>
                </select>
              </div>
              <div class="helper-card">
                <strong>Billing total</strong>
                <p class="mb-0">The total defaults to the sum of consultation and medicine fees, but you can override it.</p>
              </div>
            </template>

            <div class="d-flex flex-wrap gap-2 pt-2">
              <button class="btn btn-primary" type="submit" :disabled="loading">
                {{ editingId ? 'Update record' : 'Create record' }}
              </button>
              <button class="btn btn-outline-secondary" type="button" @click="resetForm">Reset</button>
            </div>
          </form>
        </article>
      </section>

      <section v-if="isCrudModule" class="panel-card mt-4">
        <div class="d-flex justify-content-between align-items-center gap-3 flex-wrap mb-3">
          <div>
            <p class="eyebrow mb-1">Records</p>
            <h2 class="mb-0">{{ tableHeading }}</h2>
          </div>
          <span class="text-muted">{{ records.length }} items</span>
        </div>

        <div class="table-responsive">
          <table class="table align-middle">
            <thead>
              <tr>
                <th v-for="column in tableColumns" :key="column">{{ column }}</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in records" :key="record.id">
                <template v-if="moduleKey === 'rooms'">
                  <td>{{ record.room_number }}</td>
                  <td>{{ record.type }}</td>
                  <td>
                    <span class="status-chip" :class="statusClass(record.status)">{{ record.status }}</span>
                  </td>
                  <td>{{ record.is_occupied ? 'Yes' : 'No' }}</td>
                  <td>{{ record.notes || '—' }}</td>
                </template>

                <template v-else-if="moduleKey === 'admissions'">
                  <td>{{ record.patient_name || `Patient #${record.patient_id}` }}</td>
                  <td>{{ record.room_number || `Room #${record.room_id}` }}</td>
                  <td>{{ formatTimestamp(record.admission_date) }}</td>
                  <td>{{ formatTimestamp(record.discharge_date) }}</td>
                  <td>
                    <span class="status-chip" :class="statusClass(record.status)">{{ record.status }}</span>
                  </td>
                </template>

                <template v-else>
                  <td>{{ record.patient_name || `Patient #${record.patient_id}` }}</td>
                  <td>
                    {{ record.admission_id ? `Admission #${record.admission_id}` : 'No admission link' }}
                    <div class="text-muted small">{{ record.room_number || 'Room N/A' }}</div>
                  </td>
                  <td>{{ formatCurrency(record.consultation_fees) }}</td>
                  <td>{{ formatCurrency(record.medicine_fees) }}</td>
                  <td>{{ formatCurrency(record.total_amount) }}</td>
                  <td>
                    <span class="status-chip" :class="statusClass(record.status)">{{ record.status }}</span>
                  </td>
                </template>

                <td>
                  <div class="d-flex justify-content-end flex-wrap gap-2">
                    <button class="btn btn-outline-primary btn-sm" type="button" @click="editRecord(record)">Edit</button>
                    <button class="btn btn-outline-danger btn-sm" type="button" @click="deleteRecord(record)">Delete</button>
                  </div>
                </td>
              </tr>
              <tr v-if="!records.length">
                <td :colspan="tableColumns.length + 1" class="text-center py-4 text-muted">
                  No records found yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="isCrudModule" class="panel-card mt-4">
        <div class="d-flex justify-content-between align-items-center gap-3 flex-wrap mb-3">
          <div>
            <p class="eyebrow mb-1">Reference data</p>
            <h2 class="mb-0">Supporting lists</h2>
          </div>
        </div>

        <div class="support-grid">
          <div class="support-card">
            <strong>Patients</strong>
            <p>{{ patients.length }} loaded</p>
            <small v-if="patients.length">{{ patients[0].first_name }} {{ patients[0].last_name }} is first in the list.</small>
          </div>
          <div class="support-card">
            <strong>Rooms</strong>
            <p>{{ rooms.length }} loaded</p>
            <small v-if="rooms.length">{{ rooms[0].room_number }} is the first room in the list.</small>
          </div>
          <div class="support-card">
            <strong>Admissions</strong>
            <p>{{ admissions.length }} loaded</p>
            <small v-if="admissions.length">Latest admission is #{{ admissions[0].id }}.</small>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { api, authHeaders, isUnauthorized } from '@/services/api'

const moduleConfig = {
  rooms: {
    title: 'Room Assignment',
    moduleLabel: 'Room inventory',
    focusText: 'Beds, wards, and occupancy',
    descriptionTitle: 'Room operations',
    description: 'Create and maintain room records, occupancy state, and operational notes.',
    tableHeading: 'Room roster',
    endpoint: '/admin/rooms',
    flowSteps: [
      { title: 'Create room', text: 'Register a new room and initial status.' },
      { title: 'Track occupancy', text: 'Mark occupied rooms while patients are admitted.' },
      { title: 'Maintain notes', text: 'Keep maintenance or availability notes visible.' },
    ],
    metrics: (workspace) => [
      { label: 'Total rooms', value: workspace.records.length },
      { label: 'Available', value: workspace.records.filter((room) => room.status === 'AVAILABLE').length },
      { label: 'Occupied', value: workspace.records.filter((room) => room.status === 'OCCUPIED').length },
    ],
    tableColumns: ['Room number', 'Type', 'Status', 'Occupied', 'Notes'],
  },
  admissions: {
    title: 'Admissions',
    moduleLabel: 'Admission workflow',
    focusText: 'Room assignment and discharge',
    descriptionTitle: 'Admission operations',
    description: 'Admit patients into rooms, discharge them, and keep room occupancy in sync.',
    tableHeading: 'Admission log',
    endpoint: '/admin/admissions',
    flowSteps: [
      { title: 'Select patient', text: 'Pick the patient from the live roster.' },
      { title: 'Assign room', text: 'Choose an available room for the stay.' },
      { title: 'Close stay', text: 'Discharge the patient and release the room.' },
    ],
    metrics: (workspace) => [
      { label: 'Total admissions', value: workspace.records.length },
      { label: 'Active stays', value: workspace.records.filter((admission) => admission.status === 'ADMITTED').length },
      { label: 'Discharged', value: workspace.records.filter((admission) => admission.status === 'DISCHARGED').length },
    ],
    tableColumns: ['Patient', 'Room', 'Admission', 'Discharge', 'Status'],
  },
  billing: {
    title: 'Billing',
    moduleLabel: 'Billing workflow',
    focusText: 'Charges, totals, and payment state',
    descriptionTitle: 'Billing operations',
    description: 'Record consultation and medicine charges, link admissions, and track payment progress.',
    tableHeading: 'Billing ledger',
    endpoint: '/admin/billing',
    flowSteps: [
      { title: 'Link patient', text: 'Choose the patient and optional admission.' },
      { title: 'Add charges', text: 'Enter consultation and medicine fees.' },
      { title: 'Track payment', text: 'Update the bill as PENDING, PARTIAL, or PAID.' },
    ],
    metrics: (workspace) => {
      const totalOutstanding = workspace.records
        .filter((bill) => bill.status !== 'PAID')
        .reduce((sum, bill) => sum + Number(bill.total_amount || 0), 0)

      return [
        { label: 'Total bills', value: workspace.records.length },
        { label: 'Paid bills', value: workspace.records.filter((bill) => bill.status === 'PAID').length },
        { label: 'Outstanding', value: `$${totalOutstanding.toFixed(2)}` },
      ]
    },
    tableColumns: ['Patient', 'Admission / room', 'Consultation', 'Medicine', 'Total', 'Status'],
  },
}

export default {
  name: 'HospitalManagementWorkspace',
  data() {
    return {
      loading: false,
      error: '',
      success: '',
      records: [],
      patients: [],
      rooms: [],
      admissions: [],
      editingId: null,
      form: {},
    }
  },
  computed: {
    moduleKey() {
      return this.$route.meta.moduleKey || 'rooms'
    },
    config() {
      return moduleConfig[this.moduleKey] || moduleConfig.rooms
    },
    title() {
      return this.$route.meta.title || this.config.title
    },
    moduleLabel() {
      return this.config.moduleLabel
    },
    focusText() {
      return this.config.focusText
    },
    descriptionTitle() {
      return this.config.descriptionTitle
    },
    description() {
      return this.config.description
    },
    tableHeading() {
      return this.config.tableHeading
    },
    flowSteps() {
      return this.config.flowSteps
    },
    isCrudModule() {
      return ['rooms', 'admissions', 'billing'].includes(this.moduleKey)
    },
    metrics() {
      if (!this.isCrudModule) {
        return []
      }
      return this.config.metrics(this)
    },
    tableColumns() {
      return this.config.tableColumns
    },
    recordKey() {
      if (this.moduleKey === 'rooms') {
        return 'rooms'
      }
      if (this.moduleKey === 'admissions') {
        return 'admissions'
      }
      return 'billing'
    },
    formHeading() {
      if (this.moduleKey === 'rooms') {
        return this.editingId ? 'Edit room' : 'Create room'
      }
      if (this.moduleKey === 'admissions') {
        return this.editingId ? 'Edit admission' : 'Create admission'
      }
      return this.editingId ? 'Edit bill' : 'Create bill'
    },
  },
  watch: {
    '$route.path'() {
      this.bootstrapWorkspace()
    },
  },
  mounted() {
    this.bootstrapWorkspace()
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    clearMessages() {
      this.error = ''
      this.success = ''
    },
    async bootstrapWorkspace() {
      this.clearMessages()
      this.resetForm()

      if (!this.isCrudModule) {
        return
      }

      await this.loadWorkspace()
    },
    baseForm() {
      if (this.moduleKey === 'rooms') {
        return {
          room_number: '',
          type: '',
          status: 'AVAILABLE',
          notes: '',
        }
      }

      if (this.moduleKey === 'admissions') {
        return {
          patient_id: '',
          room_id: '',
          admission_date: '',
          discharge_date: '',
          status: 'ADMITTED',
        }
      }

      return {
        patient_id: '',
        admission_id: '',
        consultation_fees: 0,
        medicine_fees: 0,
        total_amount: 0,
        status: 'PENDING',
      }
    },
    resetForm() {
      this.editingId = null
      this.form = this.baseForm()
    },
    async loadWorkspace() {
      this.loading = true
      this.clearMessages()

      try {
        const response = await api.get(this.config.endpoint, { headers: authHeaders() })
        this.records = response.data[this.recordKey] || []
        this.patients = response.data.patients || []
        this.rooms = response.data.rooms || (this.moduleKey === 'rooms' ? this.records : [])
        this.admissions = response.data.admissions || []
        this.resetForm()
      } catch (error) {
        console.error(error)
        this.error = error?.response?.data?.message || 'Unable to load workspace data.'
        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    syncTotalAmount() {
      if (this.moduleKey !== 'billing') {
        return
      }
      const consultation = Number(this.form.consultation_fees || 0)
      const medicine = Number(this.form.medicine_fees || 0)
      this.form.total_amount = Number((consultation + medicine).toFixed(2))
    },
    editRecord(record) {
      this.editingId = record.id

      if (this.moduleKey === 'rooms') {
        this.form = {
          room_number: record.room_number || '',
          type: record.type || '',
          status: record.status || 'AVAILABLE',
          notes: record.notes || '',
        }
        return
      }

      if (this.moduleKey === 'admissions') {
        this.form = {
          patient_id: String(record.patient_id || ''),
          room_id: String(record.room_id || ''),
          admission_date: this.toDateTimeLocal(record.admission_date),
          discharge_date: this.toDateTimeLocal(record.discharge_date),
          status: record.status || 'ADMITTED',
        }
        return
      }

      this.form = {
        patient_id: String(record.patient_id || ''),
        admission_id: record.admission_id ? String(record.admission_id) : '',
        consultation_fees: Number(record.consultation_fees || 0),
        medicine_fees: Number(record.medicine_fees || 0),
        total_amount: Number(record.total_amount || 0),
        status: record.status || 'PENDING',
      }
    },
    async saveRecord() {
      this.loading = true
      this.clearMessages()

      const payload = this.buildPayload()
      const headers = authHeaders()
      const resourceUrl = this.editingId ? `${this.config.endpoint}/${this.editingId}` : this.config.endpoint
      const method = this.editingId ? 'put' : 'post'

      try {
        await api[method](resourceUrl, payload, { headers })
        this.success = this.editingId ? 'Record updated successfully.' : 'Record created successfully.'
        await this.loadWorkspace()
      } catch (error) {
        console.error(error)
        this.error = error?.response?.data?.message || 'Unable to save record.'
        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    buildPayload() {
      if (this.moduleKey === 'rooms') {
        return {
          room_number: this.form.room_number,
          type: this.form.type,
          status: this.form.status,
          notes: this.form.notes,
        }
      }

      if (this.moduleKey === 'admissions') {
        return {
          patient_id: Number(this.form.patient_id),
          room_id: Number(this.form.room_id),
          admission_date: this.form.admission_date || null,
          discharge_date: this.form.discharge_date || null,
          status: this.form.status,
        }
      }

      const consultation = Number(this.form.consultation_fees || 0)
      const medicine = Number(this.form.medicine_fees || 0)
      const total = Number.isFinite(Number(this.form.total_amount)) && Number(this.form.total_amount) > 0
        ? Number(this.form.total_amount)
        : Number((consultation + medicine).toFixed(2))

      return {
        patient_id: Number(this.form.patient_id),
        admission_id: this.form.admission_id ? Number(this.form.admission_id) : null,
        consultation_fees: consultation,
        medicine_fees: medicine,
        total_amount: total,
        status: this.form.status,
      }
    },
    async deleteRecord(record) {
      const confirmed = window.confirm(`Delete record #${record.id}? This cannot be undone.`)
      if (!confirmed) {
        return
      }

      this.loading = true
      this.clearMessages()

      try {
        await api.delete(`${this.config.endpoint}/${record.id}`, { headers: authHeaders() })
        this.success = 'Record deleted successfully.'
        await this.loadWorkspace()
      } catch (error) {
        console.error(error)
        this.error = error?.response?.data?.message || 'Unable to delete record.'
        if (isUnauthorized(error)) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    statusClass(status) {
      const normalized = String(status || '').toUpperCase()

      if (['AVAILABLE', 'PAID', 'DISCHARGED'].includes(normalized)) {
        return 'success'
      }

      if (['OCCUPIED', 'PENDING', 'ADMITTED', 'PARTIAL'].includes(normalized)) {
        return 'warning'
      }

      if (['MAINTENANCE', 'CANCELLED'].includes(normalized)) {
        return 'danger'
      }

      return 'neutral'
    },
    toDateTimeLocal(value) {
      if (!value) {
        return ''
      }
      const text = String(value)
      return text.length >= 16 ? text.slice(0, 16) : text
    },
    formatTimestamp(value) {
      if (!value) {
        return '—'
      }
      return String(value).replace('T', ' ').slice(0, 16)
    },
    formatCurrency(value) {
      const amount = Number(value || 0)
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 2,
      }).format(amount)
    },
  },
}
</script>

<style scoped>
.workspace-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(14, 165, 233, 0.16), transparent 34%),
    radial-gradient(circle at top right, rgba(20, 184, 166, 0.14), transparent 30%),
    linear-gradient(180deg, #f8fbff 0%, #eef5fb 100%);
}

.workspace-header,
.panel-card,
.hero-strip {
  margin: 0 auto;
  max-width: 1320px;
}

.workspace-header {
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

.hero-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.25rem;
}

.hero-strip > div,
.panel-card {
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(18px);
  border: 1px solid var(--health-border);
  box-shadow: var(--health-shadow);
}

.hero-strip > div {
  padding: 1rem 1.2rem;
}

.hero-strip strong {
  display: block;
  margin-top: 0.35rem;
  font-size: 1.75rem;
}

.panel-card {
  margin-top: 1.5rem;
  padding: 1.35rem;
}

.workspace-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 1.25rem;
}

.accent-card {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 252, 255, 0.92));
}

.metrics-grid,
.support-grid {
  display: grid;
  gap: 1rem;
}

.metrics-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.support-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.metric-card,
.support-card,
.helper-card {
  border-radius: 22px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(15, 23, 42, 0.03);
  padding: 1rem 1.1rem;
}

.metric-card span,
.support-card p {
  display: block;
  color: var(--health-muted);
  margin-bottom: 0.35rem;
}

.metric-card strong {
  font-size: 1.7rem;
}

.flow-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.flow-step,
.helper-card {
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.78);
}

.flow-step {
  border: 1px solid rgba(148, 163, 184, 0.18);
  padding: 1rem 1.1rem;
}

.flow-step p {
  margin-bottom: 0;
  color: var(--health-muted);
}

.workspace-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.workspace-form > div {
  min-width: 0;
}

.workspace-form .helper-card,
.workspace-form .d-flex {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.92rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  font-size: 0.78rem;
  font-weight: 700;
}

.status-chip.success {
  background: rgba(22, 163, 74, 0.12);
  color: var(--health-success);
}

.status-chip.warning {
  background: rgba(245, 158, 11, 0.16);
  color: #b45309;
}

.status-chip.danger {
  background: rgba(220, 38, 38, 0.12);
  color: var(--health-danger);
}

.status-chip.neutral {
  background: rgba(71, 85, 105, 0.12);
  color: #475569;
}

@media (max-width: 992px) {
  .workspace-header,
  .hero-strip,
  .workspace-grid,
  .metrics-grid,
  .support-grid,
  .flow-grid {
    grid-template-columns: 1fr;
  }

  .workspace-header {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 768px) {
  .workspace-form {
    grid-template-columns: 1fr;
  }

  .hero-strip > div,
  .panel-card {
    border-radius: 22px;
  }
}
</style>
