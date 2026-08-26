<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useUserStore } from "../store/user"
import { useModal } from "../services/modal"
import { useAuth } from "../services/auth"

const router = useRouter()
const modal = useModal()
const auth = useAuth()
const userStore = useUserStore()

const email = ref("")
const password = ref("")

async function login() {
	await auth.login(email.value, password.value)
}
</script>

<template>
  <main>
    <form v-on:submit.prevent="login()">
      <label>
        Email Address
        <input v-model="email" type="email" autocomplete="email" required>
      </label>
      <br>
      <label>
        Password
        <input v-model="password" type="password" autocomplete="current-password" required>
      </label>
      <br>

      <RouterLink to="/create-account">Create Account</RouterLink>
      <button type="submit">
        Login
      </button>
    </form>
  </main>
</template>
