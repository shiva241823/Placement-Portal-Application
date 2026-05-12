<template>
  <div>

    <!-- ===================== -->
    <!-- COMPANY NAVBAR -->
    <!-- ===================== -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container-fluid">

        <router-link class="navbar-brand fw-bold"
                     to="/company/dashboard">
          Placement Portal
        </router-link>

        <button class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#companyNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="companyNavbar">

          <!-- LEFT MENU -->
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

          <!-- RIGHT SIDE -->
          <div class="d-flex align-items-center">

            <span class="text-white me-3 fw-semibold">
              {{ company.company_name }}
            </span>

            <button class="btn btn-outline-light btn-sm"
                    @click="logout">
              Logout
            </button>

          </div>

        </div>
      </div>
    </nav>


    <!-- ===================== -->
    <!-- DASHBOARD CONTENT -->
    <!-- ===================== -->
    <div class="container py-4">

      <h3 class="fw-bold mb-4">Company Dashboard</h3>

      <!-- LOADING -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary"></div>
      </div>

      <div v-else>

        <!-- COMPANY DETAILS CARD -->
        <div class="card shadow-sm border-0 mb-4">
          <div class="card-body">

            <div class="row">

              <!-- LEFT SIDE DETAILS -->
              <div class="col-md-6">
                <h5 class="fw-bold">{{ company.company_name }}</h5>

                <p class="mb-1 text-muted">
                  <strong>Email:</strong> {{ company.email }}
                </p>

                <p class="mb-1 text-muted">
                  <strong>HR Contact:</strong>
                  {{ company.hr_contact || "Not Provided" }}
                </p>

                <p class="mb-1 text-muted">
                  <strong>Website:</strong>
                  <a v-if="company.website"
                     :href="formattedWebsite"
                     target="_blank"
                     class="text-decoration-none">
                    {{ company.website }}
                  </a>
                  <span v-else>Not Provided</span>
                </p>

                <span class="badge bg-warning"
                      v-if="company.approval_status === 'Pending'">
                  Approval Pending
                </span>

                <span class="badge bg-success"
                      v-else-if="company.approval_status === 'Approved'">
                  Approved
                </span>

                <span class="badge bg-danger"
                      v-else>
                  Rejected
                </span>
              </div>

              <!-- RIGHT SIDE STATS -->
              <div class="col-md-6 text-md-end">
                <h6>Total Drives</h6>
                <h3>{{ company.drives.length }}</h3>
              </div>

            </div>

          </div>
        </div>


        <!-- DRIVES SECTION -->
        <div class="card shadow-sm border-0">
          <div class="card-header bg-dark text-white">
            Created Placement Drives
          </div>

          <div class="card-body">

            <div v-if="company.drives.length === 0"
                 class="text-center text-muted">
              No drives created yet
            </div>

            <div v-else>

              <div class="card mb-3 shadow-sm"
                   v-for="drive in company.drives"
                   :key="drive.drive_id">

                <div class="card-body">

                  <div class="d-flex justify-content-between align-items-center">

                    <div>
                      <h6 class="fw-bold mb-1">
                        {{ drive.job_title }}
                      </h6>

                      <p class="mb-1 text-muted">
                        Deadline:
                        {{ formatDate(drive.application_deadline) }}
                      </p>

                      <span class="badge bg-warning"
                            v-if="drive.status === 'Pending'">
                        Pending
                      </span>

                      <span class="badge bg-success"
                            v-else-if="drive.status === 'Approved'">
                        Approved
                      </span>

                      <span class="badge bg-secondary"
                            v-else>
                        Closed
                      </span>
                    </div>

                    <div class="text-center">
                      <h5 class="fw-bold mb-0">
                        {{ drive.applicants_count }}
                      </h5>
                      <small class="text-muted">
                        Applicants
                      </small>
                    </div>

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
      company: {
        company_name: "",
        email: "",
        hr_contact: "",
        website: "",
        approval_status: "",
        drives: []
      },
      loading: true
    };
  },

  computed: {
    formattedWebsite() {
      if (!this.company.website) return "#";
      if (!this.company.website.startsWith("http")) {
        return "https://" + this.company.website;
      }
      return this.company.website;
    }
  },

  mounted() {
    this.fetchDashboard();
  },

  methods: {

    async fetchDashboard() {
      this.loading = true;

      try {
        const res = await axios.get(`${API}/dashboard`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        });

        this.company = res.data;

      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    formatDate(date) {
      if (!date) return "";
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