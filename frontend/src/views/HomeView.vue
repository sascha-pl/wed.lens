<script setup lang="ts">
import { onMounted, ref } from 'vue'

const apiStatus = ref('Checking API…')

onMounted(async () => {
  try {
    const response = await fetch('/api/health')
    const data: { status: string } = await response.json()
    apiStatus.value = `API status: ${data.status}`
  } catch {
    apiStatus.value = 'API is unavailable.'
  }
})
</script>

<template>
  <main>
    <p class="eyebrow">Private wedding memories</p>
    <h1>WedLens</h1>
    <p>Photo upload, private galleries, and person-based discovery are coming next.</p>
    <p class="status">{{ apiStatus }}</p>
  </main>
</template>
