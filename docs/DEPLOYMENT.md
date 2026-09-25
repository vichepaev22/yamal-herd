# Деплой

## GitHub Pages (настроено по умолчанию)
1. `git push origin main --tags`
2. Settings → Pages → **Source: GitHub Actions**
3. Через 1–2 мин игра доступна на `https://<USER>.github.io/<REPO>/`

Workflow `deploy.yml`: verify → сборка `_site` (index.html, public/, manifest, robots,
sitemap, 404) → upload-pages-artifact → deploy-pages.

## Vercel
```bash
npm i -g vercel && vercel --prod
```
`vercel.json`: build command пустой, output `.` — публикуется как статика.

## Netlify
Drag&drop папки репозитория в app.netlify.com/drop или `netlify deploy --prod`.

## Cloudflare Pages
Build command: *(пусто)* · Output directory: `/` · `_headers` подхватится автоматически.

## Любой статик-хостинг
Достаточно: `index.html`, `public/`, `manifest.webmanifest`. Build-шаг не обязателен.

## Замечания
- `base: './'` в vite.config.js → относительные пути, работает и в подпапке.
- three.js грузится с CDN (4 fallback). Для полностью офлайн-версии скачайте
  `three.module.js` в `public/vendor/` и поправьте список `CDN` в начале модуля.
- Service Worker намеренно не добавлен: кэш ломал бы оперативные обновления.
