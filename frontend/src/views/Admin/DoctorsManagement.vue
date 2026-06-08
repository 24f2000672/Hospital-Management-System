<template>
  <div class="glass-page">

    <!-- Header -->
    <div class="page-header">
      <div>
        <h2>👨‍⚕️ Doctors Management</h2>
        <p class="text-light opacity-75">
          Manage doctor profiles, departments, and hospital staff.
        </p>
      </div>
       <button
      class="btn btn-secondary"
      @click="goDashboard"
    >
      🏠 Dashboard
    </button>

      <button
  class="btn btn-success"
  @click="addDoctor"
>
  ➕ Add Doctor
</button>
    </div>

    <!-- Stats -->
    <div class="row mb-4">

      <div class="col-md-4">
        <div class="metric-card">
          <h3>{{ doctors.length }}</h3>
          <p>Total Doctors</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="metric-card">
          <h3>{{ activeDoctors }}</h3>
          <p>Active Doctors</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="metric-card">
          <h3>{{ departments }}</h3>
          <p>Departments</p>
        </div>
      </div>

    </div>

    <!-- Doctor Table -->
    <div class="glass-card">

      <div class="table-responsive">

        <table class="table table-dark table-hover align-middle">

          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Department</th>
              <th>Experience</th>
              <th>Contact</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="doctor in doctors"
              :key="doctor.id"
            >
              <td>{{ doctor.id }}</td>

              <td>
                <strong>
                  {{ doctor.first_name }}
                  {{ doctor.last_name }}
                </strong>
              </td>

              <td>{{ doctor.department }}</td>

              <td>
                {{ doctor.experience }} Years
              </td>

              <td>{{ doctor.contact }}</td>

              <td>
                <span class="badge bg-success">
                  Active
                </span>
              </td>

              <td>

                <button
                  class="btn btn-warning btn-sm me-2"
                  @click="editDoctor(doctor.id)"
                >
                  ✏ Edit
                </button>

                <button
                  class="btn btn-danger btn-sm"
                  @click="deleteDoctor(doctor.id)"
                >
                  🗑 Delete
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
  name: "DoctorsManagement",

  data() {
    return {
      doctors: [],
      activeDoctors: 0,
      departments: 0,
    };
  },

  async mounted() {
    await this.fetchDoctors();
  },

  methods: {
    async fetchDoctors() {
      try {
        const token = localStorage.getItem("access_token");

        const res = await axios.get(
          "http://127.0.0.1:5000/admin/doctors",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.doctors = res.data.doctors || [];

        this.activeDoctors = this.doctors.length;

        const uniqueDepartments = [
          ...new Set(this.doctors.map((d) => d.department)),
        ];

        this.departments = uniqueDepartments.length;
      } catch (err) {
        console.error(err);
      }
    },
    
     goDashboard() {
      this.$router.push("/admin/dashboard");
    },
    addDoctor() {
      this.$router.push("/admin/doctors");
    },

    editDoctor(id) {
      this.$router.push(`/admin/update-doctor?id=${id}`);
    },

    async deleteDoctor(id) {
      if (!confirm("Delete this doctor?")) return;

      try {
        const token = localStorage.getItem("access_token");

        await axios.delete(
          `http://127.0.0.1:5000/delete_doctor/${id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        await this.fetchDoctors();

        alert("Doctor deleted successfully");
      } catch (err) {
        console.error(err);
        alert("Failed to delete doctor");
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
    #021b3a,
    #032d5a,
    #061a33
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
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid rgba(255,255,255,0.1);
}

.metric-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(20px);
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
  margin-bottom: 0;
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