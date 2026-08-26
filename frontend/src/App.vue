<script setup lang="ts">
import { onMounted } from "vue"
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from "./store/user"
import { useAuth } from "./services/auth"
import { useModal } from "./services/modal"

const userStore = useUserStore()
const auth = useAuth()
const modal = useModal()

onMounted(async () => {
  await userStore.initialize()
})

async function logout() {
	await auth.logout()
}
</script>

<template>
  <header class="site-header">
    <RouterLink class="brand" to="/">WedLens</RouterLink>
	<nav aria-label="Main navigation">
	  <RouterLink to="/">Home</RouterLink>
	  <RouterLink v-if="userStore.authenticated" to="/profile">Profile</RouterLink>
	  <button type="button" v-if="userStore.authenticated" @click="logout">Logout</button>
	  <RouterLink v-if="!userStore.authenticated" to="/about">About</RouterLink>
	  <RouterLink v-if="!userStore.authenticated" to="/login">Login</RouterLink>
	</nav>
  </header>

  <div v-if="!userStore.initialized">
    Loading...
  </div>

  <RouterView v-else />
  
  <div
    v-if="modal.isOpen.value"
    class="modal-backdrop"
    @click.self="modal.close"
  >
    <div class="modal">
      <p>{{ modal.message.value }}</p>

      <button @click="modal.close">
        OK
      </button>
    </div>
  </div>
</template>
