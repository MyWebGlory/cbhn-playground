import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  base: '/cbhn-playground/',
  plugins: [
    react(),
    {
      name: 'spa-fallback',
      configureServer(server) {
        server.middlewares.use((req, _res, next) => {
          // Intercept /cbhn-playground/projects/:slug (no file extension) and
          // let Vite serve the SPA index.html so React Router handles the route.
          if (
            req.url &&
            req.url.match(/\/projects\/[^/]+\/?$/) &&
            !req.url.endsWith('.html')
          ) {
            req.url = '/cbhn-playground/'
          }
          next()
        })
      },
    },
  ],
  server: {
    watch: {
      // Also watch static project files in public/ for live reload
      paths: ['public/**'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
