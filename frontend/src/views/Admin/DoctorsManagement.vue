<template>
<div class="glass-page">
  <div class="page-header">
    <h2>👨‍⚕️ Doctors Management</h2>
    <button class="btn btn-success">
      Add Doctor
    </button>
  </div>

  <div class="glass-card">
    <table class="table table-dark table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Department</th>
          <th>Experience</th>
          <th>Contact</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="doctor in doctors" :key="doctor.id">
          <td>{{ doctor.id }}</td>
          <td>{{ doctor.first_name }} {{ doctor.last_name }}</td>
          <td>{{ doctor.department }}</td>
          <td>{{ doctor.experience }}</td>
          <td>{{ doctor.contact }}</td>

          <td>
            <button class="btn btn-warning btn-sm">
              Edit
            </button>

            <button class="btn btn-danger btn-sm ms-2">
              Delete
            </button>
          </td>

        </tr>
      </tbody>
    </table>
  </div>
</div>
</template>