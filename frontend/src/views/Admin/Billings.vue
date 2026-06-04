<template>
  <div class="glass-page">
    <div class="container py-4">
      <h2 class="page-title">💳 Billing Management</h2>

      <div class="table-responsive">
        <table class="table table-dark table-hover align-middle">
          <thead>
            <tr>
              <th>Patient</th>
              <th>Consultation</th>
              <th>Medicine</th>
              <th>Total</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="bill in bills" :key="bill.id">
              <td>{{ bill.patient }}</td>
              <td>₹{{ bill.consultation_fees }}</td>
              <td>₹{{ bill.medicine_fees }}</td>
              <td>₹{{ bill.total_amount }}</td>

              <td>
                <span
                  class="badge"
                  :class="
                    bill.status === 'PAID'
                      ? 'bg-success'
                      : 'bg-warning text-dark'
                  "
                >
                  {{ bill.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="bills.length === 0" class="text-center mt-4">
        <h5>No Billing Records Found</h5>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'BillingView',

  data() {
    return {
      bills: [],
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')

      const response = await axios.get(
        'http://127.0.0.1:5000/admin/billing',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      this.bills = response.data
    } catch (error) {
      console.error('Billing Error:', error)
      alert('Failed to load billing records')
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
  font-weight: 700;
  margin-bottom: 25px;
}

.table {
  border-radius: 15px;
  overflow: hidden;
}
</style>