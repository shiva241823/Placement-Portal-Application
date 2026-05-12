import { createRouter, createWebHistory } from "vue-router"

/* ========================
   AUTH PAGES
======================== */
import LoginView from "../views/LoginView.vue"
import RegisterStudent from "../views/RegisterStudent.vue"
import RegisterCompany from "../views/RegisterCompany.vue"

/* ========================
   ADMIN PAGES
======================== */
import AdminDashboard from "../views/admin/AdminDashboard.vue"
import ManageCompanies from "../views/admin/ManageCompanies.vue"
import ManageStudents from "../views/admin/ManageStudents.vue"
import ManageDrives from "../views/admin/ManageDrives.vue"
import Applications from "../views/admin/Applications.vue"
import Reports from "../views/admin/Reports.vue"
import AdminDriveApplications from "../views/admin/AdminDriveApplications.vue"

/* ========================
   COMPANY PAGES
======================== */
import CompanyDashboard from "../views/company/CompanyDashboard.vue"
import CreateDrive from "../views/company/CreateDrive.vue"
import CompanyDrives from "../views/company/CompanyDrives.vue"
import DriveApplications from "../views/company/DriveApplications.vue"

/* ========================
   STUDENT PAGES
======================== */
import StudentLayout from "../views/student/StudentLayout.vue"
import StudentDashboard from "../views/student/StudentDashboard.vue"
import StudentCompanies from "../views/student/StudentCompanies.vue"
import StudentCompanyDrives from "../views/student/StudentCompanyDrives.vue"
import StudentDrives from "../views/student/StudentDrives.vue"
import StudentHistory from "../views/student/StudentHistory.vue"
import StudentProfile from "../views/student/StudentProfile.vue"
import StudentReports from "../views/student/StudentReports.vue"


const routes = [

  /* ========================
     PUBLIC ROUTES
  ======================== */
  { path: "/", component: LoginView },
  { path: "/register-student", component: RegisterStudent },
  { path: "/register-company", component: RegisterCompany },

  /* ========================
     ADMIN ROUTES
  ======================== */
  { path: "/admin/dashboard", component: AdminDashboard, meta: { role: "admin" } },
  { path: "/admin/companies", component: ManageCompanies, meta: { role: "admin" } },
  { path: "/admin/students", component: ManageStudents, meta: { role: "admin" } },
  { path: "/admin/drives", component: ManageDrives, meta: { role: "admin" } },
  { path: "/admin/applications", component: Applications, meta: { role: "admin" } },
  { path: "/admin/reports", component: Reports, meta: { role: "admin" } },

  {
    path: "/admin/drive/:id/applications",
    component: AdminDriveApplications,
    meta: { role: "admin" }
  },

  /* ========================
     COMPANY ROUTES
  ======================== */
  { path: "/company/dashboard", component: CompanyDashboard, meta: { role: "company" } },
  { path: "/company/create-drive", component: CreateDrive, meta: { role: "company" } },
  { path: "/company/drives", component: CompanyDrives, meta: { role: "company" } },
  { path: "/company/drive/:id/applications", component: DriveApplications, meta: { role: "company" } },

  /* ========================
     STUDENT ROUTES (NESTED)
  ======================== */
  {
    path: "/student",
    component: StudentLayout,
    meta: { role: "student" },
    children: [
      { path: "dashboard", component: StudentDashboard },
      { path: "companies", component: StudentCompanies },
      { path: "company/:id/drives", component: StudentCompanyDrives },
      { path: "drives", component: StudentDrives },
      { path: "history", component: StudentHistory },
      { path: "profile", component: StudentProfile },
      { path: "reports", component: StudentReports }
    ]
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

/* ========================
   ROLE-BASED ROUTE GUARD
======================== */
router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("access_token")
  const role = localStorage.getItem("role")

  // 🔐 Not logged in but trying protected route
  if (to.meta.role && !token) {
    return next("/")
  }

  // 🔄 Logged in but trying to access login page
  if (token && to.path === "/") {
    if (role === "admin") return next("/admin/dashboard")
    if (role === "company") return next("/company/dashboard")
    if (role === "student") return next("/student/dashboard")
  }

  // ❌ Role mismatch
  if (to.meta.role && role !== to.meta.role) {
    if (role === "admin") return next("/admin/dashboard")
    if (role === "company") return next("/company/dashboard")
    if (role === "student") return next("/student/dashboard")
    return next("/")
  }

  next()
})

export default router