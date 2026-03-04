<template>
  <div class="container mt-4">
    <!-- HEADER -->
    <div class="d-flex justify-content-between align-items-center bg-white p-3 rounded shadow">
      <div>
        <img src="@/assets/logo.png" height="60" />
      </div>

      <h2 class="text-center m-0">Vardha Hospital - Add Doctor</h2>

      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>

    <marquee style="background-color: black; color: white">
      Adding a healer to the team — every doctor strengthens our mission of care.
    </marquee>

    <!-- FORM -->
    <div class="card mt-4 shadow p-4">
      <div v-if="message" :class="'alert alert-' + alertType">
        {{ message }}
      </div>

      <form @submit.prevent="addDoctor">
        <div class="row">
          <div class="col-md-6 mb-3">
            <label>Department Name</label>
            <input v-model="form.deptname" type="text" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Description</label>
            <input v-model="form.deptdes" type="text" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>First Name</label>
            <input v-model="form.fn" type="text" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Last Name</label>
            <input v-model="form.ln" type="text" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Age</label>
            <input v-model.number="form.age" type="number" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Contact</label>
            <input v-model="form.contact" type="text" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Experience (Years)</label>
            <input v-model.number="form.exp" type="number" class="form-control" required />
          </div>
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
          {{ isSubmitting ? 'Adding...' : 'Add Doctor' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddDoctor',

  data() {
    return {
      message: '',
      alertType: 'success',
      isSubmitting: false,
      form: {
        deptname: '',
        deptdes: '',
        fn: '',
        ln: '',
        email: '',
        password: '',
        age: null,
        contact: '',
        exp: null,
      },
    }
  },

  methods: {
    async addDoctor() {
      if (this.isSubmitting) return

      const token = localStorage.getItem('access_token') || localStorage.getItem('token')

      if (!token) {
        this.message = 'Session expired. Please login again.'
        this.alertType = 'danger'
        this.$router.push('/')
        return
      }

      this.isSubmitting = true
      this.message = ''

      try {
        const response = await axios.post('http://127.0.0.1:5000/add_doctor', this.form, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        })

        this.message = response.data?.message || 'Doctor added'
        this.alertType = 'success'

        this.form = {
          deptname: '',
          deptdes: '',
          fn: '',
          ln: '',
          email: '',
          password: '',
          age: null,
          contact: '',
          exp: null,
        }

        this.$router.push({ name: 'admin-dashboard' })
      } catch (error) {
        console.log('ERROR RESPONSE:', error.response)

        if (error.response?.status === 401) {
          this.message = 'Invalid or expired token. Login again.'
          this.alertType = 'danger'
          this.logout()
        } else if (error.response?.status === 403) {
          this.message = 'Only admin can add doctor.'
          this.alertType = 'danger'
        } else {
          const serverMsg = error.response?.data?.message
          this.message =
            typeof serverMsg === 'string' && serverMsg.trim() ? serverMsg : 'Failed to add doctor'
          this.alertType = 'danger'
        }
      } finally {
        this.isSubmitting = false
      }
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/')
    },
  },
}
</script>

<style>
body {
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}
</style>
