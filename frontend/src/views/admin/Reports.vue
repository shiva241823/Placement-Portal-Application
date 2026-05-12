<template>
  <div class="container py-4">
    <h4 class="fw-bold mb-4">Placement Reports</h4>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <!-- Overview -->
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm text-center">
            <div class="card-body">
              <h6>Total Drives</h6>
              <h3>{{ overview.total_drives }}</h3>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm text-center">
            <div class="card-body">
              <h6>Total Students</h6>
              <h3>{{ overview.total_students }}</h3>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm text-center">
            <div class="card-body">
              <h6>Total Selected</h6>
              <h3>{{ overview.total_selected_students }}</h3>
            </div>
          </div>
        </div>
      </div>

      <!-- Drive Selection -->
      <div class="mb-3">
        <select class="form-select"
                v-model="selectedDrive"
                @change="fetchDriveReport">
          <option disabled value="">Select Approved Drive</option>

          <option v-for="d in drives"
                  :key="d.id"
                  :value="d.id">
            {{ d.job_title }}
          </option>
        </select>
      </div>

      <!-- Drive Report -->
      <div v-if="driveReport" class="card shadow-sm">
        <div class="card-body">
          <h5>{{ driveReport.drive_name }}</h5>
          <p><strong>Eligible:</strong> {{ driveReport.eligible_students }}</p>
          <p><strong>Applied:</strong> {{ driveReport.applied }}</p>
          <p><strong>Selected:</strong> {{ driveReport.selected }}</p>
          <p><strong>Rejected:</strong> {{ driveReport.rejected }}</p>
        </div>
      </div>

      <!-- No Approved Drives -->
      <div v-if="!loading && drives.length === 0"
           class="alert alert-info text-center mt-3">
        No approved drives available for reports
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
      overview: {
        total_drives: 0,
        total_students: 0,
        total_selected_students: 0
      },
      drives: [],
      driveReport: null,
      selectedDrive: "",
      loading: true
    };
  },

  mounted() {
    this.initializeReports();
  },

  methods: {

    getAuthHeader() {
      return {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      };
    },

    async initializeReports() {
      this.loading = true;
      try {
        await this.fetchOverview();
        await this.fetchDrives();
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async fetchOverview() {
      const res = await axios.get(`${API}/reports/overview`, {
        headers: this.getAuthHeader()
      });
      this.overview = res.data;
    },

    async fetchDrives() {
      const res = await axios.get(`${API}/reports/drives`, {
        headers: this.getAuthHeader()
      });

      // ✅ Extra safety: only approved drives
      this.drives = res.data || [];
    },

    async fetchDriveReport() {
      if (!this.selectedDrive) return;

      const res = await axios.get(
        `${API}/reports/drive/${this.selectedDrive}`,
        { headers: this.getAuthHeader() }
      );

      this.driveReport = res.data;
    }

  }
};
</script>