<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

onMounted(() => {
  if (auth.isAuthenticated && !auth.user) {
    auth.fetchUser()
  }
})
</script>