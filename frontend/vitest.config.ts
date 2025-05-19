// frontend/vitest.config.ts
import { defineConfig } from 'vitest/config'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  // 1) Global define for the Svelte plugin
  define: {
    'import.meta.env.SSR': 'false'
  },

  plugins: [
    // 2) No special overrides here—just the stock plugin
    svelte()
  ],

  test: {
    // 3) Browser-like DOM environment
    environment: 'jsdom',
    globals: true,

    // 4) Tell Vitest: whenever you see a .svelte file, transform it for the web (DOM) build
    transformMode: {
      web: [ /\.svelte$/ ]
    },

    // 5) Inline the Svelte runtime and testing-library so they get compiled into that DOM build
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
      all: true,
      // …your thresholds…
    }
  }
})
