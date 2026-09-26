import { defineConfig } from 'vite'

// Игра — один самодостаточный index.html.
// base './' → одинаково работает в корне домена и в подпапке (GitHub Pages /user/repo/).
export default defineConfig({
  base: './',
  publicDir: false,          // public/ копируется как есть (CI делает это для Pages)
  build: {
    outDir: 'dist',
    target: 'es2022',        // top-level await в three.js-лоадере игры требует es2022+
    assetsInlineLimit: 0,
    reportCompressedSize: true
  },
  server: { host: true, port: 5173 }
})
