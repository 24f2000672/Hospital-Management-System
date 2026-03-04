<template>
  <div class="container mt-4">
    <!-- HEADER -->
    <div class="d-flex justify-content-between align-items-center bg-white p-3 rounded shadow">
      <div>
        <img src="@/assets/logo.png" height="60" />
      </div>

      <h2 class="text-center m-0">Vardha Hospital - Update Doctor</h2>

      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>

    <marquee style="background-color: black; color: white">
      Updating doctor information — keeping our team records current and accurate.
    </marquee>

    <!-- FORM -->
    <div class="card mt-4 shadow p-4">
      <div v-if="message" :class="'alert alert-' + alertType">
        {{ message }}
      </div>

      <form @submit.prevent="updateDoctor" v-if="form">
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

        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-primary flex-grow-1" :disabled="isSubmitting">
            {{ isSubmitting ? 'Updating...' : 'Update Doctor' }}
          </button>
          <button type="button" class="btn btn-secondary" @click="goBack">Cancel</button>
        </div>
      </form>

      <div v-else class="alert alert-info">Loading doctor information...</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UpdateDoctor',

  data() {
    return {
      message: '',
      alertType: 'success',
      isSubmitting: false,
      doctorId: null,
      form: null,
    }
  },

  async mounted() {
    // Get doctor ID from route query params
    this.doctorId = this.$route.query.id

    if (!this.doctorId) {
      this.message = 'Doctor ID not found'
      this.alertType = 'danger'
      return
    }

    const token = localStorage.getItem('access_token')

    try {
      // Fetch full doctor details from backend
      const response = await axios.get(`http://127.0.0.1:5000/get_doctor/${this.doctorId}`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      const doctor = response.data

      // Initialize form with existing doctor data
      this.form = {
        deptname: doctor.deptname || '',
        deptdes: doctor.deptdes || '',
        fn: doctor.first_name || '',
        ln: doctor.last_name || '',
        age: doctor.age || null,
        contact: doctor.contact || '',
        exp: doctor.experience || null,
      }
    } catch (error) {
      console.error('Error fetching doctor details:', error)
      this.message = error.response?.data?.message || 'Failed to load doctor details'
      this.alertType = 'danger'
      this.form = {
        deptname: '',
        deptdes: '',
        fn: '',
        ln: '',
        age: null,
        contact: '',
        exp: null,
      }
    }
  },

  methods: {
    async updateDoctor() {
      const token = localStorage.getItem('access_token')

      if (!this.form.deptname || !this.form.fn || !this.form.ln) {
        this.message = 'Please fill all required fields'
        this.alertType = 'warning'
        return
      }

      this.isSubmitting = true

      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/update_doctor/${this.doctorId}`,
          {
            deptname: this.form.deptname,
            deptdes: this.form.deptdes,
            fn: this.form.fn,
            ln: this.form.ln,
            age: this.form.age,
            contact: this.form.contact,
            exp: this.form.exp,
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        )

        this.message = response.data.message || 'Doctor updated successfully'
        this.alertType = 'success'

        // Redirect back to dashboard after 2 seconds
        setTimeout(() => {
          this.$router.push('/admin/dashboard')
        }, 2000)
      } catch (error) {
        console.error('Error updating doctor:', error)
        this.message = error.response?.data?.message || 'Failed to update doctor'
        this.alertType = 'danger'
      } finally {
        this.isSubmitting = false
      }
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('token')
      this.$router.push('/login')
    },

    goBack() {
      this.$router.push('/admin/dashboard')
    },
  },
}
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  padding-top: 20px;
  padding-bottom: 20px;
}

.card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background-color: white;
}

marquee {
  margin-top: 10px;
  padding: 10px;
  font-size: 14px;
  font-weight: 500;
}

.alert {
  margin-bottom: 20px;
  border-radius: 4px;
}

.btn {
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

label {
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

input.form-control {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  font-size: 14px;
}

input.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  outline: none;
}

.d-flex.gap-2 {
  gap: 10px;
}
</style>
