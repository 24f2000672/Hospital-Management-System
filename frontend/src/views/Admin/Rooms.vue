<template>
  <div class="glass-page">
    <div class="container py-4">
      <h2 class="page-title">🛏 Room Management</h2>

      <div class="row g-4">
        <div
          v-for="room in rooms"
          :key="room.id"
          class="col-lg-3 col-md-4 col-sm-6"
        >
          <div class="room-card">
            <h4>{{ room.room_number }}</h4>

            <p class="room-type">{{ room.type }}</p>

            <span
              :class="
                room.status === 'AVAILABLE'
                  ? 'badge bg-success'
                  : 'badge bg-danger'
              "
            >
              {{ room.status }}
            </span>
          </div>
        </div>
      </div>

      <div v-if="rooms.length === 0" class="text-center mt-5">
        <h5>No Rooms Found</h5>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RoomsView',

  data() {
    return {
      rooms: [],
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')

      const response = await axios.get(
        'http://127.0.0.1:5000/admin/rooms',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      this.rooms = response.data
    } catch (error) {
      console.error('Error loading rooms:', error)
      alert('Failed to load rooms')
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

.room-card {
  padding: 20px;
  border-radius: 20px;
  text-align: center;

  background: rgba(255, 255, 255, 0.08);

  backdrop-filter: blur(15px);

  border: 1px solid rgba(255, 255, 255, 0.15);

  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);

  transition: all 0.3s ease;
}

.room-card:hover {
  transform: translateY(-5px);
}

.room-card h4 {
  color: white;
  font-weight: 700;
}

.room-type {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 12px;
}
</style>