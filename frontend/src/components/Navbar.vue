<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container-fluid">

      <!-- Brand -->
      <router-link class="navbar-brand fw-bold fs-5"
                   to="/admin/dashboard">
        🎓 Placement Portal
      </router-link>

      <!-- Toggle -->
      <button class="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#adminNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="adminNavbar">

        <!-- LEFT MENU -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">

          <li class="nav-item">
            <router-link class="nav-link"
              active-class="active-link"
              to="/admin/dashboard">
              Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link"
              active-class="active-link"
              to="/admin/companies">
              Companies
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link"
              active-class="active-link"
              to="/admin/students">
              Students
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link"
              active-class="active-link"
              to="/admin/drives">
              Drives
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link"
              active-class="active-link"
              to="/admin/applications">
              Applications
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link"
              active-class="active-link"
              to="/admin/reports">
              Reports
            </router-link>
          </li>

        </ul>

        <!-- SEARCH BAR -->
        <form class="d-flex me-3" @submit.prevent="handleSearch">
          <input class="form-control form-control-sm"
                 type="search"
                 v-model="searchQuery"
                 placeholder="Search..." />
          <button class="btn btn-sm btn-primary ms-2">
            Search
          </button>
        </form>

        <!-- RIGHT SIDE -->
        <div class="d-flex align-items-center">

          <span class="badge bg-warning text-dark me-3">
            Admin
          </span>

          <button class="btn btn-outline-light btn-sm"
                  @click="logout">
            Logout
          </button>

        </div>

      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: ""
    };
  },
  methods: {

    handleSearch() {
      if (!this.searchQuery.trim()) return;

      // ✅ Stay on current page and pass search query
      this.$router.push({
        path: this.$route.path,
        query: { search: this.searchQuery }
      });

      this.searchQuery = "";
    },

    logout() {
      localStorage.clear();
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
.nav-link {
  transition: 0.2s ease;
}

.active-link {
  color: #ffc107 !important;
  font-weight: 600;
}

.navbar-brand {
  letter-spacing: 0.5px;
}
</style>