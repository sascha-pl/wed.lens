<script setup lang="ts">
import { computed } from "vue"
import { useUserStore } from "../store/user"

import HomeLoggedOutView from "./HomeLoggedOutView.vue"
import HomeLoggedInView from "./HomeLoggedInView.vue"

const userStore = useUserStore()

const currentView = computed(() => {
  return userStore.authenticated
    ? HomeLoggedInView
    : HomeLoggedOutView
})
</script>

<template>
  <component :is="currentView" />
</template>