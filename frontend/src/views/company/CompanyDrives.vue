<template>
  <div>

    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container-fluid">

        <router-link class="navbar-brand fw-bold"
                     to="/company/dashboard">
          Placement Portal
        </router-link>

        <div class="collapse navbar-collapse">

          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/company/dashboard">
                Dashboard
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link"
                           active-class="active-link"
                           to="/company/drives">
                Company Drives
              </router-link>
            </li>
          </ul>

          <div class="d-flex align-items-center">
            <span class="text-white me-3 fw-semibold">
              {{ companyName }}
            </span>
            <button class="btn btn-outline-light btn-sm"
                    @click="logout">
              Logout
            </button>
          </div>

        </div>
      </div>
    </nav>


    <!-- CONTENT -->
    <div class="container py-4">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="fw-bold">Company Drives</h3>

        <router-link to="/company/create-drive"
                     class="btn btn-primary">
          ➕ Create Drive
        </router-link>
      </div>

      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary"></div>
      </div>

      <div v-else>

        <div v-if="drives.length === 0"
             class="alert alert-info text-center">
          No drives created yet
        </div>

        <div v-else>

          <div class="card shadow-sm mb-3"
               v-for="drive in drives"
               :key="drive.drive_id">

            <div class="card-body">

              <div class="row">

                <div class="col-md-8">

                  <h5 class="fw-bold">{{ drive.job_title }}</h5>

                  <p class="mb-1">
                    <strong>Deadline:</strong>
                    {{ formatDate(drive.application_deadline) }}
                  </p>

                  <p class="mb-1">
                    <strong>Status:</strong>
                    <span class="badge bg-warning"
                          v-if="drive.status==='Pending'">Pending</span>
                    <span class="badge bg-success"
                          v-else-if="drive.status==='Approved'">Approved</span>
                    <span class="badge bg-secondary"
                          v-else>Closed</span>
                  </p>

                </div>

                <div class="col-md-4 text-md-end">

                  <h5>{{ drive.applicants_count }}</h5>
                  <small class="text-muted">Applicants</small>

                  <div class="mt-3"
                       v-if="drive.status==='Approved'">
                    <router-link
                      :to="`/company/drive/${drive.drive_id}/applications`"
                      class="btn btn-sm btn-outline-primary">
                      View Applications
                    </router-link>
                  </div>

                </div>

              </div>

            </div>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>


<script>
import axios from "axios";
const API = "http://localhost:5000/api/company";

export default {

  data() {
    return {
      drives: [],
      companyName: "",
      loading: true
    };
  },

  mounted() {
    this.fetchDrives();
  },

  methods: {

    async fetchDrives() {
      this.loading = true;

      const res = await axios.get(`${API}/dashboard`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      });

      this.drives = res.data.drives;
      this.companyName = res.data.company_name;
      this.loading = false;
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },

    logout() {
      localStorage.clear();
      this.$router.push("/");
    }

  }

};
</script>

<style scoped>
.active-link {
  color: #ffc107 !important;
  font-weight: 600;
}
.card {
  border-radius: 12px;
}
</style>