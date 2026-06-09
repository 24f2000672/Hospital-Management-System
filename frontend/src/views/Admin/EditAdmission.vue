<template>
  <div class="glass-page">
    <div class="container py-4">

      <h2 class="page-title mb-4">✏ Edit Admission</h2>

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
            {{ p.name }}
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
          @click="updateAdmission"
        >
          Update Admission
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
  name: "EditAdmission",

  props: ["id"],

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
    await this.loadAdmission();
  },

  methods: {

    // ---------------- LOAD SINGLE ADMISSION ----------------
    async loadAdmission() {

      try {

        const token = localStorage.getItem("access_token");

        const res = await axios.get(
          `http://127.0.0.1:5000/api/admissions/${this.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        const data = res.data;

        this.form = {
          patient_id: data.patient_id,
          room_id: data.room_id,
          admission_date: data.admission_date
            ? data.admission_date.split("T")[0]
            : "",

          discharge_date: data.discharge_date
            ? data.discharge_date.split("T")[0]
            : "",

          status: data.status
        };

      } catch (err) {

        console.error(
          "LOAD ADMISSION ERROR:",
          err.response?.data || err.message
        );

        alert("Failed to load admission");
      }
    },

    // ---------------- LOAD PATIENTS ----------------
    async loadPatients() {

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
    },

    // ---------------- LOAD ROOMS ----------------
    async loadRooms() {

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
    },

    // ---------------- UPDATE ADMISSION ----------------
    async updateAdmission() {

      try {

        const token = localStorage.getItem("access_token");

        const payload = {
          patient_id: this.form.patient_id,
          room_id: this.form.room_id,
          admission_date: this.form.admission_date,
          discharge_date: this.form.discharge_date,
          status: this.form.status
        };

        await axios.put(
          `http://127.0.0.1:5000/api/admissions/${this.id}`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert("Admission updated successfully");

        this.$router.push("/admin/admissions");

      } catch (err) {

        console.error(
          "UPDATE ADMISSION ERROR:",
          err.response?.data || err.message
        );

        alert("Failed to update admission");
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