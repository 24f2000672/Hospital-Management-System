<template>
  <div class="glass-page">
    <div class="container py-4">

      <div class="page-header mb-4">
        <h2>📈 Hospital Analytics</h2>
      </div>

      <div class="row">

        <div class="col-lg-3 col-md-6 mb-4">
          <div class="metric-box">
            <h3>{{ totalDoctors }}</h3>
            <p>Doctors</p>
          </div>
        </div>

        <div class="col-lg-3 col-md-6 mb-4">
          <div class="metric-box">
            <h3>{{ totalPatients }}</h3>
            <p>Patients</p>
          </div>
        </div>

        <div class="col-lg-3 col-md-6 mb-4">
          <div class="metric-box">
            <h3>{{ totalAppointments }}</h3>
            <p>Appointments</p>
          </div>
        </div>

        <div class="col-lg-3 col-md-6 mb-4">
          <div class="metric-box">
            <h3>₹{{ totalRevenue }}</h3>
            <p>Revenue</p>
          </div>
        </div>

      </div>

      <!-- Extra Analytics -->

      <div class="row mt-4">

        <div class="col-md-4 mb-4">
          <div class="glass-card">
            <h4>🏥 Departments</h4>
            <h2>{{ totalDepartments }}</h2>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="glass-card">
            <h4>🚨 SOS Alerts</h4>
            <h2>{{ totalSOS }}</h2>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="glass-card">
            <h4>🛏 Active Admissions</h4>
            <h2>{{ totalAdmissions }}</h2>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Analytics",

  data() {
    return {
      totalDoctors: 0,
      totalPatients: 0,
      totalAppointments: 0,
      totalRevenue: 0,
      totalDepartments: 0,
      totalSOS: 0,
      totalAdmissions: 0,
    };
  },

  mounted() {
    this.loadAnalytics();
  },

  methods: {
    async loadAnalytics() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await axios.get(
          "http://127.0.0.1:5000/admin/analytics",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.totalDoctors =
          response.data.total_doctors || 0;

        this.totalPatients =
          response.data.total_patients || 0;

        this.totalAppointments =
          response.data.total_appointments || 0;

        this.totalRevenue =
          response.data.total_revenue || 0;

        this.totalDepartments =
          response.data.total_departments || 0;

        this.totalSOS =
          response.data.total_sos || 0;

        this.totalAdmissions =
          response.data.total_admissions || 0;

      } catch (error) {
        console.error(
          "Analytics loading failed:",
          error
        );
      }
    },
  },
};
</script>

<style scoped>
.glass-page {
  min-height: 100vh;
  padding: 20px;

  background:
    radial-gradient(circle at top left,
      rgba(45, 212, 191, 0.24),
      transparent 28%),
    radial-gradient(circle at top right,
      rgba(249, 115, 22, 0.25),
      transparent 28%),
    linear-gradient(
      160deg,
      #08111f 0%,
      #0f2a3b 48%,
      #123b52 100%
    );
}

.page-header {
  color: white;
}

.metric-box {
  text-align: center;
  padding: 25px;
  border-radius: 20px;

  background: rgba(255,255,255,0.08);

  backdrop-filter: blur(16px);

  border: 1px solid rgba(
    255,
    255,
    255,
    0.15
  );

  color: white;

  box-shadow: 0 8px 25px rgba(
    0,
    0,
    0,
    0.25
  );
}

.metric-box h3 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.metric-box p {
  margin: 0;
  font-size: 1rem;
}

.glass-card {
  text-align: center;
  padding: 20px;
  border-radius: 20px;

  background: rgba(255,255,255,0.08);

  backdrop-filter: blur(16px);

  border: 1px solid rgba(
    255,
    255,
    255,
    0.15
  );

  color: white;

  box-shadow: 0 8px 25px rgba(
    0,
    0,
    0,
    0.25
  );
}

.glass-card h2 {
  margin-top: 15px;
}
</style>