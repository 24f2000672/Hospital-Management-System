<template>
<div class="glass-page">

<div class="page-header">
<h2>🏥 Departments</h2>

<button class="btn btn-success">
Add Department
</button>
</div>

<div class="row">

<div
class="col-md-4 mb-4"
v-for="dept in departments"
:key="dept.id"
>

<div class="glass-card">

<h4>{{ dept.name }}</h4>

<p>{{ dept.description }}</p>

<button class="btn btn-primary">
Manage
</button>

</div>

</div>

</div>

</div>
</template>