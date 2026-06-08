<template>
  <div class="glass-page">
    <div class="container py-4">

      <div class="page-header mb-4">
        <h2>🏥 Departments Management</h2>
        <button
      class="btn btn-secondary"
      @click="goDashboard"
    >
      🏠 Dashboard
    </button>
        <button class="btn btn-success" @click="addDepartment">
          ➕ Add Department
        </button>
      </div>

      <div class="row">
        <div
          class="col-lg-4 col-md-6 mb-4"
          v-for="dept in departments"
          :key="dept.id"
        >
          <div class="glass-card h-100">

            <h4>{{ dept.name }}</h4>

            <p class="text-muted">
              {{ dept.description }}
            </p>

            <div class="mt-auto d-flex gap-2">
              <button
                class="btn btn-primary btn-sm"
                @click="manageDepartment(dept)"
              >
                Manage
              </button>

              <button
                class="btn btn-warning btn-sm"
                @click="editDepartment(dept)"
              >
                Edit
              </button>

              <button
                class="btn btn-danger btn-sm"
                @click="deleteDepartment(dept.id)"
              >
                Delete
              </button>
            </div>

          </div>
        </div>
      </div>

      <div
        v-if="departments.length === 0"
        class="text-center mt-5"
      >
        <h5>No Departments Found</h5>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Departments",

  data() {
    return {
      departments: [],
    };
  },

  mounted() {
    this.fetchDepartments();
  },

  methods: {
    async fetchDepartments() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await axios.get(
          "http://127.0.0.1:5000/admin/departments",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.departments = response.data || [];
      } catch (error) {
        console.error("Error loading departments:", error);
      }
    },

    addDepartment() {
      this.$router.push("/admin/add-department");
    },

    manageDepartment(dept) {
      this.$router.push(
        `/admin/manage-department/${dept.id}`
      );
    },

    editDepartment(dept) {
      this.$router.push(
        `/admin/edit-department/${dept.id}`
      );
    },
    goDashboard() {
      this.$router.push("/admin/dashboard");
    },  
    async deleteDepartment(id) {
      if (!confirm("Delete this department?")) return;

      try {
        const token = localStorage.getItem("access_token");

        await axios.delete(
          `http://127.0.0.1:5000/admin/departments/${id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.fetchDepartments();

      } catch (error) {
        console.error("Delete error:", error);
        alert("Unable to delete department");
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.glass-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px;
  border-radius: 20px;

  backdrop-filter: blur(16px);

  background: rgba(255, 255, 255, 0.08);

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
    0.2
  );
}

.glass-card h4 {
  margin-bottom: 12px;
}

.text-muted {
  color: rgba(
    255,
    255,
    255,
    0.75
  ) !important;
}
</style>