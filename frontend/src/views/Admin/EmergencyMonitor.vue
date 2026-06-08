<template>
  <div class="glass-page">

    <!-- Header -->
    <div class="page-header">
      <div>
        <h2>🚨 Emergency Monitor</h2>
        <p class="text-light opacity-75">
          Monitor SOS alerts and emergency requests in real time.
        </p>
      </div>

      <button class="btn btn-danger">
        🔴 Live Monitoring
      </button>
    </div>

    <!-- Statistics -->
    <div class="row mb-4">

      <div class="col-md-4">
        <div class="metric-card">
          <h3>{{ activeAlerts }}</h3>
          <p>Active Emergencies</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="metric-card">
          <h3>{{ resolvedAlerts }}</h3>
          <p>Resolved Cases</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="metric-card">
          <h3>{{ totalAlerts }}</h3>
          <p>Total Alerts</p>
        </div>
      </div>

    </div>

    <!-- Emergency Alerts Table -->
    <div class="glass-card">

      <h4 class="mb-3">📍 Emergency Alerts</h4>

      <div class="table-responsive">

        <table class="table table-dark table-hover align-middle">

          <thead>
            <tr>
              <th>ID</th>
              <th>Patient</th>
              <th>Location</th>
              <th>Emergency Type</th>
              <th>Time</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="alert in alerts"
              :key="alert.id"
            >
              <td>{{ alert.id }}</td>

              <td>{{ alert.patient_name }}</td>

              <td>{{ alert.location }}</td>

              <td>{{ alert.emergency_type }}</td>

              <td>{{ alert.time }}</td>

              <td>
                <span
                  class="badge"
                  :class="
                    alert.status === 'ACTIVE'
                      ? 'bg-danger'
                      : 'bg-success'
                  "
                >
                  {{ alert.status }}
                </span>
              </td>

              <td>

                <button
                  v-if="alert.status === 'ACTIVE'"
                  class="btn btn-success btn-sm"
                  @click="resolveAlert(alert.id)"
                >
                  ✓ Resolve
                </button>

                <button
                  v-else
                  class="btn btn-secondary btn-sm"
                  disabled
                >
                  Resolved
                </button>

              </td>
            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EmergencyMonitor",

  data() {
    return {
      alerts: [],
      activeAlerts: 0,
      resolvedAlerts: 0,
      totalAlerts: 0,
    };
  },

  mounted() {
    this.fetchAlerts();
  },

  methods: {
    async fetchAlerts() {
      try {
        const token = localStorage.getItem("access_token");

        const res = await axios.get(
          "http://127.0.0.1:5000/admin/emergency-monitor",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.alerts = res.data.alerts || [];

        this.totalAlerts = this.alerts.length;

        this.activeAlerts = this.alerts.filter(
          (a) => a.status === "ACTIVE"
        ).length;

        this.resolvedAlerts = this.alerts.filter(
          (a) => a.status === "RESOLVED"
        ).length;
      } catch (error) {
        console.error(error);
      }
    },

    async resolveAlert(id) {
      try {
        const token = localStorage.getItem("access_token");

        await axios.put(
          `http://127.0.0.1:5000/admin/emergency-monitor/${id}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.fetchAlerts();
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>

.glass-page {
  min-height: 100vh;
  padding: 30px;
  background: linear-gradient(
    135deg,
    #08111f,
    #0f2a3b,
    #123b52
  );
  color: white;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.glass-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(18px);
  border-radius: 24px;
  padding: 25px;
  border: 1px solid rgba(255,255,255,0.1);
}

.metric-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(18px);
  border-radius: 20px;
  padding: 25px;
  text-align: center;
  margin-bottom: 20px;
}

.metric-card h3 {
  font-size: 2rem;
  font-weight: bold;
}

.metric-card p {
  margin: 0;
  opacity: 0.8;
}

.table {
  color: white;
}

.table thead {
  background: rgba(255,255,255,0.08);
}

.table tbody tr {
  background: rgba(255,255,255,0.03);
}

.table tbody tr:hover {
  background: rgba(255,255,255,0.08);
}

</style>