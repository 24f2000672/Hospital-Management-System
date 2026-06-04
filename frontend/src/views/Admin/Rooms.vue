<template>

<div class="glass-page">

<h2>🛏 Room Management</h2>

<div class="row">

<div
v-for="room in rooms"
:key="room.id"
class="col-md-3"
>

<div class="room-card">

<h3>{{ room.room_number }}</h3>

<p>{{ room.type }}</p>

<span
:class="room.status === 'AVAILABLE'
?'badge bg-success'
:'badge bg-danger'"
>

{{ room.status }}

</span>

</div>

</div>

</div>

</div>

</template>
<script>
import axios from "axios"
mounted() {
    axios.get("http://127.0.0.1:5000/admin/rooms")
    .then(res=>{
        this.rooms = res.data
    })
}
</script>
