import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

const projectRoot = fileURLToPath(new URL('..', import.meta.url))

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, projectRoot, 'VITE_')

  return {
    envDir: projectRoot,
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: env.VITE_API_PROXY_TARGET
      ? {
          proxy: {
            '/api': env.VITE_API_PROXY_TARGET,
          },
        }
      : undefined,
  }
})
