<template>
  <div>

    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container-fluid">

        <router-link class="navbar-brand fw-bold"
                     to="/student/dashboard">
          🎓 Placement Portal
        </router-link>

        <div class="collapse navbar-collapse">

          <!-- LEFT MENU -->
          <ul class="navbar-nav me-auto">

            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/student/dashboard">
                Dashboard
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/student/companies">
                Companies
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/student/drives">
                Drives
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/student/history">
                History
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/student/profile">
                Profile
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/student/reports">
                Reports
              </router-link>
            </li>

          </ul>

          <!-- RIGHT SIDE -->
          <div class="d-flex align-items-center">
            <span class="text-white me-3 fw-semibold">
              {{ student.full_name }}
            </span>

            <button class="btn btn-outline-light btn-sm"
                    @click="logout">
              Logout
            </button>
          </div>

        </div>
      </div>
    </nav>

    <!-- PAGE CONTENT -->
    <div class="container py-4">
      <router-view />
    </div>

  </div>
</template>

<script>
import axios from "axios"
const API = "http://localhost:5000/api/student"

export default {

  data() {
    return {
      student: {
        full_name: ""
      }
    }
  },

  mounted() {
    this.fetchStudent()
  },

  methods: {

    async fetchStudent() {
      try {
        const res = await axios.get(`${API}/me`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })

        this.student = res.data

      } catch (err) {
        console.error(err)
      }
    },

    logout() {
      localStorage.clear()
      this.$router.push("/")
    }

  }
}
</script>

<style scoped>
.active-link {
  color: #ffc107 !important;
  font-weight: 600;
}
</style>