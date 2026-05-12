<template>
  <div class="container py-4">
    <h4 class="fw-bold mb-3">Registered Companies</h4>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <div v-if="companies.length === 0" class="alert alert-info text-center">
        No companies available
      </div>

      <div
        class="card mb-3 shadow-sm"
        v-for="c in companies"
        :key="c.id"
      >
        <div class="card-body d-flex justify-content-between align-items-center">

          <div>
            <h6 class="mb-1">{{ c.company_name }}</h6>

            <div class="small text-muted">
              HR: {{ c.hr_contact }}
            </div>

            <div class="small">
              Website:
              <a
                :href="formatWebsite(c.website)"
                target="_blank"
                class="text-decoration-none"
              >
                {{ c.website }}
              </a>
            </div>

            <div class="mt-1">
              Status:
              <span class="badge bg-warning" v-if="c.approval_status === 'Pending'">
                Pending
              </span>
              <span class="badge bg-success" v-else-if="c.approval_status === 'Approved'">
                Approved
              </span>
              <span class="badge bg-danger" v-else>
                Rejected
              </span>

              <span
                class="badge bg-dark ms-2"
                v-if="c.is_blacklisted"
              >
                Blacklisted
              </span>
            </div>
          </div>

          <!-- DROPDOWN -->
          <div class="dropdown">
            <button
              class="btn btn-outline-primary btn-sm dropdown-toggle"
              type="button"
              data-bs-toggle="dropdown"
            >
              Actions
            </button>

            <ul class="dropdown-menu dropdown-menu-end">

              <li v-if="c.approval_status !== 'Approved'">
                <button
                  class="dropdown-item text-success"
                  @click="approve(c.id)"
                >
                  Approve
                </button>
              </li>

              <li v-if="c.approval_status !== 'Rejected'">
                <button
                  class="dropdown-item text-danger"
                  @click="reject(c.id)"
                >
                  Reject
                </button>
              </li>

              <li v-if="c.approval_status === 'Approved'">
                <button
                  class="dropdown-item text-danger"
                  @click="toggleBlacklist(c.user_id)"
                >
                  {{ c.is_blacklisted ? 'Remove Blacklist' : 'Blacklist Company' }}
                </button>
              </li>

            </ul>
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
      companies: [],
      loading: true
    };
  },

  mounted() {
    this.fetchCompanies();
  },

  watch: {
    '$route.query.search': {
      immediate: true,
      handler() {
        this.fetchCompanies();
      }
    }
  },

  methods: {

    formatWebsite(url) {
      if (!url) return "#";
      if (!url.startsWith("http")) {
        return "https://" + url;
      }
      return url;
    },

    async fetchCompanies() {
      this.loading = true;
      try {
        const res = await axios.get(`${API}/companies`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          },
          params: {
            search: this.$route.query.search || ""
          }
        });
        this.companies = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async approve(id) {
      await axios.put(
        `${API}/company/${id}/approve`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        }
      );
      this.fetchCompanies();
    },

    async reject(id) {
      await axios.put(
        `${API}/company/${id}/reject`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        }
      );
      this.fetchCompanies();
    },

    async toggleBlacklist(userId) {
      await axios.put(
        `${API}/company/${userId}/toggle-blacklist`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        }
      );
      this.fetchCompanies();
    }

  }
};
</script>