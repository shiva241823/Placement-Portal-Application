<template>
  <div>

    <h4 class="fw-bold mb-3">Approved Companies</h4>

    <!-- LOADING -->
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <!-- ERROR -->
    <div v-else-if="error" class="alert alert-danger text-center">
      {{ error }}
    </div>

    <!-- CONTENT -->
    <div v-else>

      <div v-if="companies.length === 0"
           class="alert alert-info text-center">
        No approved companies available
      </div>

      <div v-else
           class="card mb-3 shadow-sm"
           v-for="c in companies"
           :key="c.company_id">

        <div class="card-body d-flex justify-content-between align-items-center">

          <div>
            <h5 class="mb-1">{{ c.company_name }}</h5>

            <div class="small text-muted">
              Email: {{ c.email }}
            </div>

            <div class="small">
              Website:
              <a :href="formatWebsite(c.website)"
                 target="_blank"
                 class="text-decoration-none">
                {{ c.website || 'Not Provided' }}
              </a>
            </div>

            <div class="small text-muted">
              HR Contact: {{ c.hr_contact || 'Not Provided' }}
            </div>
          </div>

          <div>
            <button
              class="btn btn-primary btn-sm"
              @click="viewDrives(c.company_id)"
            >
              View Drives
            </button>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios"
const API = "http://localhost:5000/api/student"

export default {

  data() {
    return {
      companies: [],
      loading: true,
      error: null
    }
  },

  mounted() {
    this.fetchCompanies()
  },

  methods: {

    async fetchCompanies() {
      this.loading = true
      this.error = null

      try {
        const res = await axios.get(`${API}/companies`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })

        this.companies = res.data

      } catch (err) {
        console.error(err)

        if (err.response) {
          this.error = err.response.data.error || "Failed to load companies"
        } else {
          this.error = "Server not reachable"
        }

      } finally {
        this.loading = false
      }
    },

    viewDrives(companyId) {
      this.$router.push(`/student/company/${companyId}/drives`)
    },

    formatWebsite(url) {
      if (!url) return "#"
      if (!url.startsWith("http")) {
        return "https://" + url
      }
      return url
    }

  }

}
</script>

<style scoped>
.card {
  border-radius: 12px;
}
</style>