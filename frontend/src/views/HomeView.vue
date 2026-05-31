<template>
  <div class="landing-page">
    <header class="landing-topbar container-fluid px-4 px-lg-5 py-3">
      <div class="brand-lockup">
        <img src="@/assets/logo.png" alt="Health Guardian+ logo" class="brand-mark" />
        <div>
          <p class="eyebrow mb-1">Health Guardian+</p>
          <h1 class="brand-title mb-0">Smart healthcare, emergency response, and accessibility</h1>
        </div>
      </div>

      <nav class="landing-actions d-flex flex-wrap gap-2">
        <router-link to="/login" class="btn btn-light btn-lg">Patient Login</router-link>
        <router-link to="/login" class="btn btn-outline-light btn-lg">Doctor Login</router-link>
        <router-link to="/login" class="btn btn-outline-light btn-lg">Admin Login</router-link>
      </nav>
    </header>

    <main class="container-fluid px-4 px-lg-5 pb-5">
      <section class="hero-grid">
        <div class="hero-copy">
          <span class="hero-pill">Emergency SOS, telemedicine, and inclusive care in one platform</span>
          <h2>
            A complete healthcare ecosystem for patients, clinicians, and administrators.
          </h2>
          <p class="hero-text">
            Manage appointments, monitor treatment progress, trigger live SOS alerts, track health
            records, and support specially-abled users with a single connected experience.
          </p>

          <div class="d-flex flex-wrap gap-3 mt-4">
            <router-link to="/register" class="btn btn-primary btn-lg">Create patient account</router-link>
            <router-link to="/login" class="btn btn-outline-light btn-lg">Enter dashboard</router-link>
          </div>

          <div class="hero-metrics mt-5">
            <div class="metric-card">
              <strong>24/7</strong>
              <span>Emergency-ready support</span>
            </div>
            <div class="metric-card">
              <strong>3 roles</strong>
              <span>Patient, Doctor, Admin</span>
            </div>
            <div class="metric-card">
              <strong>Accessible</strong>
              <span>Voice, visual, and high-contrast flows</span>
            </div>
          </div>
        </div>

        <aside class="hero-panel">
          <div class="panel-surface">
            <p class="panel-label mb-2">Platform highlights</p>
            <ul class="feature-stack">
              <li>
                <span>Emergency SOS</span>
                <small>Live GPS alerts and contact notifications</small>
              </li>
              <li>
                <span>Smart appointments</span>
                <small>Slot tracking, booking, cancellation, and doctor schedules</small>
              </li>
              <li>
                <span>Personal health records</span>
                <small>Prescriptions, allergies, chronic conditions, and reports</small>
              </li>
              <li>
                <span>Accessible care</span>
                <small>Voice navigation, visual alerts, and simplified UI modes</small>
              </li>
            </ul>
          </div>
        </aside>
      </section>

      <section class="section-block">
        <div class="section-heading">
          <p class="eyebrow mb-1">What it does</p>
          <h3 class="mb-0">Built for the full healthcare journey</h3>
        </div>

        <div class="feature-grid">
          <article class="feature-card">
            <span class="feature-tag">Patient</span>
            <h4>Personal care hub</h4>
            <p>Book appointments, store medical records, receive medicine reminders, and trigger SOS instantly.</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">Doctor</span>
            <h4>Clinical workflow</h4>
            <p>Manage slots, record treatments, review patient history, and generate monthly performance reports.</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">Admin</span>
            <h4>Operational control</h4>
            <p>Oversee doctors, patients, appointments, SOS events, security, and analytics from one console.</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">AI</span>
            <h4>Symptom insight</h4>
            <p>Guide users with basic symptom analysis, risk alerts, and future-ready chatbot integration.</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">Mobile</span>
            <h4>Always available</h4>
            <p>Android-ready Ionic Vue workflows with push notifications, offline medical ID, and dark mode support.</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">Access</span>
            <h4>Inclusive by design</h4>
            <p>Supports blind, deaf, mute, and elderly users with tailored navigation and emergency communication.</p>
          </article>
        </div>
      </section>

      <section class="section-block">
        <div class="section-heading">
          <p class="eyebrow mb-1">Who uses it</p>
          <h3 class="mb-0">Three roles, one coordinated platform</h3>
        </div>

        <div class="role-grid">
          <article class="role-card role-patient">
            <h4>Patients</h4>
            <p>Appointments, prescriptions, reminders, records, report downloads, and emergency SOS.</p>
          </article>
          <article class="role-card role-doctor">
            <h4>Doctors</h4>
            <p>Appointment handling, treatment notes, patient history, telemedicine, and reports.</p>
          </article>
          <article class="role-card role-admin">
            <h4>Administrators</h4>
            <p>User management, analytics, department oversight, security controls, and hospital monitoring.</p>
          </article>
        </div>
      </section>

      <section class="callout-banner">
        <div>
          <p class="eyebrow mb-1">Emergency first</p>
          <h3 class="mb-2">One-touch SOS with location-aware escalation</h3>
          <p class="mb-0">
            Health Guardian+ is designed to help users act fast when every second matters.
          </p>
        </div>
        <router-link to="/register" class="btn btn-light btn-lg">Get started</router-link>
      </section>
    </main>
  </div>
