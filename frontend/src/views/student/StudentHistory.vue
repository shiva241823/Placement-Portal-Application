<template>
  <div>

    <h4 class="fw-bold mb-3">Application History</h4>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <div v-if="applications.length === 0"
           class="alert alert-info text-center">
        You have not applied to any drives yet
      </div>

      <div v-else class="table-responsive">

        <table class="table table-bordered table-hover align-middle">

          <thead class="table-dark">
            <tr>
              <th>Company</th>
              <th>Drive</th>
              <th>Status</th>
              <th>Applied On</th>
              <th>Interview Date</th>
            </tr>
          </thead>

          <tbody>

            <tr v-for="a in applications" :key="a.drive_title">

              <td>{{ a.company }}</td>
              <td>{{ a.job_title }}</td>

              <td>
                <span class="badge"
                      :class="statusClass(a.status)">
                  {{ a.status }}
                </span>
              </td>

              <td>{{ formatDate(a.applied_on) }}</td>
              <td>{{ formatDate(a.interview_date) }}</td>

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
      applications: [],
      loading: true
    }
  },

  mounted() {
    this.fetchHistory()
  },

  methods: {

    async fetchHistory() {
      try {
        const res = await axios.get(`${API}/applications`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })
        this.applications = res.data
      } catch (err) {
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    statusClass(status) {
      if (status === "Selected") return "bg-success"
      if (status === "Rejected") return "bg-danger"
      if (status === "Shortlisted") return "bg-warning text-dark"
      return "bg-secondary"
    },

    formatDate(date) {
      if (!date) return "-"
      return new Date(date).toLocaleDateString()
    }

  }

}
</script>