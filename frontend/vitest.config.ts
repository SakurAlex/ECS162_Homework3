import { defineConfig } from 'vitest/config'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig(({ mode }) => ({
  define: {
    'import.meta.env.SSR': 'false'
  },
  resolve: {
    // Use browser resolution during tests so Svelte’s mount() is available
    conditions: mode === 'test' ? ['browser'] : []
  },
  plugins: [
    svelte()
  ],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['src/setupTests.ts'],
    transformMode: {
      web: [/\.svelte$/]
    },
    server: {
      deps: {
        inline: [
          '@testing-library/svelte',
          'svelte',
          'svelte/internal'
        ]
      }
    },
    coverage: {
      provider: 'v8',
      all: true
    }
  }
}))
