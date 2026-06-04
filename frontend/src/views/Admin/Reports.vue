<template>
  <div class="glass-page">
    <div class="container py-4">

      <div class="page-header mb-4">
        <h2>📊 Reports Center</h2>
      </div>

      <div class="row">

        <!-- Patient Reports -->
        <div class="col-lg-4 col-md-6 mb-4">
          <div class="glass-card">
            <h4>👨‍⚕️ Patient Reports</h4>
            <p>Total Patients: {{ reportStats.total_patients }}</p>

            <button
              class="btn btn-primary"
              @click="exportPatients"
            >
              Export CSV
            </button>
          </div>
        </div>

        <!-- Doctor Reports -->
        <div class="col-lg-4 col-md-6 mb-4">
          <div class="glass-card">
            <h4>🩺 Doctor Reports</h4>
            <p>Total Doctors: {{ reportStats.total_doctors }}</p>

            <button
              class="btn btn-success"
              @click="generateDoctorReport"
            >
              Generate Report
            </button>
          </div>
        </div>

        <!-- Revenue Reports -->
        <div class="col-lg-4 col-md-6 mb-4">
          <div class="glass-card">
            <h4>💰 Revenue Reports</h4>
            <p>Total Revenue: ₹{{ reportStats.total_revenue }}</p>

            <button
              class="btn btn-warning"
              @click="downloadRevenueReport"
            >
              Download PDF
            </button>
          </div>
        </div>

      </div>

      <!-- Recent Reports -->
      <div class="glass-card mt-4">
        <h4>📁 Generated Reports</h4>

        <table class="table table-dark table-hover mt-3">
          <thead>
            <tr>
              <th>ID</th>
              <th>Report Name</th>
              <th>Generated On</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="report in reports"
              :key="report.id"
            >
              <td>{{ report.id }}</td>
              <td>{{ report.name }}</td>
              <td>{{ report.created_at }}</td>

              <td>
                <button
                  class="btn btn-sm btn-info"
                  @click="downloadReport(report)"
                >
                  Download
                </button>
              </td>
            </tr>

            <tr v-if="reports.length === 0">
              <td colspan="4" class="text-center">
                No Reports Available
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
  name: "Reports",

  data() {
    return {
      reports: [],

      reportStats: {
        total_patients: 0,
        total_doctors: 0,
        total_revenue: 0,
      },
    };
  },

  mounted() {
    this.fetchReports();
  },

  methods: {
    async fetchReports() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await axios.get(
          "http://127.0.0.1:5000/admin/reports",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.reportStats = response.data.stats || {};
        this.reports = response.data.reports || [];
      } catch (error) {
        console.error("Error loading reports:", error);
      }
    },

    exportPatients() {
      window.open(
        "http://127.0.0.1:5000/admin/export/patients",
        "_blank"
      );
    },

    generateDoctorReport() {
      alert("Doctor report generated successfully.");
    },

    downloadRevenueReport() {
      window.open(
        "http://127.0.0.1:5000/admin/export/revenue",
        "_blank"
      );
    },

    downloadReport(report) {
      window.open(
        `http://127.0.0.1:5000/admin/download-report/${report.id}`,
        "_blank"
      );
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

.glass-card {
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

.table {
  color: white;
}

.btn {
  margin-top: 10px;
}
</style>