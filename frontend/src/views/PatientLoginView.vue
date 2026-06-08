<template>
  <div class="login-page">
    <!-- Header -->
    <header class="landing-topbar container-fluid px-4 px-lg-5 py-3">
      <div class="brand-lockup">
        <img src="@/assets/logo.png" alt="Logo" class="brand-mark" />
        <div>
          <p class="eyebrow mb-1">HEALTH GUARDIAN+</p>
          <h1 class="brand-title mb-0">
            Smart healthcare, emergency response, and accessibility
          </h1>
        </div>
      </div>

      <router-link to="/" class="btn btn-outline-light btn-lg">
        Home
      </router-link>
    </header>

    <!-- Banner -->
    <div class="banner">
      <span>
        Your health journey begins here — Login to access appointments,
        medical records, SOS alerts and healthcare services.
      </span>
    </div>

    <!-- Login Section -->
    <main class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-5">

          <div class="glass-card">

            <span class="hero-pill mb-3">
              Secure Authentication
            </span>

            <h2 class="login-title">
              {{ roleTitle }} Login
            </h2>

            <p class="login-subtitle">
              Choose your role and sign in to continue.
            </p>

            <!-- Role Selection -->
            <div class="role-buttons">
              <button
                class="btn"
                :class="selectedRole === 'patient'
                  ? 'btn-primary'
                  : 'btn-outline-light'"
                @click="selectedRole='patient'"
              >
                Patient
              </button>

              <button
                class="btn"
                :class="selectedRole === 'doctor'
                  ? 'btn-primary'
                  : 'btn-outline-light'"
                @click="selectedRole='doctor'"
              >
                Doctor
              </button>

              <button
                class="btn"
                :class="selectedRole === 'admin'
                  ? 'btn-primary'
                  : 'btn-outline-light'"
                @click="selectedRole='admin'"
              >
                Admin
              </button>
            </div>

            <form @submit.prevent="loginUser">

              <input
                v-model="form.email"
                type="email"
                class="form-control glass-input"
                placeholder="Enter Email"
                required
              />

              <input
                v-model="form.password"
                type="password"
                class="form-control glass-input mt-3"
                placeholder="Enter Password"
                required
              />

              <button
                type="submit"
                class="btn btn-primary btn-lg w-100 mt-4"
              >
                Login
              </button>

            </form>

            <div
              v-if="errorMessage"
              class="alert alert-danger mt-3"
            >
              {{ errorMessage }}
            </div>

            <div class="text-center mt-4">
              <span class="text-light">
                Don't have an account?
              </span>

              <router-link
                to="/register"
                class="text-info ms-2"
              >
                Register Here
              </router-link>
            </div>

          </div>

        </div>
      </div>
    </main>
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
      return (
        this.selectedRole.charAt(0).toUpperCase() +
        this.selectedRole.slice(1)
      )
    },
  },

  methods: {
    async loginUser() {
      this.errorMessage = ''

      try {
        const res = await axios.post(
          'http://127.0.0.1:5000/login',
          this.form,
        )

        localStorage.setItem(
          'access_token',
          res.data.access_token,
        )

        localStorage.setItem(
          'user_role',
          String(res.data.role || ''),
        )

        if (res.data.role === 1) {
          this.$router.push('/admin/dashboard')
        } else if (res.data.role === 2) {
          this.$router.push('/doctor/dashboard')
        } else if (res.data.role === 3) {
          this.$router.push('/patient/dashboard')
        }
      } catch (error) {
        this.errorMessage =
          error.response?.data?.message ||
          'Login Failed'
      }
    },
  },
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  color: #f4fbff;

  background:
    radial-gradient(
      circle at top left,
      rgba(45,212,191,0.24),
      transparent 28%
    ),
    radial-gradient(
      circle at top right,
      rgba(249,115,22,0.25),
      transparent 28%
    ),
    linear-gradient(
      160deg,
      #08111f 0%,
      #0f2a3b 48%,
      #123b52 100%
    );
}

.banner {
  background: rgba(0,0,0,0.35);
  color: white;
  text-align: center;
  padding: 12px;
  border-top: 1px solid rgba(255,255,255,0.1);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.landing-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-mark {
  width: 72px;
  height: 72px;
  border-radius: 18px;
}

.brand-title {
  font-family: Georgia, serif;
  font-size: 1.2rem;
}

.eyebrow {
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  color: rgba(255,255,255,0.7);
}

.glass-card {
  backdrop-filter: blur(18px);
  background: rgba(4,12,20,0.45);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 28px;
  padding: 2rem;
  box-shadow: 0 24px 70px rgba(0,0,0,0.25);
}

.hero-pill {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 999px;

  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.1);
}

.login-title {
  font-family: Georgia, serif;
  font-size: 2.5rem;
}

.login-subtitle {
  color: rgba(255,255,255,0.7);
}

.role-buttons {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.glass-input {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  color: white;
}

.glass-input::placeholder {
  color: rgba(255,255,255,0.6);
}

.glass-input:focus {
  background: rgba(255,255,255,0.12);
  color: white;
  box-shadow: none;
}

@media (max-width: 768px) {
  .login-title {
    font-size: 2rem;
  }

  .landing-topbar {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>