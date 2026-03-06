<template>
  <div
    style="background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566); min-height: 100vh;"
  >
    <!-- Navbar -->
    <nav style="background-color: white;" class="navbar d-flex align-items-center">
      <div class="logo-section">
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>
      <div class="brand-center text-center flex-grow-1">
        <h1>Vardha Hospital</h1>
      </div>
      <div class="nav-links d-flex gap-3">
        <button class="btn btn-outline-primary" @click="goToProfile">Edit Profile</button>
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </div>
    </nav>

    <marquee style="background-color: black; color: white;">
      Good health starts with awareness — welcome to your dashboard.
    </marquee>

    <center>
      <h1 style="color:rgb(15, 15, 15)">🤩 Welcome to Your Patient Dashboard! 🤩</h1>
    </center>

    <!-- Flash message -->
    <div class="container mt-3" v-if="flashMessage">
      <div class="alert alert-info alert-dismissible fade show">
        {{ flashMessage }}
        <button type="button" class="btn-close" @click="flashMessage = null"></button>
      </div>
    </div>

    <!-- Departments -->
    <div class="container mt-4">
      <h3>Departments available are:</h3>
      <ul class="list-group mt-3">
        <li
          v-for="dep in departmentsWithDoctors"
          :key="dep.Dept_id"
          class="list-group-item"
          style="color: rgb(38, 1, 250);"
        >
          <strong>Specialisation Id:</strong> {{ dep.Dept_id }}<br />
          <strong>Department Name:</strong> {{ dep.Dept_name }}<br />
          <strong>Department Description:</strong> {{ dep.description }}<br />
          <strong>Doctors:</strong>
          <span v-if="dep.doctors && dep.doctors.length">
            <span v-for="(doc, index) in dep.doctors" :key="doc.Doc_id" class="d-inline-block me-2 mt-1">
                Dr.  {{ doc.Name }}
              
            </span>
          </span>
          <span v-else>None</span>
        </li>
      </ul>
    </div>

    <!-- Appointments -->
    <div class="container mt-5">
      <h3>My Appointments</h3>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Date</th>
            <th>Time</th>
            <th>Doctor</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in myAppointments" :key="app.App_id">
            <td>{{ formatDate(app.Date) }}</td>
            <td>{{ formatTime(app.Time) }}</td>
            <td>{{ app.Doctor_Name }}</td>
            <td>
              <span v-if="app.Status === 'Booked'" class="badge bg-success">Booked</span>
              <span v-else-if="app.Status === 'Cancelled'" class="badge bg-danger">Cancelled by Doctor</span>
              <span v-else class="badge bg-secondary">{{ app.Status }}</span>
            </td>
            <td>
              <button
                v-if="app.Status === 'Booked'"
                class="btn btn-danger btn-sm"
                @click="cancelAppointment(app.App_id)"
              >
                Cancel
              </button>
            </td>
          </tr>
          <tr v-if="!myAppointments.length">
            <td colspan="5" class="text-center text-danger">No appointments found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Treatment History -->
    <div class="container mt-5">
      <h3>Your Treatment History</h3>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Date</th>
            <th>Doctor</th>
            <th>Diagnosis</th>
            <th>Prescription</th>
            <th>Notes</th>
            <th>Progress</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(t, index) in treatmentHistory" :key="index">
            <td>{{ formatDate(t.Date) }}</td>
            <td>{{ t.Doctor }}</td>
            <td>{{ t.Diagnosis }}</td>
            <td>{{ t.Prescription }}</td>
            <td>{{ t.Notes }}</td>
            <td>{{ t.Progress }}</td>
          </tr>
          <tr v-if="!treatmentHistory.length">
            <td colspan="6" class="text-center text-danger">No treatment history found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Doctors list for slots -->
    <div class="container mt-5">
      <h3>Available Appointment Slots (Today and Next 7 Days)</h3>
      <h5>Select a doctor to view their available appointment slots:</h5>
      <div v-for="doctor in doctors" :key="doctor.Doc_id" class="mb-2">
        <button class="btn btn-primary" @click="goToDoctorProfile(doctor.Doc_id)">
          Dr. {{ doctor.Name }}
        </button>
      </div>
      <p v-if="!doctors.length">No doctors found.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PatientDashboard",
  data() {
    return {
      patient: null,
      departments: [],
      doctors: [],
      myAppointments: [],
      treatmentHistory: [],
      flashMessage: null,
      departmentsWithDoctors: [],
    };
  },
  mounted() {
    this.fetchDashboard();
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
    async fetchDashboard() {
      try {
        const token = this.getToken();
        if (!token) return;

        const res = await axios.get("http://127.0.0.1:5000/patient/dashboard", {
          headers: { Authorization: `Bearer ${token}` },
        });

        this.patient = res.data.patient;
        this.departments = res.data.departments || [];
        this.doctors = res.data.doctors || [];
        this.myAppointments = res.data.upcoming_appointments || [];
        this.treatmentHistory = res.data.treatment_history || [];

        // Map doctors to their departments
        this.departmentsWithDoctors = this.departments.map((dep) => ({
          ...dep,
          doctors: this.doctors.filter((doc) => doc.Department === dep.Dept_id),
        }));
      } catch (err) {
        console.error("Dashboard fetch error:", err.response?.data || err);
        if (err.response?.status === 401) this.$router.push("/login");
      }
    },
    formatDate(date) {
      return new Date(date).toDateString();
    },
    formatTime(time) {
      const t = new Date(`1970-01-01T${time}`);
      return t.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    },
    goToProfile() {
      if (!this.patient || !this.patient.patient_id) return;
      this.$router.push(`/editpatient/${this.patient.patient_id}`);
    },
    goToDoctorProfile(docId) {
      this.$router.push(`/doctor/${docId}`);
    },
    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/login");
    },
    async cancelAppointment(appId) {
      if (!confirm("Cancel this appointment?")) return;

      try {
        const token = this.getToken();
        if (!token) return;

        const res = await axios.post(
          "http://127.0.0.1:5000/patient/cancel_slot",
          { booking_id: appId },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.flashMessage = res.data.message;
        await this.fetchDashboard();
      } catch (err) {
        console.error("Cancel appointment error:", err.response?.data || err);
      }
    },
  },
};
</script>

<style scoped>
.navbar img {
  border-radius: 10px;
}
.nav-links button {
  margin-left: 10px;
}
table th,
table td {
  vertical-align: middle;
}
</style>