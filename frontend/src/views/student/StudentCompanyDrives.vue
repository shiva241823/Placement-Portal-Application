<template>
  <div>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h4 class="fw-bold">Company Drives</h4>

      <button class="btn btn-outline-dark btn-sm"
              @click="$router.push('/student/companies')">
        ← Back to Companies
      </button>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <!-- CONTENT -->
    <div v-else>

      <div v-if="drives.length === 0"
           class="alert alert-info text-center">
        No approved drives available for this company
      </div>

      <div v-else
           class="card mb-3 shadow-sm"
           v-for="d in drives"
           :key="d.drive_id">

        <div class="card-body">

          <div class="d-flex justify-content-between">

            <div>

              <h5 class="mb-1">{{ d.job_title }}</h5>

              <p class="text-muted small mb-1">
                {{ d.description }}
              </p>

              <p class="mb-1">
                Min CGPA: {{ d.min_cgpa }} |
                Branch: {{ d.eligible_branch }} |
                Year: {{ d.eligible_year }}
              </p>

              <p class="mb-2">
                Deadline: {{ formatDate(d.deadline) }}
              </p>

              <span class="badge"
                    :class="d.is_eligible ? 'bg-success' : 'bg-danger'">
                {{ d.is_eligible ? 'Eligible' : 'Not Eligible' }}
              </span>

              <span v-if="d.already_applied"
                    class="badge bg-secondary ms-2">
                Already Applied
              </span>

            </div>

            <div class="text-end">

              <button class="btn btn-primary btn-sm"
                      :disabled="!d.is_eligible || d.already_applied"
                      @click="apply(d.drive_id)">
                Apply
              </button>

            </div>

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
      drives: [],
      loading: true
    }
  },

  mounted() {
    this.fetchDrives()
  },

  methods: {

    async fetchDrives() {
      try {
        const res = await axios.get(
          `${API}/company/${this.$route.params.id}/drives`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        )

        this.drives = res.data
      } catch (err) {
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async apply(id) {
      try {
        await axios.post(`${API}/apply/${id}`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })

        alert("Applied successfully")
        this.fetchDrives()

      } catch (err) {
        alert(err.response?.data?.error || "Application failed")
      }
    },

    formatDate(date) {
      if (!date) return ""
      return new Date(date).toLocaleDateString()
    }

  }

}
</script>