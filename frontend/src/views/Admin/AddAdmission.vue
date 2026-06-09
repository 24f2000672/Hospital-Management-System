<template>
  <div class="glass-page">
    <div class="container py-4">

      <h2 class="page-title mb-4">➕ Add Admission</h2>

      <div class="glass-card p-4">

        <!-- Patient -->
        <label class="form-label">Patient</label>
        <select v-model="form.patient_id" class="form-control mb-3">
          <option value="" disabled>Select Patient</option>
         <option
  v-for="p in patients"
  :key="p.id"
  :value="p.id"
>
  {{ p.name}}
</option>
        </select>

        <!-- Room -->
        <label class="form-label">Room</label>
        <select v-model="form.room_id" class="form-control mb-3">
          <option value="" disabled>Select Room</option>
          <option
            v-for="r in rooms"
            :key="r.id"
            :value="r.id"
          >
            {{ r.room_number }} ({{ r.type }})
          </option>
        </select>

        <!-- Admission Date -->
        <label class="form-label">Admission Date</label>
        <input
          type="date"
          v-model="form.admission_date"
          class="form-control mb-3"
        />
        <!-- Discharge Date -->
         <label class="form-label">Discharge Date</label>
        <input
        type="date"
        v-model="form.discharge_date"
        class="form-control mb-3"
        />
        <!-- Status -->
        <label class="form-label">Status</label>
        <select v-model="form.status" class="form-control mb-3">
          <option value="ADMITTED">ADMITTED</option>
          <option value="DISCHARGED">DISCHARGED</option>
        </select>

        <!-- Buttons -->
        <button
          class="btn btn-success w-100"
          @click="createAdmission"
        >
          Save Admission
        </button>

        <button
          class="btn btn-secondary w-100 mt-2"
          @click="$router.push('/admin/admissions')"
        >
          Cancel
        </button>

      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddAdmission",

  data() {
    return {
      patients: [],
      rooms: [],

      form: {
        patient_id: "",
        room_id: "",
        admission_date: "",
        discharge_date: "",
        status: "ADMITTED"
      }
    };
  },

  async mounted() {
    await this.loadPatients();
    await this.loadRooms();
  },

  methods: {

    // ---------------- LOAD PATIENTS ----------------
    async loadPatients() {
      try {
        const token = localStorage.getItem("access_token");

        const res = await axios.get(
          "http://127.0.0.1:5000/api/patients",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.patients = res.data;

      } catch (err) {
        console.error("PATIENT LOAD ERROR:", err);
      }
    },

    // ---------------- LOAD ROOMS ----------------
    async loadRooms() {
      try {
        const token = localStorage.getItem("access_token");

        const res = await axios.get(
          "http://127.0.0.1:5000/api/rooms",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.rooms = res.data;

      } catch (err) {
        console.error("ROOM LOAD ERROR:", err);
      }
    },

    // ---------------- CREATE ADMISSION ----------------
    async createAdmission() {
      try {

        const token = localStorage.getItem("access_token");

        const payload = {
          patient_id: this.form.patient_id,
          room_id: this.form.room_id,
          admission_date: this.form.admission_date,
          status: this.form.status
        };

        await axios.post(
          "http://127.0.0.1:5000/api/admissions",
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert("Admission created successfully");

        this.$router.push("/admin/admissions");

      } catch (err) {

        console.error(
          "CREATE ADMISSION ERROR:",
          err.response?.data || err.message
        );

        alert("Failed to create admission");
      }
    }
  }
};
</script>

<style scoped>
.glass-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #08111f, #0f2a3b);
  color: white;
}

.glass-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(12px);
  border-radius: 15px;
}

.form-control {
  background: rgba(255,255,255,0.1);
  color: white;
  border: none;
}

.form-control option {
  color: black;
}

.page-title {
  font-weight: bold;
}
</style>