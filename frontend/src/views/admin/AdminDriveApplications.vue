<template>
  <div class="container py-4">

    <h3 class="fw-bold mb-4">
      Applications for {{ driveTitle }}
    </h3>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <div v-if="applications.length === 0"
           class="alert alert-info text-center">
        No students applied for this drive
      </div>

      <div v-else class="table-responsive">

        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Status</th>
              <th>Applied On</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="a in applications"
                :key="a.application_id">

              <td>{{ a.student_name }}</td>
              <td>{{ a.email }}</td>
              <td>{{ a.branch }}</td>
              <td>{{ a.cgpa }}</td>

              <td>
                <span class="badge"
                      :class="statusClass(a.status)">
                  {{ a.status }}
                </span>
              </td>

              <td>
                {{ formatDate(a.application_date) }}
              </td>

            </tr>
          </tbody>
        </table>

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
      driveTitle: "",
      applications: [],
      loading: true
    };
  },

  mounted() {
    this.fetchApplications();
  },

  methods: {

    async fetchApplications() {

      const driveId = this.$route.params.id;

      const res = await axios.get(
        `${API}/drive/${driveId}/applications`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        }
      );

      this.driveTitle = res.data.drive_title;
      this.applications = res.data.applications;
      this.loading = false;
    },

    statusClass(status) {
      switch (status) {
        case "Applied": return "bg-secondary";
        case "Shortlisted": return "bg-warning";
        case "Interview Scheduled": return "bg-primary";
        case "Selected": return "bg-success";
        case "Rejected": return "bg-danger";
        default: return "bg-secondary";
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }

  }

};
</script>

<style scoped>
.badge {
  font-size: 0.75rem;
}
</style>