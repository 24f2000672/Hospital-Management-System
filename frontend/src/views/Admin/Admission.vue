<template>
  <div class="glass-page">
    <div class="container py-4">
      <h2 class="page-title">🏥 Admissions Management</h2>

      <div class="table-responsive">
        <table class="table table-dark table-hover align-middle">
          <thead>
            <tr>
              <th>Patient</th>
              <th>Room</th>
              <th>Admission Date</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="admission in admissions"
              :key="admission.id"
            >
              <td>{{ admission.patient }}</td>
              <td>{{ admission.room }}</td>
              <td>{{ admission.admission_date }}</td>

              <td>
                <span
                  class="badge"
                  :class="
                    admission.status === 'ADMITTED'
                      ? 'bg-success'
                      : 'bg-secondary'
                  "
                >
                  {{ admission.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="admissions.length === 0"
        class="text-center mt-4"
      >
        <h5>No Admissions Found</h5>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdmissionsView',

  data() {
    return {
      admissions: [],
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')

      const response = await axios.get(
        'http://127.0.0.1:5000/admin/admissions',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      this.admissions = response.data
    } catch (error) {
      console.error('Admissions Error:', error)
      alert('Failed to load admissions')
    }
  },
}
</script>

<style scoped>
.glass-page {
  min-height: 100vh;
  padding: 30px;
  background:
    radial-gradient(circle at top left,
      rgba(45, 212, 191, 0.25),
      transparent 30%),
    radial-gradient(circle at top right,
      rgba(249, 115, 22, 0.25),
      transparent 30%),
    linear-gradient(
      160deg,
      #08111f 0%,
      #0f2a3b 50%,
      #123b52 100%
    );
}

.page-title {
  color: white;
  margin-bottom: 25px;
  font-weight: 700;
}

.table {
  border-radius: 15px;
  overflow: hidden;
}
</style>