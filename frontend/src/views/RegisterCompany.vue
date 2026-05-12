<template>
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="col-11 col-sm-9 col-md-6 col-lg-5">
      <div class="card shadow-lg p-4">
        <h4 class="text-center mb-4 fw-bold text-secondary">
          Company Registration
        </h4>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Company Name</label>
            <input v-model="company_name" type="text" class="form-control" />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">HR Contact</label>
            <input v-model="hr_contact" type="text" class="form-control" />
          </div>

          <div class="col-md-12 mb-3">
            <label class="form-label">Website</label>
            <input v-model="website" type="text" class="form-control" />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" />
          </div>
        </div>

        <button @click="register" class="btn btn-secondary w-100 mb-3">
          Register
        </button>

        <div v-if="message" class="alert alert-success text-center py-2">
          {{ message }}
        </div>

        <div v-if="error" class="alert alert-danger text-center py-2">
          {{ error }}
        </div>

        <div class="text-center small">
          Already registered?
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
      company_name: "",
      hr_contact: "",
      website: "",
      email: "",
      password: "",
      message: "",
      error: "",
    };
  },
  methods: {
    async register() {
      this.message = "";
      this.error = "";

      try {
        await api.post("/auth/register/company", {
          company_name: this.company_name,
          hr_contact: this.hr_contact,
          website: this.website,
          email: this.email,
          password: this.password,
        });

        this.message =
          "Company registered! Await admin approval before login.";
      } catch (err) {
        this.error = "Registration failed.";
      }
    },
  },
};
</script>