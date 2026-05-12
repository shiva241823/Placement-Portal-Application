<template>
  <div>

    <h4 class="fw-bold mb-3">Download Placement Report</h4>

    <div class="card shadow-sm p-4 text-center">

      <p class="mb-3">
        Your complete placement application history will be generated
        and sent to your registered email address.
      </p>

      <button class="btn btn-primary"
              :disabled="loading"
              @click="generateReport">

        <span v-if="loading"
              class="spinner-border spinner-border-sm me-2">
        </span>

        {{ loading ? "Generating..." : "Generate & Email Report" }}

      </button>

      <!-- Success Message -->
      <div v-if="successMessage"
           class="alert alert-success mt-3">
        {{ successMessage }}
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage"
           class="alert alert-danger mt-3">
        {{ errorMessage }}
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
      loading: false,
      successMessage: "",
      errorMessage: ""
    }
  },

  methods: {

    async generateReport() {

      this.loading = true
      this.successMessage = ""
      this.errorMessage = ""

      try {

        const response = await axios.get(
          `${API}/export-history`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        )

        this.successMessage = response.data.message

      } catch (err) {

        if (err.response && err.response.data.message) {
          this.errorMessage = err.response.data.message
        } else {
          this.errorMessage = "Failed to generate report. Please try again."
        }

      } finally {
        this.loading = false
      }

    }

  }

}
</script>

<style scoped>
.card {
  border-radius: 12px;
}
</style>