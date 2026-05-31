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
      path: '/patient/profile',
      name: 'patient-profile',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Patient Profile',
        moduleKey: 'patient-profile',
      },
    },
    {
      path: '/patient/medical-records',
      name: 'patient-medical-records',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Medical Records',
        moduleKey: 'medical-records',
      },
    },
    {
      path: '/patient/reports',
      name: 'patient-reports',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Health Reports',
        moduleKey: 'reports',
      },
    },
    {
      path: '/patient/appointment-booking',
      name: 'patient-appointment-booking',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Appointment Booking',
        moduleKey: 'appointment-booking',
      },
    },
    {
      path: '/patient/my-appointments',
      name: 'patient-my-appointments',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'My Appointments',
        moduleKey: 'my-appointments',
      },
    },
    {
      path: '/patient/medicine-reminder',
      name: 'patient-medicine-reminder',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Medicine Reminder',
        moduleKey: 'medicine-reminder',
      },
    },
    {
      path: '/patient/emergency-sos',
      name: 'patient-emergency-sos',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Emergency SOS',
        moduleKey: 'emergency-sos',
      },
    },
    {
      path: '/patient/ai-health-assistant',
      name: 'patient-ai-assistant',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'AI Health Assistant',
        moduleKey: 'ai-assistant',
      },
    },
    {
      path: '/patient/accessibility',
      name: 'patient-accessibility',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Accessibility',
        moduleKey: 'accessibility',
      },
    },
    {
      path: '/patient/health-card',
      name: 'patient-health-card',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Health Card',
        moduleKey: 'health-card',
      },
    },
    {
      path: '/patient/history/:id',
      name: 'patient-history',
      component: () => import('../views/Patient/History.vue'),
    },
    {
      path: '/patient/doctor-profile/:id?',
      name: 'patient-doctor-profile',
      component: () => import('../views/Patient/DoctorProfile.vue'),
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
      path: '/doctor/patient-history/:id?',
      name: 'doctor-patient-history',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Patient History',
        moduleKey: 'doctor-history',
      },
    },
    {
      path: '/doctor/manage-slots/:doc_id',
      name: 'doctor-manage-slots',
      component: () => import('../views/Doctor/ManageSlots.vue'),
    },
    {
      path: '/doctor/monthly-reports',
      name: 'doctor-monthly-reports',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Monthly Reports',
        moduleKey: 'monthly-reports',
      },
    },
    {
      path: '/doctor/telemedicine',
      name: 'doctor-telemedicine',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Telemedicine',
        moduleKey: 'telemedicine',
      },
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
      path: '/admin/manage-doctors',
      name: 'admin-manage-doctors',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Manage Doctors',
        moduleKey: 'manage-doctors',
      },
    },
    {
      path: '/admin/manage-patients',
      name: 'admin-manage-patients',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Manage Patients',
        moduleKey: 'manage-patients',
      },
    },
    {
      path: '/admin/departments',
      name: 'admin-departments',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Departments',
        moduleKey: 'departments',
      },
    },
    {
      path: '/admin/analytics',
      name: 'admin-analytics',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Analytics',
        moduleKey: 'analytics',
      },
    },
    {
      path: '/admin/emergency-monitor',
      name: 'admin-emergency-monitor',
      component: () => import('../views/Shared/ModuleWorkspace.vue'),
      meta: {
        title: 'Emergency Monitor',
        moduleKey: 'emergency-monitor',
      },
    },
    {
      path: '/admin/rooms',
      name: 'admin-rooms',
      component: () => import('../views/Shared/HospitalManagementWorkspace.vue'),
      meta: {
        title: 'Rooms',
        moduleKey: 'rooms',
      },
    },
    {
      path: '/admin/admissions',
      name: 'admin-admissions',
      component: () => import('../views/Shared/HospitalManagementWorkspace.vue'),
      meta: {
        title: 'Admissions',
        moduleKey: 'admissions',
      },
    },
    {
      path: '/admin/billing',
      name: 'admin-billing',
      component: () => import('../views/Shared/HospitalManagementWorkspace.vue'),
      meta: {
        title: 'Billing',
        moduleKey: 'billing',
      },
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
