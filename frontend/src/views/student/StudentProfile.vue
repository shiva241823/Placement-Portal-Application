<template>
  <div>

    <h4 class="fw-bold mb-3">Profile Settings</h4>

    <div class="card shadow-sm p-4">

      <!-- EMAIL (NON EDITABLE) -->
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input :value="email"
               class="form-control"
               disabled />
      </div>

      <!-- FULL NAME -->
      <div class="mb-3">
        <label class="form-label">Full Name</label>
        <input v-model="form.full_name" class="form-control" />
      </div>

      <!-- BRANCH -->
      <div class="mb-3">
        <label class="form-label">Branch</label>
        <input v-model="form.branch" class="form-control" />
      </div>

      <!-- CGPA -->
      <div class="mb-3">
        <label class="form-label">CGPA</label>
        <input type="number"
               step="0.01"
               v-model="form.cgpa"
               class="form-control" />
      </div>

      <!-- GRAD YEAR -->
      <div class="mb-3">
        <label class="form-label">Graduation Year</label>
        <input type="number"
               v-model="form.graduation_year"
               class="form-control" />
      </div>

      <!-- RESUME LINK -->
      <div class="mb-3">
        <label class="form-label">Resume Link</label>
        <input type="url"
               v-model="form.resume_link"
               placeholder="https://drive.google.com/..."
               class="form-control" />
      </div>

      <button class="btn btn-primary"
              @click="updateProfile">
        Update Profile
      </button>

      <hr class="my-4">

      <!-- PASSWORD RESET SECTION -->
      <h5 class="fw-bold mb-3">Change Password</h5>

      <div class="mb-3">
        <label class="form-label">Current Password</label>
        <input type="password"
               v-model="passwordForm.current_password"
               class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">New Password</label>
        <input type="password"
               v-model="passwordForm.new_password"
               class="form-control" />
      </div>

      <button class="btn btn-warning"
              @click="changePassword">
        Change Password
      </button>

    </div>

  </div>
</template>

<script>
import axios from "axios"
const API = "http://localhost:5000/api/student"

export default {

  data() {
    return {
      email: "",
      form: {
        full_name: "",
        branch: "",
        cgpa: "",
        graduation_year: "",
        resume_link: ""
      },
      passwordForm: {
        current_password: "",
        new_password: ""
      }
    }
  },

  mounted() {
    this.fetchProfile()
  },

  methods: {

    async fetchProfile() {
      try {
        const res = await axios.get(`${API}/me`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })

        this.email = res.data.email
        this.form.full_name = res.data.full_name || ""
        this.form.branch = res.data.branch || ""
        this.form.cgpa = res.data.cgpa || ""
        this.form.graduation_year = res.data.graduation_year || ""
        this.form.resume_link = res.data.resume_link || ""

      } catch (err) {
        console.error(err)
      }
    },

    async updateProfile() {
      try {

        await axios.put(
          `${API}/update-profile`,
          this.form,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        )

        alert("Profile updated successfully")

      } catch (err) {
        alert("Update failed")
      }
    },

    async changePassword() {
      try {

        await axios.put(
          `${API}/change-password`,
          this.passwordForm,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        )

        alert("Password updated successfully")

        this.passwordForm.current_password = ""
        this.passwordForm.new_password = ""

      } catch (err) {
        alert(err.response?.data?.error || "Password change failed")
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