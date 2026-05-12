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


    <!-- FORM -->
    <div class="container py-4">

      <h3 class="fw-bold mb-4">Create New Drive</h3>

      <div class="card shadow-sm p-4">

        <div class="mb-3">
          <label class="form-label">Job Title</label>
          <input v-model="form.job_title"
                 class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Job Description</label>
          <textarea v-model="form.job_description"
                    class="form-control"></textarea>
        </div>

        <!-- MULTI SELECT BRANCH -->
        <div class="mb-3">
          <label class="form-label fw-semibold">Eligible Branches</label>

          <div class="row">
            <div class="col-md-4 mb-2"
                 v-for="branch in branches"
                 :key="branch">
              <div class="form-check">
                <input class="form-check-input"
                       type="checkbox"
                       :id="branch"
                       :value="branch"
                       v-model="form.eligible_branches" />
                <label class="form-check-label"
                       :for="branch">
                  {{ branch }}
                </label>
              </div>
            </div>
          </div>

          <div v-if="form.eligible_branches.length"
               class="mt-2">
            <small class="text-muted">
              Selected:
              <span class="badge bg-primary me-1"
                    v-for="b in form.eligible_branches"
                    :key="b">
                {{ b }}
              </span>
            </small>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Minimum CGPA</label>
          <input type="number"
                 step="0.01"
                 v-model="form.min_cgpa"
                 class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Eligible Year</label>
          <input type="number"
                 v-model="form.eligible_year"
                 class="form-control" />
        </div>

        <!-- ✅ FIXED DEADLINE VALIDATION -->
        <div class="mb-3">
          <label class="form-label">Application Deadline</label>
          <input type="date"
                 :min="today"
                 v-model="form.application_deadline"
                 class="form-control" />
        </div>

        <button class="btn btn-primary"
                @click="createDrive">
          Create Drive
        </button>

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
      today: new Date().toISOString().split("T")[0], // ✅ prevents back date
      form: {
        job_title: "",
        job_description: "",
        eligible_branches: [],
        min_cgpa: "",
        eligible_year: "",
        application_deadline: ""
      },
      branches: [
        "Computer Science Engineering (CSE)",
        "Information Technology (IT)",
        "Electronics & Communication Engineering (ECE)",
        "Electrical Engineering (EE)",
        "Mechanical Engineering (ME)",
        "Civil Engineering (CE)",
        "Chemical Engineering",
        "Aerospace Engineering",
        "Biotechnology Engineering",
        "Artificial Intelligence & Data Science",
        "Cyber Security",
        "Robotics Engineering",
        "Instrumentation Engineering",
        "Production Engineering"
      ]
    };
  },

  mounted() {
    this.fetchCompany();
  },

  methods: {

    async fetchCompany() {
      const res = await axios.get(`${API}/dashboard`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      });
      this.companyName = res.data.company_name;
    },

    async createDrive() {

      if (this.form.eligible_branches.length === 0) {
        alert("Please select at least one branch");
        return;
      }

      if (!this.form.application_deadline) {
        alert("Please select a deadline");
        return;
      }

      const selectedDate = new Date(this.form.application_deadline);
      const todayDate = new Date();

      todayDate.setHours(0,0,0,0);

      if (selectedDate < todayDate) {
        alert("Deadline cannot be in the past");
        return;
      }

      await axios.post(`${API}/create-drive`,
        this.form,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        }
      );

      this.$router.push("/company/drives");
    },

    logout() {
      localStorage.clear();
      this.$router.push("/");
    }

  }

};
</script>


<style scoped>
.active-link {
  color: #ffc107 !important;
  font-weight: 600;
}
.card {
  border-radius: 12px;
}
</style>