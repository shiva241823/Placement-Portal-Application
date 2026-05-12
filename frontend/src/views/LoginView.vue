<template>
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="col-11 col-sm-8 col-md-5 col-lg-4">
      <div class="card shadow-lg p-4">
        <h3 class="text-center mb-4 fw-bold text-primary">
          Placement Portal
        </h3>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            v-model="email"
            type="email"
            class="form-control"
            placeholder="Enter your email"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Enter your password"
          />
        </div>

        <button @click="login" class="btn btn-primary w-100 mb-3">
          Login
        </button>

        <div v-if="error" class="alert alert-danger text-center py-2">
          {{ error }}
        </div>

        <hr />

        <div class="text-center small">
          <p class="mb-2">New here?</p>
          <router-link
            to="/register-student"
            class="btn btn-outline-success btn-sm me-2"
          >
            Register as Student
          </router-link>
          <router-link
            to="/register-company"
            class="btn btn-outline-secondary btn-sm"
          >
            Register as Company
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      email: "",
      password: "",
      error: "",
      loading: false
    };
  },

  methods: {
    async login() {
      this.error = "";
      this.loading = true;

      try {
        // Clear old token properly
        localStorage.removeItem("access_token");
        localStorage.removeItem("role");

        const res = await api.post("/auth/login", {
          email: this.email,
          password: this.password,
        });

        // STORE CORRECT KEY
        localStorage.setItem("access_token", res.data.access_token);
        localStorage.setItem("role", res.data.role);

        // Redirect based on role
        if (res.data.role === "admin") {
          this.$router.push("/admin/dashboard");
        } else if (res.data.role === "company") {
          this.$router.push("/company/dashboard");
        } else {
          this.$router.push("/student/dashboard");
        }

      } catch (err) {
        console.error("Login error:", err);

        if (err.response?.data?.error) {
          this.error = err.response.data.error;
        } else {
          this.error = "Login failed. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>