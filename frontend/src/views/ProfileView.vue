<script setup lang="ts">
import { useUserStore } from "../store/user"

const userStore = useUserStore()
</script>
<template>
  <main>
    <h1>Profile</h1>
    <p>User Name: {{userStore.user?.name ?? '-'}}</p>
    <p>Email Address: {{userStore.user?.email ?? '-'}}</p>
  </main>
</template>
