<template>
  <div class="glass-page">

    <h2 class="title">✏️ Edit Patient</h2>

    <div class="glass-card" v-if="patient">

      <form @submit.prevent="updatePatient">

        <!-- First Name -->
        <div class="mb-3">
          <label>First Name</label>
          <input
            v-model="patient.first_name"
            type="text"
            class="form-control"
            required
          />
        </div>

        <!-- Last Name -->
        <div class="mb-3">
          <label>Last Name</label>
          <input
            v-model="patient.last_name"
            type="text"
            class="form-control"
            required
          />
        </div>

        <!-- Age -->
        <div class="mb-3">
          <label>Age</label>
          <input
            v-model="patient.age"
            type="number"
            class="form-control"
            required
          />
        </div>

        <!-- Gender -->
        <div class="mb-3">
          <label>Gender</label>
          <select v-model="patient.gender" class="form-control" required>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>

        <!-- Phone -->
        <div class="mb-3">
          <label>Phone</label>
          <input
            v-model="patient.phone"
            type="text"
            class="form-control"
            required
          />
        </div>

        <!-- Buttons -->
        <button type="submit" class="btn btn-success">
          💾 Save Changes
        </button>

        <button
          type="button"
          class="btn btn-secondary ms-2"
          @click="$router.push('/admin/manage-patients')"
        >
          Cancel
        </button>

      </form>

    </div>

    <div v-else class="text-white">
      Loading patient...
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminEditPatient",

  data() {
    return {
      patient: null
    };
  },

  mounted() {
    this.loadPatient();
  },

  methods: {

    // ---------------- FETCH PATIENT ----------------
    async loadPatient() {
      try {
        const token = localStorage.getItem("access_token");

        const id = this.$route.params.id;

        const response = await axios.get(
          `http://127.0.0.1:5000/patients/${id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.patient = response.data;

      } catch (error) {
        console.error("Failed to load patient:", error);
      }
    },

    // ---------------- UPDATE PATIENT ----------------
    async updatePatient() {
      try {
        const token = localStorage.getItem("access_token");

        const id = this.$route.params.id;

        await axios.put(
          `http://127.0.0.1:5000/patients/${id}`,
          this.patient,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert("Patient updated successfully!");

        this.$router.push("/admin/manage-patients");

      } catch (error) {
        console.error("Update failed:", error);
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
  padding: 20px;
  border-radius: 15px;
  color: white;
  backdrop-filter: blur(12px);
}

label {
  margin-bottom: 5px;
  font-weight: 500;
  color: #ddd;
}
</style>