</template>

<script setup></script>

<style scoped>
.landing-page {
  min-height: 100vh;
  color: #f4fbff;
  background:
    radial-gradient(circle at top left, rgba(45, 212, 191, 0.24), transparent 28%),
    radial-gradient(circle at top right, rgba(249, 115, 22, 0.25), transparent 28%),
    linear-gradient(160deg, #08111f 0%, #0f2a3b 48%, #123b52 100%);
}

.landing-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-mark {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.72rem;
  color: rgba(240, 249, 255, 0.72);
}

.brand-title,
.hero-copy h2,
.section-heading h3,
.callout-banner h3 {
  font-family: Georgia, 'Times New Roman', serif;
}

.brand-title {
  font-size: 1.2rem;
  max-width: 34rem;
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(280px, 0.9fr);
  gap: 1.5rem;
  align-items: stretch;
  padding-top: 2rem;
}

.hero-copy,
.hero-panel,
.callout-banner,
.feature-card,
.role-card {
  backdrop-filter: blur(18px);
}

.hero-copy {
  padding: 2rem 0;
}

.hero-pill,
.feature-tag,
.panel-label {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border-radius: 999px;
  padding: 0.35rem 0.8rem;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #ecfeff;
}

.hero-copy h2 {
  margin: 1rem 0 0;
  font-size: clamp(2.6rem, 4vw, 4.8rem);
  line-height: 0.98;
  max-width: 12ch;
}

.hero-text {
  margin-top: 1.25rem;
  max-width: 58rem;
  font-size: 1.05rem;
  color: rgba(240, 249, 255, 0.8);
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.metric-card,
.panel-surface,
.feature-card,
.role-card,
.callout-banner {
  border-radius: 28px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(4, 12, 20, 0.42);
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.22);
}

.metric-card {
  padding: 1rem 1.1rem;
}

.metric-card strong {
  display: block;
  font-size: 1.35rem;
  color: #f8fafc;
}

.metric-card span {
  color: rgba(240, 249, 255, 0.7);
  font-size: 0.92rem;
}

.hero-panel {
  display: flex;
  align-items: center;
}

.panel-surface {
  width: 100%;
  padding: 1.25rem;
}

.feature-stack {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
  display: grid;
  gap: 0.85rem;
}

.feature-stack li {
  padding: 1rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.feature-stack span {
  display: block;
  font-weight: 700;
  color: #f8fafc;
}

.feature-stack small {
  display: block;
  color: rgba(240, 249, 255, 0.72);
  margin-top: 0.35rem;
}

.section-block {
  margin-top: 2.5rem;
}

.section-heading {
  margin-bottom: 1rem;
}

.section-heading h3 {
  font-size: clamp(1.8rem, 2.5vw, 2.5rem);
}

.feature-grid,
.role-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.feature-card,
.role-card {
  padding: 1.25rem;
  min-height: 190px;
}

.feature-card h4,
.role-card h4 {
  margin: 1rem 0 0.5rem;
  font-size: 1.15rem;
}

.feature-card p,
.role-card p,
.callout-banner p {
  color: rgba(240, 249, 255, 0.76);
  margin-bottom: 0;
}

.feature-card:nth-child(2),
.role-doctor {
  border-color: rgba(45, 212, 191, 0.28);
}

.feature-card:nth-child(3),
.role-admin {
  border-color: rgba(249, 115, 22, 0.28);
}

.callout-banner {
  margin-top: 2rem;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.2rem;
}

@media (max-width: 992px) {
  .hero-grid,
  .feature-grid,
  .role-grid {
    grid-template-columns: 1fr;
  }

  .hero-metrics {
    grid-template-columns: 1fr;
  }

  .landing-topbar,
  .callout-banner {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 576px) {
  .hero-copy h2 {
    font-size: 2.2rem;
  }

  .brand-lockup {
    align-items: flex-start;
  }

  .brand-mark {
    width: 58px;
    height: 58px;
  }
}
</style>
