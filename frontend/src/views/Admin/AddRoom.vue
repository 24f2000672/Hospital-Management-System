<template>
  <div class="glass-page">
    <div class="container py-4">

      <h2 class="page-title">➕ Add New Room</h2>

      <div class="glass-card p-4">

        <form @submit.prevent="submitRoom">

          <!-- Room Number -->
          <div class="mb-3">
            <label class="form-label">Room Number</label>
            <input
              v-model="room.room_number"
              type="text"
              class="form-control"
              placeholder="Enter room number (e.g. 101A)"
              required
            />
          </div>

          <!-- Room Type -->
          <div class="mb-3">
            <label class="form-label">Room Type</label>
            <select v-model="room.type" class="form-select" required>
              <option disabled value="">Select type</option>
              <option>General</option>
              <option>Private</option>
              <option>ICU</option>
              <option>Emergency</option>
            </select>
          </div>

          <!-- Capacity -->
          <div class="mb-3">
            <label class="form-label">Capacity</label>
            <input
              v-model.number="room.capacity"
              type="number"
              min="1"
              class="form-control"
              placeholder="Number of beds"
              required
            />
          </div>

          <!-- Floor -->
          <div class="mb-3">
            <label class="form-label">Floor</label>
            <input
              v-model.number="room.floor"
              type="number"
              min="0"
              class="form-control"
              placeholder="Floor number"
              required
            />
          </div>

          <!-- Status -->
          <div class="mb-3">
            <label class="form-label">Status</label>
            <select v-model="room.status" class="form-select" required>
              <option value="AVAILABLE">AVAILABLE</option>
              <option value="OCCUPIED">OCCUPIED</option>
              <option value="MAINTENANCE">MAINTENANCE</option>
            </select>
          </div>

          <!-- Buttons -->
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-success">
              💾 Save Room
            </button>

            <button type="reset" class="btn btn-secondary" @click="resetForm">
              🔄 Reset
            </button>
          </div>

        </form>

        <!-- Message -->
        <div v-if="message" class="alert mt-3" :class="messageClass">
          {{ message }}
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddRoom",

  data() {
    return {
      room: {
        room_number: "",
        type: "",
        capacity: 1,
        floor: 0,
        status: "AVAILABLE"
      },
      message: "",
      messageClass: ""
    };
  },

  methods: {

    // ---------------- SUBMIT ROOM ----------------
    async submitRoom() {
      try {
        const token = localStorage.getItem("access_token");

        if (!token) {
          this.message = "Login required!";
          this.messageClass = "alert-danger";
          return;
        }

        const payload = {
          room_number: this.room.room_number,
          type: this.room.type,
          capacity: this.room.capacity,
          floor: this.room.floor,
          status: this.room.status
        };

        const response = await axios.post(
          "http://127.0.0.1:5000/api/rooms",
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        console.log("ROOM CREATED:", response.data);

        this.message = "Room added successfully!";
        this.messageClass = "alert-success";

        this.resetForm();

      } catch (error) {
        console.error("ADD ROOM ERROR:", error.response?.data || error.message);

        this.message = error.response?.data?.message || "Failed to add room!";
        this.messageClass = "alert-danger";
      }
    },

    // ---------------- RESET FORM ----------------
    resetForm() {
      this.room = {
        room_number: "",
        type: "",
        capacity: 1,
        floor: 0,
        status: "AVAILABLE"
      };
    }
  }
};
</script>

<style scoped>
.glass-page {
  min-height: 100vh;
  background: #0f172a;
  color: white;
}

.page-title {
  font-weight: bold;
  margin-bottom: 20px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>