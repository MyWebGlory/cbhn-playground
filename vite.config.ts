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
    {
      name: 'watch-public',
      configureServer(server) {
        // Watch all files under public/ (static project HTML, CSS, images, etc.)
        // and trigger a full-page reload whenever any of them change.
        server.watcher.add(path.resolve(__dirname, 'public'))
        server.watcher.on('change', (file) => {
          if (file.includes(`${path.sep}public${path.sep}`)) {
            server.ws.send({ type: 'full-reload', path: '*' })
          }
        })
      },
    },
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
