<template>
  <div class="page">

    <!-- HEADER (Dashboard style) -->
    <div class="header d-flex justify-content-between align-items-center">
      <h2>🩺 Vardha Hospital - Update Doctor</h2>

      <div class="d-flex gap-2">
        <button class="btn btn-success">+ Add Doctor</button>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </div>

    <!-- STATS CARDS -->
    <div class="stats-container">
      <div class="stat-card">
        <h3>1</h3>
        <p>Total Doctors</p>
      </div>

      <div class="stat-card">
        <h3>1</h3>
        <p>Active Doctors</p>
      </div>

      <div class="stat-card">
        <h3>1</h3>
        <p>Departments</p>
      </div>
    </div>

    <!-- FORM CARD -->
    <div class="form-card">

      <div v-if="message" :class="'alert alert-' + alertType">
        {{ message }}
      </div>

      <form v-if="form" @submit.prevent="updateDoctor">

        <div class="grid">
          <input v-model="form.deptname" placeholder="Department Name" required />
          <input v-model="form.deptdes" placeholder="Description" required />
          <input v-model="form.fn" placeholder="First Name" required />
          <input v-model="form.ln" placeholder="Last Name" required />
          <input v-model.number="form.age" type="number" placeholder="Age" required />
          <input v-model="form.contact" placeholder="Contact" required />
          <input v-model.number="form.exp" type="number" placeholder="Experience (Years)" required />
        </div>

        <div class="actions">
          <button class="btn btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? 'Updating...' : 'Update Doctor' }}
          </button>

          <button type="button" class="btn btn-secondary" @click="goBack">
            Cancel
          </button>
        </div>

      </form>

      <div v-else class="loading">
        Loading doctor information...
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UpdateDoctor",

  data() {
    return {
      message: "",
      alertType: "success",
      isSubmitting: false,
      doctorId: null,
      form: null,
    };
  },

  async mounted() {
    this.doctorId = this.$route.query.id;

    if (!this.doctorId) {
      this.message = "Doctor ID not found";
      this.alertType = "danger";
      return;
    }

    const token = localStorage.getItem("access_token");

    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/get_doctor/${this.doctorId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const d = res.data;

      this.form = {
        deptname: d.deptname || "",
        deptdes: d.deptdes || "",
        fn: d.first_name || "",
        ln: d.last_name || "",
        age: d.age || null,
        contact: d.contact || "",
        exp: d.experience || null,
      };
    } catch (err) {
      this.message = "Failed to load doctor details";
      this.alertType = "danger";
    }
  },

  methods: {
    async updateDoctor() {
      const token = localStorage.getItem("access_token");

      this.isSubmitting = true;

      try {
        await axios.put(
          `http://127.0.0.1:5000/update_doctor/${this.doctorId}`,
          this.form,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.message = "Doctor updated successfully!";
        this.alertType = "success";

        setTimeout(() => {
          this.$router.push("/admin/dashboard");
        }, 1500);
      } catch (err) {
        this.message = "Update failed!";
        this.alertType = "danger";
      } finally {
        this.isSubmitting = false;
      }
    },

    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },

    goBack() {
      this.$router.push("/admin/dashboard");
    },
  },
};
</script>

<style scoped>
.page {
  background: #071a2f;
  min-height: 100vh;
  padding: 20px;
  color: white;
}

/* HEADER */
.header {
  background: #0b2a4a;
  padding: 15px 20px;
  border-radius: 10px;
}

/* STATS */
.stats-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 20px;
}

.stat-card {
  background: #0d355e;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

/* FORM */
.form-card {
  margin-top: 25px;
  background: #0b2a4a;
  padding: 25px;
  border-radius: 12px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

input {
  padding: 10px;
  border-radius: 8px;
  border: none;
  outline: none;
}

/* BUTTONS */
.actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.loading {
  color: #ccc;
}
</style>