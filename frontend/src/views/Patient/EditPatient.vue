<template>
  <div
    style="background: linear-gradient(to right,#ccccff,#66ccff,#ff8566,#ccccff,#ff8566); min-height:100vh;"
  >
    <!-- Navbar -->
    <nav class="navbar d-flex justify-content-between align-items-center px-4" style="background-color: white;">
      <div class="logo-section">
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>

      <div class="brand-center text-center">
        <h1>Vardha Hospital</h1>
      </div>

      <div class="nav-links d-flex gap-3">
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </div>
    </nav>

    <marquee style="background-color:black;color:white;">
      Editing patient details — make sure information is correct.
    </marquee>

    <!-- Flash message -->
    <div class="container mt-3" v-if="flashMessage">
      <div class="alert alert-info alert-dismissible fade show">
        {{ flashMessage }}
        <button type="button" class="btn-close" @click="flashMessage = null"></button>
      </div>
    </div>

    <div class="container mt-4">
      <h2>Edit Patient</h2>
      <form @submit.prevent="updatePatient">
        <div class="mb-3">
          <label class="form-label">First Name</label>
          <input type="text" v-model="patient.First_Name" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Last Name</label>
          <input type="text" v-model="patient.Last_Name" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Age</label>
          <input type="number" v-model="patient.Age" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Gender</label>
          <input type="text" v-model="patient.Gender" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Address</label>
          <input type="text" v-model="patient.Address" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Phone</label>
          <input type="text" v-model="patient.Phone_no" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">DOB</label>
          <input type="date" v-model="patient.DOB" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Has Insurance</label>
          <input type="text" v-model="patient.Has_Insurance" class="form-control" required />
        </div>

        <button type="submit" class="btn btn-primary">Update Patient</button>
        <button type="button" class="btn btn-secondary ms-2" @click="goBack">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditPatient",
  data() {
    return {
      patient: {
        First_Name: "",
        Last_Name: "",
        Age: "",
        Gender: "",
        Address: "",
        Phone_no: "",
        DOB: "",
        Has_Insurance: "",
        patient_id: null
      },
      flashMessage: null,
    };
  },
  mounted() {
    this.fetchPatient();
  },
  methods: {
    getToken() {
      const token = localStorage.getItem("access_token");
      if (!token) {
        alert("Session expired. Please login again.");
        this.$router.push("/login");
        return null;
      }
      return token;
    },
    async fetchPatient() {
      try {
        const token = this.getToken();
        if (!token) return;

        const patientId = this.$route.params.id; 
        const res = await axios.get(
          `http://127.0.0.1:5000/editpatient/${patientId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.patient = res.data.patient;
      } catch (err) {
        console.error("Fetch patient error:", err.response?.data || err);
        this.flashMessage = err.response?.data?.message || "Failed to fetch patient";
      }
    },
    async updatePatient() {
      try {
        const token = this.getToken();
        if (!token) return;

        const patientId = this.$route.params.id;
        const res = await axios.put(
          `http://127.0.0.1:5000/editpatient/${patientId}`,
          this.patient,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.flashMessage = res.data.message || "Patient updated successfully!";
      } catch (err) {
        console.error("Update patient error:", err.response?.data || err);
        this.flashMessage = err.response?.data?.message || "Failed to update patient";
      }
    },
    goBack() {
      this.$router.push("/admin/dashboard");
    },
    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
body, html {
  height: 100%;
  margin: 0;
  font-family: Arial;
}
.navbar img {
  border-radius: 10px;
}
.btn {
  margin-top: 5px;
}
</style>