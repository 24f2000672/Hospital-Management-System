import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // Home
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

    // Patient
    {
      path: '/patient/dashboard',
      name: 'patient-dashboard',
      component: () => import('../views/Patient/Dashboard.vue'),
    },
    {
      path: '/patient/history/:id',
      name: 'patient-history',
      component: () => import('../views/Patient/History.vue'),
    },
    {
      path: '/editpatient/:id',
      name: 'patient-edit',
      component: () => import('../views/Patient/EditPatient.vue'),
    },

    // Doctor
    {
      path: '/doctor/dashboard',
      name: 'doctor-dashboard',
      component: () => import('../views/Doctor/Dashboard.vue'),
    },
    {
      path: '/doctor/manage-slots/:doc_id',
      name: 'doctor-manage-slots',
      component: () => import('../views/Doctor/ManageSlots.vue'),
    },
    {
      path: '/doctor/treatment/:id',
      name: 'doctor-treatment',
      component: () => import('../views/Doctor/AddTreatment.vue'),
    },

    // Admin
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

    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFound.vue'),
    },
  ],
})

export default router
