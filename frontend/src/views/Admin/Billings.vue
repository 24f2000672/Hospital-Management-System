<template>

<div class="glass-page">

<h2>💳 Billing</h2>

<table class="table">

<tr>
<th>Patient</th>
<th>Consultation</th>
<th>Medicine</th>
<th>Total</th>
<th>Status</th>
</tr>

<tr
v-for="bill in bills"
:key="bill.id"
>

<td>{{ bill.patient }}</td>
<td>₹{{ bill.consultation_fees }}</td>
<td>₹{{ bill.medicine_fees }}</td>
<td>₹{{ bill.total_amount }}</td>

<td>

<span
class="badge"
:class="
bill.status==='PAID'
?'bg-success'
:'bg-warning'
"
>

{{ bill.status }}

</span>

</td>

</tr>

</table>

</div>

</template>