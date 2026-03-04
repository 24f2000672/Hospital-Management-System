<template>
  <div class="home-page">
    <!-- Header -->
    <header class="navbar bg-white d-flex justify-content-between align-items-center px-4">
      <div>
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>

      <div class="text-center">
        <h1>Vardha Hospital</h1>
      </div>

      <nav class="d-flex gap-3">
        <router-link to="/login" class="btn btn-outline-success"> Patient Login </router-link>

        <router-link to="/login" class="btn btn-outline-warning"> Doctor Login </router-link>

        <router-link to="/login" class="btn btn-outline-primary"> Admin Login </router-link>
      </nav>
    </header>

    <!-- Scrolling Banner (Modern Marquee Replacement) -->
    <div class="scroll-container">
      <div class="scroll-text">
        Welcome to Vardha Hospitals. To proceed further, Login or Signup.
      </div>
    </div>

    <!-- Welcome Title -->
    <div class="text-center mt-4">
      <h2 class="title-heading">🏥 Welcome to the Hospital Dashboard</h2>
    </div>

    <br />

    <!-- Main Section -->
    <div class="container-fluid mt-4 px-5">
      <div class="row align-items-center">
        <div class="col-md-6">
          <p class="content-text">
            <b>
              Welcome to Varsha Multispeciality Hospital, where compassion meets innovation. This
              dashboard serves as the central hub for managing and understanding the hospital’s
              overall operations, services, and facilities.
            </b>
          </p>

          <hr />

          <h3 class="text-center">💙 About the Hospital</h3>

          <p class="content-text text-center">
            <b>
              Vardha Multispeciality Hospital is a leading healthcare institution committed to
              delivering world-class medical care with advanced technology and human touch.
            </b>
          </p>
        </div>

        <div class="col-md-6 text-center">
          <img src="@/assets/doc.jpg" class="img-fluid rounded shadow" />
        </div>
      </div>
    </div>

    <hr />

    <!-- Mission -->
    <h3 class="text-center">🩺 Our Mission</h3>
    <p class="content-text text-center">
      <b>
        Our mission is to promote health, prevent illness, and provide the highest quality care to
        every patient.
      </b>
    </p>

    <hr />

    <!-- Departments -->
    <h3 class="text-center">⚕️ Our Departments</h3>

    <p class="content-text text-center">We provide specialized care through:</p>

    <ul class="list-unstyled text-center content-text">
      <li>General Medicine</li>
      <li>Cardiology</li>
      <li>Neurology</li>
      <li>Orthopedics</li>
      <li>Pediatrics</li>
      <li>Gynecology</li>
      <li>Emergency & Critical Care</li>
      <li>Diagnostics and Laboratory Services</li>
    </ul>

    <hr />

    <!-- Digital Management -->
    <h3 class="text-center">💻 Digital Hospital Management</h3>
    <p class="content-text text-center">
      This digital dashboard ensures smooth communication and efficient healthcare management.
    </p>

    <hr />

    <!-- Values -->
    <h3 class="text-center">🌿 Our Values</h3>

    <ul class="list-unstyled text-center content-text">
      <li><b>Compassion:</b> Treating every patient with empathy.</li>
      <li><b>Integrity:</b> Upholding honesty and professionalism.</li>
      <li><b>Excellence:</b> Continuous improvement and innovation.</li>
      <li><b>Collaboration:</b> Working together for best care.</li>
    </ul>

    <hr />

    <!-- Commitment -->
    <h3 class="text-center">💖 Commitment to Care</h3>
    <p class="content-text text-center">
      We are more than a hospital — we are a family that cares for every individual.
    </p>
  </div>
</template>

<script setup></script>

<style>
.home-page {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(to right, #ccccff, #66ccff, #ff8566, #ccccff, #ff8566);
}

.scroll-container {
  background-color: black;
  color: white;
  overflow: hidden;
  white-space: nowrap;
}

.scroll-text {
  display: inline-block;
  padding-left: 100%;
  animation: scroll 12s linear infinite;
}

@keyframes scroll {
  from {
    transform: translateX(0%);
  }
  to {
    transform: translateX(-100%);
  }
}

.title-heading {
  color: rgb(5, 60, 150);
}

.content-text {
  color: rgb(74, 41, 41);
}

html,
body {
  margin: 0;
  padding: 0;
}
</style>
