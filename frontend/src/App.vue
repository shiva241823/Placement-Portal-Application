<template>
  <div>
    <!-- Show Navbar ONLY for admin routes -->
    <Navbar v-if="isAdminRoute" />

    <!-- Main Page Content -->
    <router-view />
  </div>
</template>

<script>
import { computed } from "vue"
import { useRoute } from "vue-router"
import Navbar from "./components/Navbar.vue"

export default {
  name: "App",
  components: { Navbar },

  setup() {
    const route = useRoute()

    const isAdminRoute = computed(() => {
      return route.path.startsWith("/admin")
    })

    return { isAdminRoute }
  }
}
</script>