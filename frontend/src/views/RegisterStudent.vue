<template>
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="col-11 col-sm-9 col-md-6 col-lg-5">
      <div class="card shadow-lg p-4">
        <h4 class="text-center mb-4 fw-bold text-success">
          Student Registration
        </h4>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="full_name" type="text" class="form-control" />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" />
          </div>

          <!-- UPDATED BRANCH SELECT -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Branch</label>
            <select v-model="branch" class="form-select">
              <option disabled value="">Select Branch</option>
              <option v-for="b in branches" :key="b" :value="b">
                {{ b }}
              </option>
            </select>
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">CGPA</label>
            <input v-model="cgpa" type="number" step="0.01" class="form-control" />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Graduation Year</label>
            <input v-model="graduation_year" type="number" class="form-control" />
          </div>
        </div>

        <button @click="register" class="btn btn-success w-100 mb-3">
          Register
        </button>

        <div v-if="message" class="alert alert-success text-center py-2">
          {{ message }}
        </div>

        <div v-if="error" class="alert alert-danger text-center py-2">
          {{ error }}
        </div>

        <div class="text-center small">
          Already have an account?
          <router-link to="/" class="text-decoration-none">
            Login here
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
      full_name: "",
      email: "",
      password: "",
      branch: "",
      cgpa: "",
      graduation_year: "",
      message: "",
      error: "",

      // UNIFORM ENGINEERING BRANCH LIST
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
  methods: {
    async register() {
      this.message = "";
      this.error = "";

      try {
        await api.post("/auth/register/student", {
          full_name: this.full_name,
          email: this.email,
          password: this.password,
          branch: this.branch,
          cgpa: this.cgpa,
          graduation_year: this.graduation_year,
        });

        this.message = "Registration successful! You can now login.";

        // Optional reset
        this.full_name = "";
        this.email = "";
        this.password = "";
        this.branch = "";
        this.cgpa = "";
        this.graduation_year = "";

      } catch (err) {
        this.error = err.response?.data?.error || "Registration failed.";
      }
    },
  },
};
</script>