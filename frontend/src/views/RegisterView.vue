<template>
  <div class="register-page">
    
    <header class="navbar bg-white d-flex align-items-center justify-content-between px-4">
      <div>
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>

      <div class="text-center">
        <h1>Vardha Hospital</h1>
      </div>

      <div>
        <router-link to="/" class="btn btn-outline-success"> Main Dashboard </router-link>
      </div>
    </header>

    <!-- Signup Form -->
    <div class="container mt-4">
      <h2 class="mb-4">Patient Signup Form</h2>
      <p class="text-muted mb-4">
        Register once to manage appointments, records, reminders, SOS alerts, and accessibility tools.
      </p>

      <form @submit.prevent="registerPatient">
        <input
          v-model="form.first_name"
          type="text"
          class="form-control mb-3"
          placeholder="Enter Your First Name"
          required
        />

        <input
          v-model="form.last_name"
          type="text"
          class="form-control mb-3"
          placeholder="Enter Your Last Name"
          required
        />

        <input
          v-model="form.email"
          type="email"
          class="form-control mb-3"
          placeholder="Enter Your Email"
          required
        />

        <input
          v-model="form.password"
          type="password"
          class="form-control mb-3"
          placeholder="Enter Your Password"
          required
        />

        <input
          v-model="form.age"
          type="number"
          class="form-control mb-3"
          placeholder="Enter Your Age"
          required
        />

        <select v-model="form.gender" class="form-control mb-3" required>
          <option disabled value="">Select Gender</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
        </select>

        <input
          v-model="form.address"
          type="text"
          class="form-control mb-3"
          placeholder="Enter Your Address"
          required
        />

        <input
          v-model="form.phone"
          type="text"
          class="form-control mb-3"
          placeholder="Enter Your Phone"
          required
        />

        <input v-model="form.dob" type="date" class="form-control mb-3" required />

        <select v-model="form.insurance" class="form-control mb-3" required>
          <option disabled value="">Insurance?</option>
          <option value="Y">Yes</option>
          <option value="N">No</option>
        </select>

        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>

      
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterView',
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        age: '',
        gender: '',
        address: '',
        phone: '',
        dob: '',
        insurance: '',
      },
      errorMessage: '',
    }
  },
  methods: {
    async registerPatient() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/signup', this.form)

        alert('Registration Successful!')
        this.$router.push('/login')
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Registration failed!'
      }
    },
  },
}
</script>

<style>
.register-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>
