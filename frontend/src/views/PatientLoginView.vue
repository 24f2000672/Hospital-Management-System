<template>
  <div class="login-page">
    
    <header class="navbar bg-white d-flex align-items-center justify-content-between px-4">
      <div>
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>

      <div class="text-center">
        <h1>Vardha Hospital</h1>
      </div>

      <nav class="d-flex gap-3 flex-wrap">
        <button class="btn" :class="selectedRole === 'patient' ? 'btn-success' : 'btn-outline-success'" @click="selectedRole = 'patient'">
          Patient Login
        </button>
        <button class="btn" :class="selectedRole === 'doctor' ? 'btn-secondary' : 'btn-outline-secondary'" @click="selectedRole = 'doctor'">
          Doctor Login
        </button>
        <button class="btn" :class="selectedRole === 'admin' ? 'btn-primary' : 'btn-outline-primary'" @click="selectedRole = 'admin'">
          Admin Login
        </button>
      </nav>
    </header>

    
    <div class="scroll-container">
      <div class="scroll-text">Your health journey begins here — log in to care for yourself</div>
    </div>

    
    <div class="container mt-5">
      <div class="card shadow p-4 mx-auto login-card">
        <h2 class="text-center mb-2">{{ roleTitle }} Login</h2>
        <p class="text-center text-muted mb-4">Choose a role, then sign in to the correct dashboard.</p>

        <form @submit.prevent="loginUser">
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

          <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>

        
        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>

        
        <div class="mt-3 text-center">
          <span>Don't have an account?</span>
          <router-link to="/register" class="ms-2">Sign Up</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginView',

  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errorMessage: '',
      selectedRole: 'patient',
    }
  },

  computed: {
    roleTitle() {
      return this.selectedRole.charAt(0).toUpperCase() + this.selectedRole.slice(1)
    },
  },

  methods: {
    async loginUser() {
      this.errorMessage = ''

      try {
        const res = await axios.post('http://127.0.0.1:5000/login', this.form)

        console.log('LOGIN RESPONSE:', res.data)

        // Save JWT token
        localStorage.setItem('access_token', res.data.access_token)
        localStorage.setItem('user_role', String(res.data.role || ''))

        alert(res.data.message)

        // Role-based redirects
        if (res.data.role === 1) {
          this.$router.push({ path: '/admin/dashboard' })
        } else if (res.data.role === 2) {
          this.$router.push({ path: '/doctor/dashboard' })
        } else if (res.data.role === 3) {
          this.$router.push({ path: '/patient/dashboard' })
        } else {
          // fallback to login
          this.$router.push({ path: '/login' })
        }
      } catch (error) {
        if (error.response) {
          const status = error.response.status
          if (status === 401) {
            alert('Incorrect password. Please try again.')
          } else if (status === 404) {
            alert('User not found. Please Sign Up.')
            this.$router.push({ path: '/register' })
          } else {
            this.errorMessage = error.response.data.message || 'Login failed'
          }
        } else {
          this.errorMessage = 'Server not reachable'
        }
      }
    },
  },
}
</script>

<style>
.login-page {
  min-height: 100vh;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}

/* SCROLL BANNER */
.scroll-container {
  background: black;
  color: white;
  overflow: hidden;
  white-space: nowrap;
}
.scroll-text {
  display: inline-block;
  padding-left: 100%;
  animation: scroll 12s linear infinite;
}
@keyframes scroll {
  from {
    transform: translateX(0%);
  }
  to {
    transform: translateX(-100%);
  }
}

/* LOGIN CARD */
.login-card {
  max-width: 450px;
  border-radius: 12px;
}
</style>
