import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Main Dashboard
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    // Authentication
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/PatientLoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },

    {
      path: '/patient/dashboard',
      name: 'patient-dashboard',
      component: () => import('../views/Patient/Dashboard.vue'),
    },

    {
      path: '/doctor/dashboard',
      name: 'doctor-dashboard',
      component: () => import('../views/Doctor/Dashboard.vue'),
    },

    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/Admin/Dashboard.vue'),
    },
    {
      path: '/admin/doctors',
      name: 'admin-doctors',
      component: () => import('../views/Admin/Add_Doctor.vue'),
    },
    {
      path: '/admin/update-doctor',
      name: 'admin-update-doctor',
      component: () => import('../views/Admin/Update_Doctor.vue'),
    },
    {
      path: '/admin/patients',
      name: 'admin-patients',
      component: () => import('../views/Admin/Patients.vue'),
    },
    {
      path: '/admin/update-patient',
      name: 'admin-update-patient',
      component: () => import('../views/Admin/Update_Patient.vue'),
    },
    {
      path: '/admin/appointments',
      name: 'admin-appointments',
      component: () => import('../views/Admin/Appointments.vue'),
    },
    {
      path: '/admin/search',
      name: 'admin-search',
      component: () => import('../views/Admin/Admin_Search.vue'),
    },
  ],
})

export default router
