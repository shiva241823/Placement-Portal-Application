<template>
  <div class="container py-4">
    <h4 class="fw-bold mb-3">Registered Students</h4>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <div v-if="students.length === 0" class="alert alert-info text-center">
        No students available
      </div>

      <div v-else class="table-responsive">
        <table class="table table-hover table-bordered">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in students" :key="s.user_id">
              <td>{{ s.full_name }}</td>
              <td>{{ s.email }}</td>
              <td>{{ s.branch }}</td>
              <td>{{ s.cgpa }}</td>

              <td class="d-flex align-items-center justify-content-between">
                <span
                  class="badge"
                  :class="s.is_blacklisted ? 'bg-danger' : 'bg-success'"
                >
                  {{ s.is_blacklisted ? 'Blacklisted' : 'Active' }}
                </span>

                <div class="dropdown">
                  <button
                    class="btn btn-sm btn-outline-secondary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                  >
                    Actions
                  </button>

                  <ul class="dropdown-menu dropdown-menu-end">
                    <li>
                      <button
                        class="dropdown-item text-danger"
                        @click="toggleBlacklist(s.user_id)"
                      >
                        {{ s.is_blacklisted ? 'Remove Blacklist' : 'Blacklist Student' }}
                      </button>
                    </li>
                  </ul>
                </div>

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
      students: [],
      loading: true
    };
  },

  mounted() {
    this.fetchStudents();
  },

  watch: {
    '$route.query.search': {
      immediate: true,
      handler() {
        this.fetchStudents();
      }
    }
  },

  methods: {

    async fetchStudents() {
      this.loading = true;
      try {
        const res = await axios.get(`${API}/students`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          },
          params: {
            search: this.$route.query.search || ""
          }
        });
        this.students = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async toggleBlacklist(userId) {
      await axios.put(
        `${API}/student/${userId}/toggle-blacklist`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        }
      );
      this.fetchStudents();
    }

  }
};
</script>

<style scoped>
.badge {
  font-size: 0.8rem;
}
</style>