<template>
  <div class="container py-4">

    <h3 class="fw-bold mb-4">Admin Dashboard</h3>

    <!-- LOADING -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <!-- STATS CARDS -->
      <div class="row g-4 mb-4">

        <div class="col-md-4">
          <div class="card shadow-sm border-0 stat-card bg-primary text-white">
            <div class="card-body">
              <h6>Total Students</h6>
              <h2>{{ stats.total_students }}</h2>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm border-0 stat-card bg-success text-white">
            <div class="card-body">
              <h6>Total Companies</h6>
              <h2>{{ stats.total_companies }}</h2>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm border-0 stat-card bg-warning text-dark">
            <div class="card-body">
              <h6>Total Drives</h6>
              <h2>{{ stats.total_drives }}</h2>
            </div>
          </div>
        </div>

      </div>

      <!-- PENDING APPROVAL SECTION -->
      <div class="row g-4">

        <!-- Pending Companies -->
        <div class="col-md-6">
          <div class="card shadow-sm border-0">
            <div class="card-header bg-dark text-white">
              Pending Company Approvals ({{ pendingCompanies.length }})
            </div>
            <div class="card-body">

              <div v-if="pendingCompanies.length === 0"
                   class="text-center text-muted">
                No pending companies
              </div>

              <ul v-else class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between align-items-center"
                    v-for="company in pendingCompanies"
                    :key="company.id">
                  {{ company.company_name }}

                  <div>
                    <button class="btn btn-sm btn-success me-2"
                            @click="approveCompany(company.id)">
                      Approve
                    </button>

                    <button class="btn btn-sm btn-danger"
                            @click="rejectCompany(company.id)">
                      Reject
                    </button>
                  </div>
                </li>
              </ul>

            </div>
          </div>
        </div>

        <!-- Pending Drives -->
        <div class="col-md-6">
          <div class="card shadow-sm border-0">
            <div class="card-header bg-dark text-white">
              Pending Drive Approvals ({{ pendingDrives.length }})
            </div>
            <div class="card-body">

              <div v-if="pendingDrives.length === 0"
                   class="text-center text-muted">
                No pending drives
              </div>

              <ul v-else class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between align-items-center"
                    v-for="drive in pendingDrives"
                    :key="drive.id">
                  {{ drive.job_title }}

                  <div>
                    <button class="btn btn-sm btn-success me-2"
                            @click="approveDrive(drive.id)">
                      Approve
                    </button>

                    <button class="btn btn-sm btn-danger"
                            @click="rejectDrive(drive.id)">
                      Reject
                    </button>
                  </div>
                </li>
              </ul>

            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

const API = "http://localhost:5000/api/admin";

export default {
  data() {
    return {
      stats: {
        total_students: 0,
        total_companies: 0,
        total_drives: 0
      },
      pendingCompanies: [],
      pendingDrives: [],
      loading: true
    };
  },

  mounted() {
    this.loadDashboard();
  },

  watch: {
    '$route.query.search': {
      immediate: false,
      handler(newVal) {
        if (newVal) {
          this.handleGlobalSearch(newVal);
        }
      }
    }
  },

  methods: {

    getAuthHeader() {
      return {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      };
    },

    async handleGlobalSearch(searchTerm) {
      try {
        const res = await axios.get(`${API}/global-search`, {
          headers: this.getAuthHeader(),
          params: { search: searchTerm }
        });

        const { students, companies, drives } = res.data;

        if (students.length > 0) {
          this.$router.push({ path: "/admin/students", query: { search: searchTerm } });
        } else if (companies.length > 0) {
          this.$router.push({ path: "/admin/companies", query: { search: searchTerm } });
        } else if (drives.length > 0) {
          this.$router.push({ path: "/admin/drives", query: { search: searchTerm } });
        } else {
          alert("No results found");
        }

      } catch (err) {
        console.error(err);
      }
    },

    async loadDashboard() {
      this.loading = true;

      try {
        const [statsRes, companiesRes, drivesRes] = await Promise.all([
          axios.get(`${API}/dashboard`, { headers: this.getAuthHeader() }),
          axios.get(`${API}/companies`, { headers: this.getAuthHeader() }),
          axios.get(`${API}/drives`, { headers: this.getAuthHeader() })
        ]);

        this.stats = statsRes.data || {};

        this.pendingCompanies = (companiesRes.data || []).filter(
          c => c.approval_status === "Pending"
        );

        this.pendingDrives = (drivesRes.data || []).filter(
          d => d.status === "Pending"
        );

      } catch (error) {
        console.error("Dashboard Load Error:", error);
      } finally {
        this.loading = false;
      }
    },

    async approveCompany(id) {
      await axios.put(`${API}/company/${id}/approve`, {}, { headers: this.getAuthHeader() });
      this.loadDashboard();
    },

    async rejectCompany(id) {
      await axios.put(`${API}/company/${id}/reject`, {}, { headers: this.getAuthHeader() });
      this.loadDashboard();
    },

    async approveDrive(id) {
      await axios.put(`${API}/drive/${id}/approve`, {}, { headers: this.getAuthHeader() });
      this.loadDashboard();
    },

    async rejectDrive(id) {
      await axios.put(`${API}/drive/${id}/reject`, {}, { headers: this.getAuthHeader() });
      this.loadDashboard();
    }

  }
};
</script>

<style scoped>
.stat-card {
  border-radius: 12px;
  transition: 0.3s;
}
.stat-card:hover {
  transform: translateY(-6px);
}
</style>