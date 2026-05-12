<template>
  <div class="container py-4">
    <h4 class="fw-bold mb-3">Placement Drives</h4>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <div v-if="drives.length === 0" class="alert alert-info text-center">
        No drives available
      </div>

      <div v-else class="card mb-3 shadow-sm"
           v-for="d in drives"
           :key="d.id">

        <div class="card-body">

          <div class="d-flex justify-content-between">
            <div>
              <h5>{{ d.job_title }}</h5>
              <p class="mb-1 text-muted">
                Company: {{ d.company }}
              </p>
              <p class="mb-1">
                Min CGPA: {{ d.min_cgpa }} |
                Branch: {{ d.eligible_branch }} |
                Year: {{ d.eligible_year }}
              </p>
              <p class="mb-1">
                Status:
                <span class="badge bg-warning" v-if="d.status==='Pending'">
                  Pending
                </span>
                <span class="badge bg-success" v-else-if="d.status==='Approved'">
                  Approved
                </span>
                <span class="badge bg-danger" v-else>
                  Rejected
                </span>
              </p>
            </div>

            <!-- ACTION SECTION -->
            <div>

              <!-- Pending Drives -->
              <div v-if="d.status==='Pending'">
                <button class="btn btn-success btn-sm me-2"
                        @click="approveDrive(d.id)">
                  Approve
                </button>
                <button class="btn btn-danger btn-sm"
                        @click="rejectDrive(d.id)">
                  Reject
                </button>
              </div>

              <!-- Approved Drives -->
              <div v-else-if="d.status==='Approved'">
                <router-link
                  :to="`/admin/drive/${d.id}/applications`"
                  class="btn btn-outline-primary btn-sm">
                  View Applications
                </router-link>
              </div>

              <!-- Rejected Drives -->
              <div v-else>
                <span class="text-muted small">
                  No actions available
                </span>
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
const API = "http://localhost:5000/api/admin";

export default {
  data() {
    return {
      drives: [],
      loading: true
    };
  },

  mounted() {
    this.fetchDrives();
  },

  watch: {
    '$route.query.search': {
      immediate: true,
      handler() {
        this.fetchDrives();
      }
    }
  },

  methods: {

    async fetchDrives() {
      this.loading = true;
      try {
        const res = await axios.get(`${API}/drives`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          },
          params: {
            search: this.$route.query.search || ""
          }
        });
        this.drives = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async approveDrive(id) {
      await axios.put(`${API}/drive/${id}/approve`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      });
      this.fetchDrives();
    },

    async rejectDrive(id) {
      await axios.put(`${API}/drive/${id}/reject`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      });
      this.fetchDrives();
    }

  }
};
</script>