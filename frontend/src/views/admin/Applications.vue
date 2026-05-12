<template>
  <div class="container py-4">
    <h4 class="fw-bold mb-3">All Applications</h4>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <div v-if="applications.length === 0"
           class="alert alert-info text-center">
        No applications available
      </div>

      <div v-else class="card shadow-sm mb-3"
           v-for="a in applications"
           :key="a.application_date">

        <div class="card-body">

          <div class="d-flex justify-content-between">
            <div>
              <h6>{{ a.student_name }}</h6>
              <p class="mb-1">
                {{ a.drive_title }} - {{ a.company }}
              </p>
              <small class="text-muted">
                Applied on: {{ formatDate(a.application_date) }}
              </small>
            </div>

            <div>
              <span class="badge bg-info">
                {{ a.status }}
              </span>
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
      applications: [],
      loading: true
    };
  },

  mounted() {
    this.fetchApplications();
  },

  watch: {
    '$route.query.search': {
      immediate: true,
      handler() {
        this.fetchApplications();
      }
    }
  },

  methods: {

    async fetchApplications() {
      this.loading = true;
      try {
        const res = await axios.get(`${API}/applications`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          },
          params: {
            search: this.$route.query.search || ""
          }
        });
        this.applications = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    formatDate(date) {
      if (!date) return "";
      return new Date(date).toLocaleDateString();
    }

  }
};
</script>