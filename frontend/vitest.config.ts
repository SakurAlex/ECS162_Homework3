import { defineConfig } from 'vitest/config';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [
    svelte({
        compilerOptions: {
        // force DOM-mode (not SSR) so onMount / mount() works
        generate: 'dom',
        hydratable: true,
        },
    }),
  ],
  test: {
    environment: 'jsdom',
    globals: true,
    
    // Force Svelte to treat us as browser (not SSR) during tests:
    define: {
      'import.meta.env.SSR': 'false'
    },

    // Make sure .svelte files are transformed for the web
    transformMode: {
      web: [/\.[jt]sx?$/, /\.svelte$/]
    },

    // Inline Svelte dependencies so they go through the plugin
    server: {
      deps: {
        inline: [
          '@testing-library/svelte',
          'svelte',
          'svelte/internal',
        ],
      },
    },


    
    coverage: {
      provider: 'istanbul',
      reporter: ['text', 'html'],
      include: ['src/**/*.{ts,svelte}'],
      exclude: ['src/main.ts', 'src/vite-env.d.ts'],
      statements: 98,
      branches:   98,
      functions: 98,
      lines:     98,
    },
  },
});
