<template>
<div class="glass-page">

<h2>🧑 Patients Management</h2>

<div class="glass-card">

<table class="table table-hover">

<tr>
<th>ID</th>
<th>Name</th>
<th>Age</th>
<th>Gender</th>
<th>Phone</th>
<th>Actions</th>
</tr>

<tr v-for="patient in patients" :key="patient.id">

<td>{{ patient.id }}</td>
<td>{{ patient.first_name }}</td>
<td>{{ patient.age }}</td>
<td>{{ patient.gender }}</td>
<td>{{ patient.phone }}</td>

<td>
<button class="btn btn-warning btn-sm">
Edit
</button>

<button class="btn btn-danger btn-sm">
Delete
</button>
</td>

</tr>

</table>

</div>
</div>
</template>