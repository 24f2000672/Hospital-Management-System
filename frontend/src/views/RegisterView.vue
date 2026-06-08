<template>
  <div class="register-page">
    <!-- Header -->
    <header class="landing-topbar">
      <div class="brand-lockup">
        <img src="@/assets/logo.png" class="brand-mark" />

        <div>
          <p class="eyebrow mb-1">HEALTH GUARDIAN+</p>
          <h1 class="brand-title">
            Smart healthcare, emergency response, and accessibility
          </h1>
        </div>
      </div>

      <router-link to="/" class="btn btn-outline-light btn-lg">
        Main Dashboard
      </router-link>
    </header>

    <!-- Register Container -->
    <div class="register-container">
      <!-- Left Side -->
      <div class="hero-section">
        <span class="hero-pill">
          Patient Registration Portal
        </span>

        <h2>
          Create your
          Health Guardian+
          account
        </h2>

        <p>
          Register once to access appointments, medical records,
          medicine reminders, emergency SOS alerts, accessibility
          settings, health reports and much more.
        </p>

        <div class="metric-grid">
          <div class="metric-card">
            <strong>24/7</strong>
            <span>SOS Support</span>
          </div>

          <div class="metric-card">
            <strong>Secure</strong>
            <span>Health Records</span>
          </div>

          <div class="metric-card">
            <strong>Smart</strong>
            <span>Appointments</span>
          </div>
        </div>
      </div>

      <!-- Right Side Form -->
      <div class="glass-form">
        <h3 class="mb-4">Patient Signup Form</h3>

        <form @submit.prevent="registerPatient">

          <input
            v-model="form.first_name"
            type="text"
            class="glass-input"
            placeholder="First Name"
            required
          />

          <input
            v-model="form.last_name"
            type="text"
            class="glass-input"
            placeholder="Last Name"
            required
          />

          <input
            v-model="form.email"
            type="email"
            class="glass-input"
            placeholder="Email"
            required
          />

          <input
            v-model="form.password"
            type="password"
            class="glass-input"
            placeholder="Password"
            required
          />

          <input
            v-model="form.age"
            type="number"
            class="glass-input"
            placeholder="Age"
            required
          />

          <select
            v-model="form.gender"
            class="glass-input"
            required
          >
            <option value="">Gender</option>
            <option value="M">Male</option>
            <option value="F">Female</option>
          </select>

          <input
            v-model="form.address"
            type="text"
            class="glass-input"
            placeholder="Address"
            required
          />

          <input
            v-model="form.phone"
            type="text"
            class="glass-input"
            placeholder="Phone Number"
            required
          />

          <input
            v-model="form.dob"
            type="date"
            class="glass-input"
            required
          />

          <select
            v-model="form.insurance"
            class="glass-input"
            required
          >
            <option value="">Insurance</option>
            <option value="Y">Yes</option>
            <option value="N">No</option>
          </select>

          <button
            type="submit"
            class="btn btn-primary btn-lg w-100 mt-3"
          >
            Create Account
          </button>

          <div
            v-if="errorMessage"
            class="alert alert-danger mt-3"
          >
            {{ errorMessage }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterView",

  data() {
    return {
      form: {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        age: "",
        gender: "",
        address: "",
        phone: "",
        dob: "",
        insurance: ""
      },
      errorMessage: ""
    };
  },

  methods: {
    async registerPatient() {
      try {
        await axios.post(
          "http://127.0.0.1:5000/signup",
          this.form
        );

        alert("Registration Successful!");
        this.$router.push("/login");

      } catch (error) {
        this.errorMessage =
          error.response?.data?.message ||
          "Registration Failed";
      }
    }
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  color: white;

  background:
    radial-gradient(circle at top left,
      rgba(45,212,191,.24),
      transparent 28%),
    radial-gradient(circle at top right,
      rgba(249,115,22,.25),
      transparent 28%),
    linear-gradient(
      160deg,
      #08111f 0%,
      #0f2a3b 48%,
      #123b52 100%
    );
}

.landing-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 50px;
}

.brand-lockup {
  display: flex;
  gap: 15px;
  align-items: center;
}

.brand-mark {
  width: 70px;
  height: 70px;
  border-radius: 20px;
}

.brand-title {
  font-size: 1.3rem;
}

.eyebrow {
  letter-spacing: .2rem;
  font-size: .75rem;
  color: rgba(255,255,255,.7);
}

.register-container {
  display: grid;
  grid-template-columns: 1fr 500px;
  gap: 40px;
  padding: 40px 60px;
}

.hero-section h2 {
  font-size: 4rem;
  line-height: 1;
  margin-top: 20px;
  font-family: Georgia, serif;
}

.hero-section p {
  margin-top: 25px;
  color: rgba(255,255,255,.8);
  font-size: 1.1rem;
}

.hero-pill {
  display: inline-block;
  padding: 10px 18px;
  border-radius: 999px;
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.15);
}

.metric-grid {
  display: flex;
  gap: 15px;
  margin-top: 40px;
}

.metric-card {
  flex: 1;
  padding: 20px;
  border-radius: 24px;
  backdrop-filter: blur(18px);
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.1);
}

.metric-card strong {
  display: block;
  font-size: 1.3rem;
}

.metric-card span {
  color: rgba(255,255,255,.7);
}

.glass-form {
  padding: 30px;
  border-radius: 30px;
  backdrop-filter: blur(20px);
  background: rgba(4,12,20,.45);
  border: 1px solid rgba(255,255,255,.12);
}

.glass-input {
  width: 100%;
  margin-bottom: 15px;
  padding: 14px;
  border-radius: 15px;
  border: 1px solid rgba(255,255,255,.15);
  background: rgba(255,255,255,.08);
  color: white;
}

.glass-input::placeholder {
  color: rgba(255,255,255,.6);
}

.glass-input:focus {
  outline: none;
  border-color: #2dd4bf;
}

@media(max-width:992px){

  .register-container{
    grid-template-columns:1fr;
  }

  .hero-section h2{
    font-size:2.7rem;
  }

  .landing-topbar{
    flex-direction:column;
    gap:20px;
  }
}
</style>