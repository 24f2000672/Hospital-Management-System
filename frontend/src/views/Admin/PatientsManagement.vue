<template>
  <div class="glass-page">
    <div class="page-header">

  <h2 class="title">🧑 Patients Management</h2>

  <button
    class="btn btn-secondary"
    @click="goDashboard"
  >
    🏠 Dashboard
  </button>

</div>
    <div class="glass-card">

      <table class="table table-hover table-dark">

        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
            <th>Gender</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="patient in patients" :key="patient.id">

            <td>{{ patient.id }}</td>
            <td>{{ patient.first_name }} {{ patient.last_name }}</td>
            <td>{{ patient.age }}</td>
            <td>{{ patient.gender }}</td>
            <td>{{ patient.phone }}</td>

            <td>

              <!-- ✅ EDIT (redirect to AdminEditPatient.vue) -->
              <button
                class="btn btn-warning btn-sm me-2"
                @click="editPatient(patient.id)"
              >
                Edit
              </button>

              <!-- ❌ DELETE -->
              <button
                class="btn btn-danger btn-sm"
                @click="deletePatient(patient.id)"
              >
                Delete
              </button>

            </td>

          </tr>
        </tbody>

      </table>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PatientsManagement",

  data() {
    return {
      patients: []
    };
  },

  mounted() {
    this.loadPatients();
  },

  methods: {

    // ---------------- LOAD PATIENTS ----------------
    async loadPatients() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await axios.get(
          "http://127.0.0.1:5000/patients",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.patients = response.data;

      } catch (error) {
        console.error("Failed to load patients:", error);
      }
    },

    // ---------------- EDIT (REDIRECT) ----------------
    editPatient(id) {
      this.$router.push({
        name: "admin-edit-patient",
        params: { id }
      });
    },
    goDashboard() {
  this.$router.push("/admin/dashboard");
},
    // ---------------- DELETE ----------------
    async deletePatient(id) {
      if (!confirm("Are you sure you want to delete this patient?")) return;

      try {
        const token = localStorage.getItem("access_token");

        await axios.delete(
          `http://127.0.0.1:5000/patients/${id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        // refresh list
        this.loadPatients();

      } catch (error) {
        console.error("Delete failed:", error);
      }
    }
  }
};
</script>

<style scoped>
.glass-page {
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(160deg, #08111f, #0f2a3b);
}

.title {
  color: white;
  margin-bottom: 20px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(14px);
  border-radius: 15px;
  padding: 20px;
  color: white;
}

table {
  color: white;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  margin: 0;
}
</style>