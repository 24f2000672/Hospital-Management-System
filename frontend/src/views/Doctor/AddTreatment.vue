<template>
  <main>
    <h1>Patient Dashboard</h1>
    <p>
      Welcome to your dashboard! Here you can view your upcoming appointments and manage your
      profile.
    </p>
    <div class="dashboard-section">
      <h2>Upcoming Appointments</h2>
      <ul>
        <li v-for="appointment in appointments" :key="appointment.id">
          <strong>{{ appointment.doctor_name }}</strong> - {{ formatDate(appointment.date) }} at
          {{ appointment.time }}
        </li>
      </ul>
    </div>
    <div class="dashboard-section">
      <h2>Profile Management</h2>
      <p>You can update your profile information and change your password here.</p>
      <button class="btn btn-primary" @click="goToProfile">Go to Profile</button>
    </div>
    <div class="dashboard-section mt-4">
      <h2>Medical History</h2>
      <p>You can view your medical history here.</p>
      <button class="btn btn-secondary" @click="goToHistory">View History</button>
    </div>
  </main>
</template>
