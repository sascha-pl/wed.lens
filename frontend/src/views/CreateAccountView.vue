<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useUserStore } from "../store/user"
import { useModal } from "../services/modal"

const router = useRouter()
const modal = useModal()
const userStore = useUserStore()

const email = ref("")
const name = ref("")
const password = ref("")
const password_repeat = ref("")

async function createAccount() {
    if (password.value != password_repeat.value) {
      modal.show("Passwords do not match")
      return
    }

  const response = await fetch("/api/user/create", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email.value,
      name: name.value,
      password: password.value,
    }),
  })

  const data = await response.json()

  if (!response.ok || !data.authenticated) {
    modal.show("Invalid email or password")
    return
  }

  await userStore.initialize()

  await router.push("/")
}
</script>

<template>
  <main>
    <form v-on:submit.prevent="createAccount()">
      <label>
        Email Address
        <input v-model="email" type="email" autocomplete="email" required>
      </label>
      <br>
      <label>
        Name
        <input v-model="name" type="text" autocomplete="name" required>
      </label>
      <br>
      <label>
        Password
        <input v-model="password" type="password" autocomplete="new-password" required>
      </label>
      <br>
      <label>
        Repeat Password
        <input v-model="password_repeat" type="password" autocomplete="new-password" required>
      </label>
      <br>

      <button type="submit">
        Login
      </button>
    </form>
</main>
</template>
