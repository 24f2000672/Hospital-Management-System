<template>
  <div class="glass-page">
    <div class="container py-4">

      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="page-title">🏥 Admissions Management</h2>

        <div>
          <button
            class="btn btn-secondary me-2"
            @click="$router.push('/admin/dashboard')"
          >
            🏠 Dashboard
          </button>

          <button
            class="btn btn-success"
            @click="$router.push('/admin/add-admission')"
          >
            ➕ Add Admission
          </button>
        </div>
      </div>

      <!-- Search -->
      <input
        v-model="search"
        class="form-control mb-4"
        placeholder="🔍 Search patient, room or status..."
      />

      <!-- Loading -->
      <div
        v-if="loading"
        class="text-center text-white"
      >
        Loading admissions...
      </div>

      <!-- Table -->
      <div
        v-else
        class="table-responsive"
      >
        <table
          class="table table-dark table-hover align-middle"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Patient</th>
              <th>Room</th>
              <th>Admission Date</th>
              <th>Discharge Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="admission in filteredAdmissions"
              :key="admission.id"
            >
              <td>{{ admission.id }}</td>

              <td>
                {{ admission.patient_name }}
              </td>

              <td>
                {{ admission.room_number }}
              </td>

              <td>
                {{ admission.admission_date }}
              </td>

              <td>
                {{
                  admission.discharge_date ||
                  "N/A" 
                }}
              </td>

              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-success':
                      admission.status === 'ADMITTED',

                    'bg-danger':
                      admission.status === 'DISCHARGED'
                  }"
                >
                  {{ admission.status }}
                </span>
              </td>

              <td>

                <button
                  class="btn btn-warning btn-sm me-2"
                  @click="editAdmission(admission.id)"
                >
                  ✏ Edit
                </button>

                <button
                  class="btn btn-danger btn-sm"
                  @click="deleteAdmission(admission.id)"
                >
                  🗑 Delete
                </button>

              </td>
            </tr>

          </tbody>
        </table>
      </div>

      <div
        v-if="
          !loading &&
          filteredAdmissions.length === 0
        "
        class="text-center text-white mt-4"
      >
        No Admissions Found
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdmissionsView",

  data() {
    return {
      admissions: [],
      loading: true,
      search: ""
    };
  },

  computed: {

    filteredAdmissions() {

      if (!this.search) {
        return this.admissions;
      }

      const searchText =
        this.search.toLowerCase().trim();

      return this.admissions.filter(admission => {

        return (

          String(admission.patient_name || "")
            .toLowerCase()
            .includes(searchText)

          ||

          String(admission.room_number || "")
            .toLowerCase()
            .includes(searchText)

          ||

          String(admission.status || "")
            .toLowerCase()
            .includes(searchText)

          ||

          String(admission.id || "")
            .includes(searchText)

        );

      });

    }

  },

  async mounted() {
    await this.loadAdmissions();
  },

  methods: {

    // ================= LOAD ADMISSIONS =================

    async loadAdmissions() {

      try {

        this.loading = true;

        const token =
          localStorage.getItem("access_token");

        const response = await axios.get(
          "http://127.0.0.1:5000/api/admissions",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.admissions = response.data;

        console.log(
          "Admissions Loaded:",
          response.data
        );

      } catch (error) {

        console.error(
          "LOAD ADMISSIONS ERROR:",
          error.response?.data ||
          error.message
        );

        alert("Failed to load admissions");

      } finally {

        this.loading = false;

      }
    },

    // ================= EDIT ADMISSION =================

    editAdmission(id) {

      this.$router.push(
        `/admin/admissions/edit/${id}`
      );

    },

    // ================= DELETE ADMISSION =================

    async deleteAdmission(id) {

      const confirmDelete = confirm(
        "Are you sure you want to delete this admission?"
      );

      if (!confirmDelete) {
        return;
      }

      try {

        const token =
          localStorage.getItem("access_token");

        await axios.delete(
          `http://127.0.0.1:5000/api/admissions/${id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert(
          "Admission deleted successfully"
        );

        await this.loadAdmissions();

      } catch (error) {

        console.error(
          "DELETE ADMISSION ERROR:",
          error.response?.data ||
          error.message
        );

        alert("Failed to delete admission");
      }
    },

    // ================= DASHBOARD =================

    goDashboard() {

      this.$router.push(
        "/admin/dashboard"
      );

    }

  }
};
</script>

<style scoped>
.glass-page {
  min-height: 100vh;
  padding: 30px;

  background:
    radial-gradient(
      circle at top left,
      rgba(45,212,191,.25),
      transparent 30%
    ),
    radial-gradient(
      circle at top right,
      rgba(249,115,22,.25),
      transparent 30%
    ),
    linear-gradient(
      160deg,
      #08111f 0%,
      #0f2a3b 50%,
      #123b52 100%
    );
}

.page-title {
  color: white;
  font-weight: 700;
}

.table {
  border-radius: 15px;
  overflow: hidden;
}

.form-control {
  background: rgba(
    255,
    255,
    255,
    0.1
  );
  color: white;
  border: none;
}

.form-control::placeholder {
  color: #d1d5db;
}

.form-control:focus {
  background: rgba(
    255,
    255,
    255,
    0.15
  );
  color: white;
  box-shadow: none;
}

.badge {
  padding: 8px 12px;
  font-size: 0.85rem;
}
</style>