<template>
  <div class="glass-page container py-4">

    <!-- HEADER -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="page-title">🛏 Room Management</h2>

      <button class="btn btn-success" @click="goToAddRoom">
        ➕ Add Room
      </button>
    </div>

    <!-- STATS -->
    <div class="row mb-4 text-center">

      <div class="col-md-4">
        <div class="stat-card">
          <h3>{{ rooms.length }}</h3>
          <p>Total Rooms</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="stat-card green">
          <h3>{{ availableCount }}</h3>
          <p>Available</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="stat-card red">
          <h3>{{ occupiedCount }}</h3>
          <p>Occupied</p>
        </div>
      </div>

    </div>

    <!-- SEARCH -->
    <input
      v-model="search"
      class="form-control mb-3"
      placeholder="🔍 Search room number or type..."
    />

    <!-- LOADING -->
    <div v-if="loading" class="text-white text-center">
      Loading rooms...
    </div>

    <!-- ROOMS GRID -->
    <div v-else class="row g-4">

      <div
        v-for="room in filteredRooms"
        :key="room.id"
        class="col-lg-3 col-md-4 col-sm-6"
      >
        <div class="room-card">

          <h4>Room {{ room.room_number }}</h4>

          <p class="room-type">{{ room.type }}</p>

          <span
            class="badge"
            :class="room.status === 'AVAILABLE' ? 'bg-success' : 'bg-danger'"
          >
            {{ room.status }}
          </span>

        </div>
      </div>

    </div>

    <div v-if="!loading && filteredRooms.length === 0" class="text-center mt-4 text-white">
      No rooms found
    </div>

    <!-- ADD ROOM MODAL -->
    <div v-if="showAddModal" class="modal-backdrop">

      <div class="modal-box">

        <h4>Add Room</h4>

        <input
          v-model="newRoom.room_number"
          class="form-control mb-2"
          placeholder="Room Number"
        />

        <input
          v-model="newRoom.type"
          class="form-control mb-2"
          placeholder="Type (ICU/General)"
        />

        <select v-model="newRoom.status" class="form-control mb-3">
          <option value="AVAILABLE">AVAILABLE</option>
          <option value="OCCUPIED">OCCUPIED</option>
          <option value="MAINTENANCE">MAINTENANCE</option>
        </select>

        <button class="btn btn-primary w-100" @click="addRoom">
          Save
        </button>

        <button class="btn btn-secondary w-100 mt-2" @click="showAddModal = false">
          Cancel
        </button>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RoomManagement",

  data() {
    return {
      rooms: [],
      loading: true,
      search: "",
      showAddModal: false,

      newRoom: {
        room_number: "",
        type: "",
        status: "AVAILABLE"
      }
    };
  },

  computed: {
    filteredRooms() {
      return this.rooms.filter(r =>
        (r.room_number + "").toLowerCase().includes(this.search.toLowerCase()) ||
        (r.type || "").toLowerCase().includes(this.search.toLowerCase())
      );
    },

    availableCount() {
      return this.rooms.filter(r => r.status === "AVAILABLE").length;
    },

    occupiedCount() {
      return this.rooms.filter(r => r.status === "OCCUPIED").length;
    }
  },

  async mounted() {
    await this.loadRooms();
  },

  methods: {

    // ---------------- LOAD ROOMS ----------------
    async loadRooms() {
      try {
        this.loading = true;

        const token = localStorage.getItem("access_token");

        const res = await axios.get(
          "http://127.0.0.1:5000/api/rooms",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.rooms = res.data;

      } catch (err) {
        console.error("LOAD ROOMS ERROR:", err.response?.data || err.message);
      } finally {
        this.loading = false;
      }
    },

    // ---------------- ADD ROOM ----------------
    async addRoom() {
      try {
        const token = localStorage.getItem("access_token");

        const payload = {
          room_number: this.newRoom.room_number,
          type: this.newRoom.type,
          status: this.newRoom.status
        };

        const res = await axios.post(
          "http://127.0.0.1:5000/api/rooms",
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        console.log("ROOM ADDED:", res.data);

        this.showAddModal = false;

        this.newRoom = {
          room_number: "",
          type: "",
          status: "AVAILABLE"
        };

        await this.loadRooms();

      } catch (err) {
        console.error("ADD ROOM ERROR:", err.response?.data || err.message);
        alert("Failed to add room. Check backend.");
      }
    },
    goToAddRoom() {
  this.$router.push("/admin/add-room");
}
  }
};
</script>

<style scoped>
.glass-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #08111f, #0f2a3b);
}

.page-title {
  color: white;
  font-weight: bold;
}

.room-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(12px);
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  color: white;
}

.room-card:hover {
  transform: scale(1.03);
  transition: 0.3s;
}

.stat-card {
  background: rgba(255,255,255,0.1);
  padding: 15px;
  border-radius: 12px;
  color: white;
}

.stat-card.green {
  border-left: 4px solid #22c55e;
}

.stat-card.red {
  border-left: 4px solid #ef4444;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
}
</style>