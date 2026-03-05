<template>
  <div class="login-page">
    
    <!-- HEADER -->
    <header class="navbar bg-white d-flex align-items-center justify-content-between px-4">
      
      <div>
        <img src="@/assets/logo.png" height="80" width="80" alt="Logo" />
      </div>

      <div class="text-center">
        <h1>Vardha Hospital</h1>
      </div>

      <nav class="d-flex gap-3">
        <router-link to="/login" class="btn btn-outline-success">Patient Login</router-link>
        <router-link to="/login" class="btn btn-outline-secondary">Doctor Login</router-link>
        <router-link to="/login" class="btn btn-outline-primary">Admin Login</router-link>
      </nav>

    </header>

    <!-- SCROLLING BANNER -->
    <div class="scroll-container">
      <div class="scroll-text">
        Your health journey begins here — log in to care for yourself
      </div>
    </div>

    <!-- LOGIN FORM -->
    <div class="container mt-5">
      <div class="card shadow p-4 mx-auto login-card">

        <h2 class="text-center mb-4">Login Form</h2>

        <form @submit.prevent="loginUser">

          <input
            v-model="form.email"
            type="email"
            class="form-control mb-3"
            placeholder="Enter Your Email"
            required
          />

          <input
            v-model="form.password"
            type="password"
            class="form-control mb-3"
            placeholder="Enter Your Password"
            required
          />

          <button type="submit" class="btn btn-primary w-100">
            Login
          </button>

        </form>

        <!-- ERROR -->
        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>

        <!-- SIGNUP -->
        <div class="mt-3 text-center">
          <span>Don't have an account?</span>
          <router-link to="/register" class="ms-2">Sign Up</router-link>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "PatientLoginView",

  data(){
    return{
      form:{
        email:"",
        password:""
      },
      errorMessage:""
    }
  },

  methods:{

    async loginUser(){

      this.errorMessage=""

      try{

        const res = await axios.post(
          "http://127.0.0.1:5000/login",
          this.form
        )

        console.log("LOGIN RESPONSE:",res.data)

        // SAVE TOKEN
        localStorage.setItem("token",res.data.access_token)

        alert(res.data.message)

        // ROLE BASED REDIRECT
        if(res.data.role === 1){
          this.$router.push("/admin/dashboard")
        }
        else if(res.data.role === 2){
          this.$router.push("/doctor/dashboard")
        }
        else{
          this.$router.push("/patient/dashboard")
        }

      }
      catch(error){

        if(error.response){

          if(error.response.status === 401){

            alert("User does not exist. Please Sign Up.")
            this.$router.push("/register")

          }else{

            this.errorMessage = error.response.data.message

          }

        }else{

          this.errorMessage = "Server not reachable"

        }

      }

    }

  }

}
</script>

<style>

.login-page{
min-height:100vh;
background:linear-gradient(to right,#ccccff,#66ccff,#ff8566,#ccccff,#ff8566);
}

/* SCROLL BANNER */

.scroll-container{
background:black;
color:white;
overflow:hidden;
white-space:nowrap;
}

.scroll-text{
display:inline-block;
padding-left:100%;
animation:scroll 12s linear infinite;
}

@keyframes scroll{
from{transform:translateX(0%)}
to{transform:translateX(-100%)}
}

/* CARD */

.login-card{
max-width:450px;
border-radius:12px;
}

</style>