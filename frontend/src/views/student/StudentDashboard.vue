<template>
  <div>

    <h4 class="fw-bold mb-3">Approved Placement Drives</h4>

    <!-- SEARCH -->
    <div class="row mb-3">
      <div class="col-md-6">
        <input
          v-model="search"
          class="form-control"
          placeholder="Search by company or job title..."
          @input="fetchDrives"
        />
      </div>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <!-- TABLE -->
    <div v-else>

      <div v-if="drives.length === 0"
           class="alert alert-info text-center">
        No data available
      </div>

      <div v-else class="table-responsive">
        <table class="table table-hover table-bordered align-middle">

          <thead class="table-dark">
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Eligibility</th>
              <th>Deadline</th>
              <th>Status</th>
              <th style="width: 160px;">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="d in drives" :key="d.drive_id">

              <td>{{ d.company }}</td>

              <td>
                <strong>{{ d.job_title }}</strong>
                <div class="small text-muted">
                  {{ d.description }}
                </div>
              </td>

              <td>
                CGPA ≥ {{ d.min_cgpa }} <br>
                Branch: {{ d.eligible_branch }} <br>
                Year: {{ d.eligible_year }}
              </td>

              <td>{{ formatDate(d.deadline) }}</td>

              <td>
                <span
                  class="badge"
                  :class="d.is_eligible ? 'bg-success' : 'bg-danger'"
                >
                  {{ d.is_eligible ? 'Eligible' : 'Not Eligible' }}
                </span>

                <span
                  v-if="d.already_applied"
                  class="badge bg-secondary ms-1"
                >
                  Applied
                </span>
              </td>

              <td>

                <button
                  class="btn btn-sm btn-primary me-2"
                  :disabled="!d.is_eligible || d.already_applied"
                  @click="apply(d.drive_id)"
                >
                  Apply
                </button>

                <!-- <button
                  class="btn btn-sm btn-outline-dark"
                  @click="viewCompany(d.company)"
                >
                  View Company
                </button> -->

              </td>

            </tr>
          </tbody>

        </table>
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
      loading: true,
      search: ""
    }
  },

  mounted() {
    this.fetchDrives()
  },

  methods: {

    async fetchDrives() {
      this.loading = true
      try {
        const res = await axios.get(`${API}/dashboard`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          },
          params: {
            search: this.search
          }
        })

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

    viewCompany(companyName) {
      this.$router.push("/student/companies")
    },

    formatDate(date) {
      if (!date) return ""
      return new Date(date).toLocaleDateString()
    }

  }

}
</script>