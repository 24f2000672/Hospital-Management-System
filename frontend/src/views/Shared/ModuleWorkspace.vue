<template>
  <div class="module-page">
    <header class="module-header container-fluid px-4 px-lg-5 py-3">
      <div class="d-flex align-items-center gap-3">
        <img src="@/assets/logo.png" alt="Health Guardian+" class="header-logo" />
        <div>
          <p class="eyebrow mb-1">{{ subtitle }}</p>
          <h1 class="mb-0">{{ title }}</h1>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <router-link :to="homeRoute" class="btn btn-outline-secondary">Home</router-link>
        <router-link :to="dashboardRoute" class="btn btn-outline-primary">Dashboard</router-link>
      </div>
    </header>

    <main class="container-fluid px-4 px-lg-5 pb-5">
      <section class="hero-strip">
        <div>
          <span class="summary-label">Mode</span>
          <strong>{{ moduleLabel }}</strong>
        </div>
        <div>
          <span class="summary-label">Focus</span>
          <strong>{{ focusText }}</strong>
        </div>
        <div>
          <span class="summary-label">Status</span>
          <strong>Ready for API wiring</strong>
        </div>
      </section>

      <section class="module-grid mt-4">
        <article class="panel-card">
          <p class="eyebrow mb-1">Overview</p>
          <h2 class="mb-3">{{ title }}</h2>
          <p class="text-muted">{{ description }}</p>

          <div class="feature-list mt-4">
            <div v-for="item in highlights" :key="item.title" class="feature-item">
              <strong>{{ item.title }}</strong>
              <p>{{ item.text }}</p>
            </div>
          </div>
        </article>

        <article class="panel-card">
          <p class="eyebrow mb-1">Actions</p>
          <h2 class="mb-3">Quick controls</h2>

          <div v-if="moduleKey === 'emergency-sos'" class="action-stack">
            <button class="btn btn-danger btn-lg">Trigger SOS</button>
            <button class="btn btn-outline-primary">Share GPS location</button>
            <button class="btn btn-outline-secondary">Notify emergency contacts</button>
          </div>

          <div v-else-if="moduleKey === 'medicine-reminder'" class="action-stack">
            <input class="form-control" placeholder="Medicine name" />
            <input class="form-control" placeholder="Dosage" />
            <input class="form-control" placeholder="Reminder time" />
            <button class="btn btn-primary">Save reminder</button>
          </div>

          <div v-else-if="moduleKey === 'ai-assistant'" class="action-stack">
            <textarea class="form-control" rows="4" placeholder="Describe symptoms"></textarea>
            <button class="btn btn-primary">Check symptoms</button>
            <button class="btn btn-outline-secondary">Open AI chat</button>
          </div>

          <div v-else-if="moduleKey === 'accessibility'" class="action-stack">
            <label v-for="item in accessibilityOptions" :key="item" class="check-row">
              <input type="checkbox" />
              <span>{{ item }}</span>
            </label>
          </div>

          <div v-else-if="moduleKey === 'health-card'" class="health-card-preview">
            <div class="card-row"><span>Name</span><strong>Patient Name</strong></div>
            <div class="card-row"><span>Blood Group</span><strong>O+</strong></div>
            <div class="card-row"><span>Allergies</span><strong>None recorded</strong></div>
            <div class="card-row"><span>Emergency Contact</span><strong>Primary contact</strong></div>
          </div>

          <div v-else class="action-stack">
            <input class="form-control" placeholder="Search / select item" />
            <button class="btn btn-primary">Save changes</button>
            <button class="btn btn-outline-secondary">Download report</button>
          </div>
        </article>
      </section>

      <section class="panel-card mt-4">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3">
          <div>
            <p class="eyebrow mb-1">Accessible flow</p>
            <h2 class="mb-0">{{ accessibleFlowTitle }}</h2>
          </div>
          <button class="btn btn-outline-primary">Open mobile tab</button>
        </div>

        <div class="flow-grid">
          <div v-for="step in flowSteps" :key="step.title" class="flow-step">
            <strong>{{ step.title }}</strong>
            <p>{{ step.text }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
const moduleCatalog = {
  'patient-profile': {
    subtitle: 'Patient section',
    title: 'Profile',
    description: 'View personal details and keep medical information current.',
    moduleLabel: 'Patient Profile',
    focusText: 'Identity + medical data',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'From login to health management',
    highlights: [
      { title: 'Personal details', text: 'Name, contact, address, and emergency metadata.' },
      { title: 'Medical info', text: 'Blood group, allergies, chronic diseases, and notes.' },
      { title: 'Digital card', text: 'Use as a quick medical ID during emergencies.' },
    ],
    flowSteps: [
      { title: 'Login', text: 'Authenticate securely.' },
      { title: 'Review profile', text: 'Confirm details and update records.' },
      { title: 'Save', text: 'Keep profile ready for care and emergencies.' },
    ],
  },
  'medical-records': {
    subtitle: 'Patient section',
    title: 'Medical Records',
    description: 'Track blood group, allergies, chronic diseases, and emergency notes.',
    moduleLabel: 'Patient Records',
    focusText: 'Core medical history',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Medical record access flow',
    highlights: [
      { title: 'Blood group', text: 'Useful for transfusion and emergency treatment.' },
      { title: 'Allergies', text: 'Reduce risk during medication planning.' },
      { title: 'Emergency notes', text: 'Critical information visible in emergencies.' },
    ],
    flowSteps: [
      { title: 'Open record', text: 'Access the patient record hub.' },
      { title: 'Review fields', text: 'Check allergies, diseases, and notes.' },
      { title: 'Share securely', text: 'Provide to doctors when needed.' },
    ],
  },
  reports: {
    subtitle: 'Patient section',
    title: 'Health Reports',
    description: 'Upload and download lab reports, X-rays, MRI reports, and prescriptions.',
    moduleLabel: 'Patient Reports',
    focusText: 'Documents and downloads',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Report management flow',
    highlights: [
      { title: 'Uploads', text: 'Attach scanned prescriptions and diagnostics.' },
      { title: 'Downloads', text: 'Access reports anytime from the dashboard.' },
      { title: 'History', text: 'Maintain an organized report archive.' },
    ],
    flowSteps: [
      { title: 'Upload', text: 'Add report documents.' },
      { title: 'Review', text: 'Verify type and notes.' },
      { title: 'Download', text: 'Export when needed.' },
    ],
  },
  'appointment-booking': {
    subtitle: 'Patient section',
    title: 'Appointment Booking',
    description: 'Browse doctors, choose slots, and book visits instantly.',
    moduleLabel: 'Appointments',
    focusText: 'Doctors and slots',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Booking flow',
    highlights: [
      { title: 'Doctor list', text: 'Find the right specialist.' },
      { title: 'Slot availability', text: 'See open times in real time.' },
      { title: 'Booking action', text: 'Reserve and confirm a slot.' },
    ],
    flowSteps: [
      { title: 'Pick doctor', text: 'Choose your care provider.' },
      { title: 'Select slot', text: 'See available time windows.' },
      { title: 'Confirm', text: 'Book the appointment.' },
    ],
  },
  'my-appointments': {
    subtitle: 'Patient section',
    title: 'My Appointments',
    description: 'View upcoming and past appointments with cancel controls.',
    moduleLabel: 'Appointment history',
    focusText: 'Upcoming + past visits',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Appointment lifecycle',
    highlights: [
      { title: 'Upcoming', text: 'Track the next visit.' },
      { title: 'Past', text: 'Review completed appointments.' },
      { title: 'Cancel', text: 'Handle schedule changes safely.' },
    ],
    flowSteps: [
      { title: 'Review', text: 'Check scheduled appointments.' },
      { title: 'Change', text: 'Cancel if necessary.' },
      { title: 'Return', text: 'Book a new slot later.' },
    ],
  },
  'medicine-reminder': {
    subtitle: 'Patient section',
    title: 'Medicine Reminder',
    description: 'Add medicines, configure dosage, and track adherence.',
    moduleLabel: 'Medicine adherence',
    focusText: 'Schedules + doses',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Reminder workflow',
    highlights: [
      { title: 'Daily doses', text: 'Define medicine timing and dosage.' },
      { title: 'Missed dose tracking', text: 'Monitor adherence trends.' },
      { title: 'Notifications', text: 'Send reminders and escalations.' },
    ],
    flowSteps: [
      { title: 'Add medicine', text: 'Save dosage and frequency.' },
      { title: 'Notify', text: 'Alert at the right time.' },
      { title: 'Track', text: 'Measure compliance.' },
    ],
  },
  'emergency-sos': {
    subtitle: 'Patient section',
    title: 'Emergency SOS',
    description: 'One-tap alerting with location sharing and emergency contact notification.',
    moduleLabel: 'Emergency mode',
    focusText: 'SOS + location',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Emergency escalation flow',
    highlights: [
      { title: 'SOS button', text: 'Trigger emergency response immediately.' },
      { title: 'GPS sharing', text: 'Send live location to responders.' },
      { title: 'Contact alerts', text: 'Notify family and caregivers.' },
    ],
    flowSteps: [
      { title: 'Trigger', text: 'Tap the SOS button.' },
      { title: 'Share location', text: 'Expose current coordinates.' },
      { title: 'Escalate', text: 'Notify contacts and hospitals.' },
    ],
  },
  'ai-assistant': {
    subtitle: 'Patient section',
    title: 'AI Health Assistant',
    description: 'Check symptoms, get recommendations, and expand into AI chat later.',
    moduleLabel: 'AI module',
    focusText: 'Symptoms + suggestions',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'AI health guidance flow',
    highlights: [
      { title: 'Symptom checker', text: 'Capture symptoms and triage risk.' },
      { title: 'Health advice', text: 'Offer simple recommendations.' },
      { title: 'Future chat', text: 'Ready for chatbot expansion.' },
    ],
    flowSteps: [
      { title: 'Describe', text: 'Enter symptoms.' },
      { title: 'Analyze', text: 'Get a preliminary suggestion.' },
      { title: 'Act', text: 'Follow a care recommendation.' },
    ],
  },
  accessibility: {
    subtitle: 'Patient section',
    title: 'Accessibility',
    description: 'Configure voice, contrast, vibration, sign-language, and large-text modes.',
    moduleLabel: 'Accessibility settings',
    focusText: 'Inclusive controls',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Accessibility configuration flow',
    highlights: [
      { title: 'Voice navigation', text: 'Use spoken prompts and navigation.' },
      { title: 'High contrast', text: 'Improve readability for low-vision users.' },
      { title: 'Vibration alerts', text: 'Support hearing-impaired users.' },
    ],
    flowSteps: [
      { title: 'Choose mode', text: 'Pick your preferred accessibility setup.' },
      { title: 'Save', text: 'Persist preferences.' },
      { title: 'Use everywhere', text: 'Apply settings across the app.' },
    ],
  },
  'health-card': {
    subtitle: 'Patient section',
    title: 'Health Card',
    description: 'A digital medical ID with blood group, allergies, and emergency contacts.',
    moduleLabel: 'Medical ID',
    focusText: 'Digital emergency card',
    dashboardRoute: '/patient/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Emergency ID flow',
    highlights: [
      { title: 'Identity', text: 'Name and core medical details.' },
      { title: 'Blood group', text: 'Visible in emergency situations.' },
      { title: 'Contacts', text: 'Quick emergency reach-out information.' },
    ],
    flowSteps: [
      { title: 'Load card', text: 'Open from the patient dashboard.' },
      { title: 'Show responders', text: 'Display details to helpers.' },
      { title: 'Use safely', text: 'Share essential data only.' },
    ],
  },
  'doctor-history': {
    subtitle: 'Doctor section',
    title: 'Patient History',
    description: 'Review treatment history, reports, and patient progress.',
    moduleLabel: 'Doctor records',
    focusText: 'Treatment timeline',
    dashboardRoute: '/doctor/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Clinical review flow',
    highlights: [
      { title: 'Treatment timeline', text: 'Review prior visits and prescriptions.' },
      { title: 'Reports', text: 'Open uploaded lab and imaging reports.' },
      { title: 'Progress', text: 'Track outcomes over time.' },
    ],
    flowSteps: [
      { title: 'Select patient', text: 'Open the record.' },
      { title: 'Review history', text: 'Examine treatments and reports.' },
      { title: 'Plan care', text: 'Prepare next treatment steps.' },
    ],
  },
  'monthly-reports': {
    subtitle: 'Doctor section',
    title: 'Monthly Reports',
    description: 'Generate monthly performance reports and export them as HTML files.',
    moduleLabel: 'Performance reporting',
    focusText: 'Monthly output',
    dashboardRoute: '/doctor/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Reporting flow',
    highlights: [
      { title: 'Appointments', text: 'Summarize monthly load.' },
      { title: 'Treatments', text: 'Capture diagnosis patterns.' },
      { title: 'Download', text: 'Export HTML reports.' },
    ],
    flowSteps: [
      { title: 'Choose month', text: 'Pick the reporting period.' },
      { title: 'Generate', text: 'Compile the report.' },
      { title: 'Download', text: 'Save the HTML file.' },
    ],
  },
  telemedicine: {
    subtitle: 'Doctor section',
    title: 'Telemedicine',
    description: 'Video consultation and message-based remote care.',
    moduleLabel: 'Remote care',
    focusText: 'Video + chat',
    dashboardRoute: '/doctor/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Telemedicine flow',
    highlights: [
      { title: 'Video calls', text: 'Launch a secure meeting link.' },
      { title: 'Chat', text: 'Exchange short messages.' },
      { title: 'Follow-up', text: 'Document notes and prescriptions.' },
    ],
    flowSteps: [
      { title: 'Schedule', text: 'Set a consultation time.' },
      { title: 'Consult', text: 'Meet remotely.' },
      { title: 'Document', text: 'Capture care notes.' },
    ],
  },
  'manage-doctors': {
    subtitle: 'Admin section',
    title: 'Manage Doctors',
    description: 'Add, update, blacklist, and remove doctors.',
    moduleLabel: 'Doctor management',
    focusText: 'CRUD actions',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Doctor administration flow',
    highlights: [
      { title: 'Add doctor', text: 'Register a new clinician.' },
      { title: 'Update doctor', text: 'Modify department and contact data.' },
      { title: 'Blacklist', text: 'Suspend doctors when necessary.' },
    ],
    flowSteps: [
      { title: 'Review', text: 'Check current roster.' },
      { title: 'Edit', text: 'Update details or status.' },
      { title: 'Publish', text: 'Save changes.' },
    ],
  },
  'manage-patients': {
    subtitle: 'Admin section',
    title: 'Manage Patients',
    description: 'Handle patient records, blacklist status, updates, and removals.',
    moduleLabel: 'Patient management',
    focusText: 'CRUD actions',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Patient administration flow',
    highlights: [
      { title: 'Search', text: 'Find patient records quickly.' },
      { title: 'Update', text: 'Edit contact and profile data.' },
      { title: 'Blacklist', text: 'Protect system integrity.' },
    ],
    flowSteps: [
      { title: 'Locate', text: 'Search the roster.' },
      { title: 'Update', text: 'Change patient details.' },
      { title: 'Secure', text: 'Apply access controls.' },
    ],
  },
  departments: {
    subtitle: 'Admin section',
    title: 'Departments',
    description: 'Organize hospital departments and services.',
    moduleLabel: 'Department management',
    focusText: 'Hospital structure',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Department configuration flow',
    highlights: [
      { title: 'Department list', text: 'Group services into care specialities.' },
      { title: 'Descriptions', text: 'Add clear operational notes.' },
      { title: 'Assignment', text: 'Map doctors to departments.' },
    ],
    flowSteps: [
      { title: 'Create', text: 'Add a department.' },
      { title: 'Assign', text: 'Attach doctors.' },
      { title: 'Maintain', text: 'Keep data current.' },
    ],
  },
  analytics: {
    subtitle: 'Admin section',
    title: 'Analytics',
    description: 'Track appointment trends, patient growth, and doctor performance.',
    moduleLabel: 'Analytics dashboard',
    focusText: 'Charts + metrics',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Analytics review flow',
    highlights: [
      { title: 'Appointment trends', text: 'Observe system load over time.' },
      { title: 'Patient growth', text: 'Track adoption and active users.' },
      { title: 'Doctor performance', text: 'Measure throughput and outcomes.' },
    ],
    flowSteps: [
      { title: 'Collect', text: 'Pull dashboard data.' },
      { title: 'Visualize', text: 'Render metrics and charts.' },
      { title: 'Act', text: 'Use insights to improve service.' },
    ],
  },
  'emergency-monitor': {
    subtitle: 'Admin section',
    title: 'Emergency Monitor',
    description: 'Observe live SOS alerts and patient locations.',
    moduleLabel: 'Emergency control',
    focusText: 'SOS tracking',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Emergency monitoring flow',
    highlights: [
      { title: 'Live alerts', text: 'Watch active SOS submissions.' },
      { title: 'Locations', text: 'Map patient coordinates.' },
      { title: 'Response', text: 'Track escalation and resolution.' },
    ],
    flowSteps: [
      { title: 'Alert', text: 'Receive SOS.' },
      { title: 'Locate', text: 'View patient position.' },
      { title: 'Respond', text: 'Coordinate assistance.' },
    ],
  },
  rooms: {
    subtitle: 'Admin section',
    title: 'Rooms',
    description: 'Track room allocation, type, and status across the hospital.',
    moduleLabel: 'Hospital rooms',
    focusText: 'Beds and wards',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Room management flow',
    highlights: [
      { title: 'Room number', text: 'Maintain a clean room inventory.' },
      { title: 'Type', text: 'Separate ICU, ward, and private rooms.' },
      { title: 'Status', text: 'Keep occupancy states current.' },
    ],
    flowSteps: [
      { title: 'Create room', text: 'Register a new room.' },
      { title: 'Assign status', text: 'Mark availability.' },
      { title: 'Use in admissions', text: 'Allocate to patients.' },
    ],
  },
  admissions: {
    subtitle: 'Admin section',
    title: 'Admissions',
    description: 'Register patient admissions, rooms, and discharge states.',
    moduleLabel: 'Admissions',
    focusText: 'Patient intake',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Admission workflow',
    highlights: [
      { title: 'Admit patient', text: 'Tie a patient to a room.' },
      { title: 'Discharge', text: 'Track when a patient leaves.' },
      { title: 'Audit trail', text: 'Keep the admission record visible.' },
    ],
    flowSteps: [
      { title: 'Admit', text: 'Create the admission entry.' },
      { title: 'Monitor', text: 'Track status in real time.' },
      { title: 'Discharge', text: 'Close the stay.' },
    ],
  },
  billing: {
    subtitle: 'Admin section',
    title: 'Billing',
    description: 'Combine consultation and medicine fees into a total bill.',
    moduleLabel: 'Hospital billing',
    focusText: 'Cost tracking',
    dashboardRoute: '/admin/dashboard',
    homeRoute: '/',
    accessibleFlowTitle: 'Billing flow',
    highlights: [
      { title: 'Consultation fees', text: 'Capture visit charges.' },
      { title: 'Medicine fees', text: 'Record pharmacy costs.' },
      { title: 'Total amount', text: 'Keep billing totals visible.' },
    ],
    flowSteps: [
      { title: 'Add charges', text: 'Enter individual fees.' },
      { title: 'Calculate total', text: 'Summarize the bill.' },
      { title: 'Record payment', text: 'Update billing status.' },
    ],
  },
}

export default {
  name: 'ModuleWorkspace',
  data() {
    return {
      accessibilityOptions: ['Voice navigation', 'Text to speech', 'High contrast', 'Large text', 'Vibration alerts'],
    }
  },
  computed: {
    config() {
      return moduleCatalog[this.$route.meta.moduleKey] || moduleCatalog['patient-profile']
    },
    title() {
      return this.$route.meta.title || this.config.title
    },
    subtitle() {
      return this.config.subtitle
    },
    description() {
      return this.config.description
    },
    moduleKey() {
      return this.$route.meta.moduleKey || 'patient-profile'
    },
    moduleLabel() {
      return this.config.moduleLabel
    },
    focusText() {
      return this.config.focusText
    },
    dashboardRoute() {
      return this.config.dashboardRoute
    },
    homeRoute() {
      return this.config.homeRoute
    },
    accessibleFlowTitle() {
      return this.config.accessibleFlowTitle
    },
    highlights() {
      return this.config.highlights
    },
    flowSteps() {
      return this.config.flowSteps
    },
  },
}
</script>

<style scoped>
.module-page {
  min-height: 100vh;
}

.module-header,
.panel-card,
.hero-strip {
  margin: 0 auto;
  max-width: 1320px;
}

.module-header {
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
  background: var(--health-surface);
  backdrop-filter: blur(16px);
  border: 1px solid var(--health-border);
  box-shadow: var(--health-shadow);
}

.hero-strip > div {
  padding: 1rem 1.2rem;
}

.hero-strip strong {
  display: block;
  margin-top: 0.35rem;
  font-size: 1.4rem;
}

.module-grid {
  display: grid;
  grid-template-columns: 1fr 0.85fr;
  gap: 1rem;
}

.panel-card {
  padding: 1.25rem;
}

.feature-list,
.flow-grid,
.action-stack {
  display: grid;
  gap: 0.9rem;
}

.feature-item,
.flow-step,
.health-card-preview,
.check-row {
  border-radius: 20px;
  border: 1px solid var(--health-border);
  padding: 1rem;
  background: rgba(15, 118, 110, 0.04);
}

.feature-item p,
.flow-step p {
  margin-bottom: 0;
  color: var(--health-muted);
}

.check-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.health-card-preview .card-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.65rem 0;
  border-bottom: 1px solid var(--health-border);
}

.health-card-preview .card-row:last-child {
  border-bottom: 0;
}

@media (max-width: 992px) {
  .module-header,
  .module-grid {
    grid-template-columns: 1fr;
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 768px) {
  .hero-strip {
    grid-template-columns: 1fr;
  }
}
</style>