<template>
  <div>

    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container-fluid">

        <router-link class="navbar-brand fw-bold"
                     to="/company/dashboard">
          Placement Portal
        </router-link>

        <div class="collapse navbar-collapse">

          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link"
                           to="/company/dashboard">
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active-link"
                           to="/company/drives">
                Company Drives
              </router-link>
            </li>
          </ul>

          <div class="d-flex align-items-center">
            <span class="text-white me-3 fw-semibold">
              {{ companyName }}
            </span>
            <button class="btn btn-outline-light btn-sm"
                    @click="logout">
              Logout
            </button>
          </div>

        </div>
      </div>
    </nav>

    <!-- CONTENT -->
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
          No applications received yet
        </div>

        <div v-else>

          <div class="card shadow-sm mb-3"
               v-for="app in applications"
               :key="app.application_id">

            <div class="card-body">
              <div class="row align-items-center">

                <!-- STUDENT INFO -->
                <div class="col-md-4">
                  <h6 class="fw-bold mb-1">{{ app.student_name }}</h6>
                  <p class="mb-1 text-muted">Branch: {{ app.branch }}</p>
                  <p class="mb-1 text-muted">CGPA: {{ app.cgpa }}</p>

                   <div class="mt-2">
    <a v-if="app.resume_link && app.resume_link.trim() !== ''"
       :href="app.resume_link"
       target="_blank"
       class="btn btn-sm btn-outline-secondary">
      View Resume
    </a>

    <span v-else class="text-muted small">
      Resume not available
    </span>
  </div>
                </div>

                <!-- STATUS -->
                <div class="col-md-3 text-md-center">
                  <span class="badge"
                        :class="statusClass(app.status)">
                    {{ app.status }}
                  </span>

                  <div v-if="app.interview_date"
                       class="small text-muted mt-1">
                    Interview: {{ formatDate(app.interview_date) }}
                  </div>
                </div>

                <!-- ACTIONS -->
                <div class="col-md-5 text-md-end">

                  <!-- Applied -->
                  <div v-if="app.status === 'Applied'">
                    <button class="btn btn-success btn-sm me-2"
                            @click="updateStatus(app, 'Shortlisted')">
                      Shortlist
                    </button>

                    <button class="btn btn-danger btn-sm"
                            @click="updateStatus(app, 'Rejected')">
                      Reject
                    </button>
                  </div>

                  <!-- Shortlisted -->
                  <div v-else-if="app.status === 'Shortlisted'">
                    <input type="date"
                           v-model="app.tempInterviewDate"
                           class="form-control form-control-sm d-inline w-auto me-2" />

                    <button class="btn btn-primary btn-sm me-2"
                            @click="scheduleInterview(app)">
                      Schedule Interview
                    </button>

                    <button class="btn btn-danger btn-sm"
                            @click="updateStatus(app, 'Rejected')">
                      Reject
                    </button>
                  </div>

                  <!-- Interview Scheduled -->
                  <div v-else-if="app.status === 'Interview Scheduled'">
                    <button class="btn btn-success btn-sm me-2"
                            @click="updateStatus(app, 'Selected')">
                      Select
                    </button>

                    <button class="btn btn-danger btn-sm"
                            @click="updateStatus(app, 'Rejected')">
                      Reject
                    </button>
                  </div>

                  <!-- Selected -->
                  <div v-else-if="app.status === 'Selected'">
                    <button class="btn btn-danger btn-sm"
                            @click="updateStatus(app, 'Rejected')">
                      Reject Instead
                    </button>
                  </div>

                  <!-- Rejected -->
                  <div v-else-if="app.status === 'Rejected'">
                    <button class="btn btn-warning btn-sm"
                            @click="updateStatus(app, 'Shortlisted')">
                      Reconsider
                    </button>
                  </div>

                </div>

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
const API = "http://localhost:5000/api/company";

export default {

  data() {
    return {
      companyName: "",
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
      this.loading = true;

      try {
        const driveId = this.$route.params.id;

        const res = await axios.get(
          `${API}/drive/${driveId}/applications`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        );

        this.applications = res.data.map(a => ({
          ...a,
          tempInterviewDate: ""
        }));

        const dash = await axios.get(`${API}/dashboard`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        });

        this.companyName = dash.data.company_name;
        this.driveTitle =
          dash.data.drives.find(d => d.drive_id == driveId)?.job_title || "";

      } catch (err) {
        alert("Failed to load applications");
      }

      this.loading = false;
    },

    async updateStatus(app, newStatus) {
      try {
        await axios.put(
          `${API}/application/${app.application_id}/update`,
          { status: newStatus },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        );

        this.fetchApplications();
      } catch (err) {
        alert(err.response?.data?.error || "Status update failed");
      }
    },

    async scheduleInterview(app) {
      if (!app.tempInterviewDate) {
        alert("Please select interview date");
        return;
      }

      try {
        await axios.put(
          `${API}/application/${app.application_id}/update`,
          {
            status: "Interview Scheduled",
            interview_date: app.tempInterviewDate
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        );

        this.fetchApplications();
      } catch (err) {
        alert(err.response?.data?.error || "Interview scheduling failed");
      }
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
      if (!date) return "";
      return new Date(date).toLocaleDateString();
    },

    logout() {
      localStorage.clear();
      this.$router.push("/");
    }

  }

};
</script>