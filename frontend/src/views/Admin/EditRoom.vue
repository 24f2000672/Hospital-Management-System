<template>
  <div class="glass-page">
    <div class="container py-4">

      <div class="glass-card">

        <h2 class="mb-4">✏ Edit Room</h2>

        <div v-if="loading" class="text-center">
          Loading room...
        </div>

        <form v-else @submit.prevent="updateRoom">

          <div class="mb-3">
            <label class="form-label">Room Number</label>
            <input
              v-model="room.room_number"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Room Type</label>
            <input
              v-model="room.type"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Capacity</label>
            <input
              type="number"
              v-model="room.capacity"
              class="form-control"
              min="1"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Floor</label>
            <input
              type="number"
              v-model="room.floor"
              class="form-control"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Status</label>

            <select
              v-model="room.status"
              class="form-select"
            >
              <option value="AVAILABLE">
                AVAILABLE
              </option>

              <option value="OCCUPIED">
                OCCUPIED
              </option>

              <option value="MAINTENANCE">
                MAINTENANCE
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Notes</label>

            <textarea
              v-model="room.notes"
              class="form-control"
              rows="3"
            ></textarea>
          </div>

          <div class="d-flex gap-2">

            <button
              type="submit"
              class="btn btn-success"
            >
              💾 Update Room
            </button>

            <button
              type="button"
              class="btn btn-secondary"
              @click="$router.push('/admin/rooms')"
            >
              Cancel
            </button>

          </div>

        </form>

      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "EditRoom",

  props: ["id"],

  data() {
    return {
      loading: true,

      room: {
        room_number: "",
        type: "",
        capacity: 1,
        floor: 0,
        status: "AVAILABLE",
        notes: ""
      }
    };
  },

  async mounted() {
    await this.loadRoom();
  },

  methods: {

    async loadRoom() {

      try {

        const token =
          localStorage.getItem("access_token");

        const res = await axios.get(
          `http://127.0.0.1:5000/api/rooms/${this.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.room = res.data;

      } catch (err) {

        console.error(
          "LOAD ROOM ERROR",
          err.response?.data || err
        );

        alert("Failed to load room");

      } finally {
        this.loading = false;
      }
    },

    async updateRoom() {

      try {

        const token =
          localStorage.getItem("access_token");

        await axios.put(
          `http://127.0.0.1:5000/api/rooms/${this.id}`,
          this.room,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert("Room updated successfully");

        this.$router.push("/admin/rooms");

      } catch (err) {

        console.error(
          "UPDATE ROOM ERROR",
          err.response?.data || err
        );

        alert("Failed to update room");
      }
    }
  }
};
</script>

<style scoped>
.glass-page{
  min-height:100vh;
  background:linear-gradient(
    160deg,
    #08111f,
    #0f2a3b
  );
  padding:20px;
}

.glass-card{
  max-width:700px;
  margin:auto;
  background:rgba(255,255,255,.08);
  backdrop-filter:blur(14px);
  border-radius:20px;
  padding:30px;
  color:white;
}

.form-control,
.form-select{
  background:rgba(255,255,255,.15);
  border:none;
  color:white;
}

.form-control:focus,
.form-select:focus{
  box-shadow:none;
}

textarea{
  resize:none;
}
</style>