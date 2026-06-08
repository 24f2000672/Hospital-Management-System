import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminEditPatient from '../views/Admin/AdminEditPatient.vue'  // ✅ FIXED IMPORT
import AddRoom from '../views/Admin/AddRoom.vue'  // ✅ FIXED IMPORT

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // ================= HOME =================
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    // ================= AUTH =================
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

    // ================= PATIENT =================
    {
      path: '/patient/dashboard',
      name: 'patient-dashboard',
      component: () => import('../views/Patient/Dashboard.vue'),
    },

    {
      path: '/patient/tabs',
      name: 'patient-tabs',
      component: () => import('../views/Patient/MobileTabsView.vue'),
    },

    {
      path: '/editpatient/:id',
      name: 'patient-edit',
      component: () => import('../views/Patient/EditPatient.vue'),
    },

    // ================= ADMIN =================
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/Admin/Dashboard.vue'),
    },

    {
      path: '/admin/departments',
      name: 'admin-departments',
      component: () => import('../views/Admin/Departments.vue'),
    },
    {
      path: '/admin/analytics',
      name: 'admin-analytics',
      component: () => import('../views/Admin/Analytics.vue'),
    },
    {
      path: '/admin/billing',
      name: 'admin-billing',
      component: () => import('../views/Admin/Billings.vue'),
    },
    {
      path: '/admin/rooms',
      name: 'admin-rooms',
      component: () => import('../views/Admin/Rooms.vue'),
    },
    {
      path: '/admin/add-room',
      name: 'admin-add-room',
      component: () => import('../views/Admin/AddRoom.vue'),
    },

    {
      path: '/admin/manage-patients',
      name: 'admin-manage-patients',
      component: () => import('../views/Admin/PatientsManagement.vue'),
    },

    // ✅ EDIT PATIENT (FIXED)
    {
      path: '/admin/patients/edit/:id',
      name: 'admin-edit-patient',
      component: AdminEditPatient,
      props: true,
    },

    {
      path: '/admin/manage-doctors',
      name: 'admin-manage-doctors',
      component: () => import('../views/Admin/DoctorsManagement.vue'),
    },

    {
      path: '/admin/appointments',
      name: 'admin-appointments',
      component: () => import('../views/Admin/Appointments.vue'),
    },

    // ================= FALLBACK =================
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFound.vue'),
    },
  ],
})

export default router