<template>
  <div class="container mt-4">
    <!-- HEADER -->
    <div class="d-flex justify-content-between align-items-center bg-white p-3 rounded shadow">
      <div>
        <img src="@/assets/logo.png" height="60" />
      </div>

      <h2 class="text-center m-0">Vardha Hospital - Update Patient</h2>

      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>

    <marquee style="background-color: black; color: white">
      Updating patient information — maintaining accurate health records for better care.
    </marquee>

    <!-- FORM -->
    <div class="card mt-4 shadow p-4">
      <div v-if="message" :class="'alert alert-' + alertType">
        {{ message }}
      </div>

      <form @submit.prevent="updatePatient" v-if="form">
        <div class="row">
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
            <label>Phone</label>
            <input v-model="form.phone" type="tel" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label>Gender</label>
            <select v-model="form.gender" class="form-control" required>
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="col-md-6 mb-3">
            <label>Date of Birth</label>
            <input v-model="form.dob" type="date" class="form-control" required />
          </div>

          <div class="col-md-12 mb-3">
            <label>Address</label>
            <textarea v-model="form.address" class="form-control" rows="3" required></textarea>
          </div>

          <div class="col-md-6 mb-3">
            <label>Insurance</label>
            <input v-model="form.insurance" type="text" class="form-control" />
          </div>
        </div>

        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-primary flex-grow-1" :disabled="isSubmitting">
            {{ isSubmitting ? 'Updating...' : 'Update Patient' }}
          </button>
          <button type="button" class="btn btn-secondary" @click="goBack">Cancel</button>
        </div>
      </form>

      <div v-else class="alert alert-info">Loading patient information...</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UpdatePatient',

  data() {
    return {
      message: '',
      alertType: 'success',
      isSubmitting: false,
      patientId: null,
      form: null,
    }
  },

  async mounted() {
    // Get patient ID from route query params
    this.patientId = this.$route.query.id

    if (!this.patientId) {
      this.message = 'Patient ID not found'
      this.alertType = 'danger'
      return
    }

    const token = localStorage.getItem('access_token')

    try {
      // Fetch full patient details from backend
      const response = await axios.get(`http://127.0.0.1:5000/get_patient/${this.patientId}`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      const patient = response.data

      // Initialize form with existing patient data
      this.form = {
        fn: patient.first_name || '',
        ln: patient.last_name || '',
        age: patient.age || null,
        phone: patient.phone || '',
        gender: patient.gender || '',
        dob: patient.dob || '',
        address: patient.address || '',
        insurance: patient.insurance || '',
      }
    } catch (error) {
      console.error('Error fetching patient details:', error)
      this.message = error.response?.data?.message || 'Failed to load patient details'
      this.alertType = 'danger'
      this.form = {
        fn: '',
        ln: '',
        age: null,
        phone: '',
        gender: '',
        dob: '',
        address: '',
        insurance: '',
      }
    }
  },

  methods: {
    async updatePatient() {
      const token = localStorage.getItem('access_token')

      if (!this.form.fn || !this.form.ln || !this.form.phone) {
        this.message = 'Please fill all required fields'
        this.alertType = 'warning'
        return
      }

      this.isSubmitting = true

      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/update_patient/${this.patientId}`,
          {
            fn: this.form.fn,
            ln: this.form.ln,
            age: this.form.age,
            phone: this.form.phone,
            gender: this.form.gender,
            dob: this.form.dob,
            address: this.form.address,
            insurance: this.form.insurance,
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        )

        this.message = response.data.message || 'Patient updated successfully'
        this.alertType = 'success'

        // Redirect back to dashboard after 2 seconds
        setTimeout(() => {
          this.$router.push('/admin/dashboard')
        }, 2000)
      } catch (error) {
        console.error('Error updating patient:', error)
        this.message = error.response?.data?.message || 'Failed to update patient'
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

input.form-control,
select.form-control,
textarea.form-control {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  font-size: 14px;
}

input.form-control:focus,
select.form-control:focus,
textarea.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  outline: none;
}

.d-flex.gap-2 {
  gap: 10px;
}
</style>
