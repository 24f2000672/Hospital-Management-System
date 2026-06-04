<template>

<div class="glass-page">

<h2>🏥 Admissions</h2>

<table class="table table-striped">

<tr>
<th>Patient</th>
<th>Room</th>
<th>Date</th>
<th>Status</th>
</tr>

<tr
v-for="admission in admissions"
:key="admission.id"
>

<td>{{ admission.patient }}</td>
<td>{{ admission.room }}</td>
<td>{{ admission.date }}</td>
<td>{{ admission.status }}</td>

</tr>

</table>

</div>

</template>