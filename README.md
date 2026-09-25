<div align="center">

# ЯМАЛ: СОБЕРИ СТАДО
### YAMAL HERD · stylized low-poly 3D arcade

**Найди → собери → приведи → повтори**

Игра про ямальского оленевода: разбредшиеся олени собираются в цепочку-стадо
(механика Snake) и отводятся к стойбищу с чумом.

[![Deploy to GitHub Pages](https://github.com/YOUR-USER/yamal-herd/actions/workflows/deploy.yml/badge.svg)](https://github.com/YOUR-USER/yamal-herd/actions/workflows/deploy.yml)
[![CI](https://github.com/YOUR-USER/yamal-herd/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR-USER/yamal-herd/actions/workflows/ci.yml)
![version](https://img.shields.io/badge/version-4.2.0-8fd6ff)
![license](https://img.shields.io/badge/license-MIT-ffc46b)
![size](https://img.shields.io/badge/single--file-no%20build%20step-7ee6b0)

**Один `index.html`. Без сборки. Без backend. Открывается по ссылке на телефоне.**

</div>

---

## Быстрый старт

```bash
# 1) просто открыть
open index.html                # macOS
xdg-open index.html            # Linux
start index.html               # Windows

# 2) локальный сервер (рекомендуется для теста на телефоне)
python3 -m http.server 8080    # → http://localhost:8080

# 3) через npm
npm install && npm run dev     # → http://localhost:5173
npm run build                  # → dist/
```

> Нужен интернет: three.js 0.160 подгружается с CDN (4 запасных зеркала:
> jsdelivr → unpkg → esm.sh → skypack). Всё остальное — внутри одного файла.

## Живая ссылка

После первого push в `main` GitHub Actions опубликует игру по адресу:

```
https://<USER>.github.io/yamal-herd/
```

Эту ссылку можно отправить в мессенджер — на телефоне игра запустится сразу
(плавающий джойстик + кнопка БЕГ, safe-area, portrait/landscape).

## Управление

| | |
|---|---|
| **Desktop** | `WASD` / стрелки — движение (camera-relative), `SHIFT`/`SPACE` — бег, `ESC` — пауза, `R` — рестарт |
| **Mobile** | плавающий джойстик в правом нижнем секторе (dead zone 14 %, аналоговая скорость) + кнопка **БЕГ** |
| **Gamepad** | стик / крестовина, `A` или `RT` — бег, `Start` — пауза |

Ввод проходит через единый **InputController** — геймплей не знает, клавиатура это или тач.

## Что внутри

**Контент**
- tutorial + **30 уровней**, 3 главы: I «Собери стадо» · II «Жизнь стойбища» · III «Вместе»
- **планы рейсов** (`2 → 3 → 4`, `4 → 5 → 5 → 6` …) + защита от soft-lock при over-delivery
- **4 оленевода** с разными характеристиками и **4 ветки развития** за северные ягоды
- **Child Mode** — арифметика из реального состояния игры: `0+1=1`, `2+1=3`, `4+3=7`

**Механики**
- HerdManager: олени идут по истории пути игрока (без телепортов/дрожи), устойчиво на 26+ оленях
- состояния оленей: IDLE · WANDER · ATTRACTED · FOLLOWING · DELIVERED · LOST · **DISTRACTED**
- **собака стойбища**: FSM из 10 состояний, эволюция PLAYFUL → MIXED → HELPER —
  сначала отвлекает одного оленя, позже подводит 1–2 свободных к игроку
- Calm / Stamina / Sprint / столкновения / мягкая невидимая граница / множитель очков / 3 звезды

**Мир и картинка**
- процедурные low-poly модели (олень, оленевод, чум, нарты, собака, ягоды) — vertex colors, fuse-геометрия
- бесшовная тундра: graded-террейн до ~1.2 км, fog = цвет неба → горизонта не видно
- погода: clear · snow · wind · **fog** · night+aurora · blizzard + **фазовая смена внутри уровня**
- снег-шейдер, северное сияние, следы на снегу, частицы, тёплый свет стойбища

**Инженерия**
- радар с **импульсной детекцией** (Reindeer Detection Pulse), прокачиваемой «Зовом тундры»
- camera-relative movement + корректная ориентация радара (вверх на экране = вверх на радаре)
- mobile web: safe-area, viewport-fit, orientation-hint, touch-targets ≥ 44 px, dpr ≤ 1.5
- **adaptive quality**: 3 шага деградации (dpr → тени → снег/следы) с cooldown
- PWA: manifest, иконки, standalone
- localStorage save **v4 + автоматическая миграция с v1/v2/v3**
- 100 % процедурное аудио (WebAudio): ветер, эмбиент, шаги, лай, подбор, доставка, победа

## Структура репозитория

```
index.html                     ← вся игра: логика, 3D, UI, аудио (единый файл)
manifest.webmanifest           ← PWA
public/icon*.svg|png           ← иконки (сгенерированы, без бинарных зависимостей)
scripts/verify.py              ← статическая верификация сборки
scripts/size-report.sh         ← отчёт о размере
test/smoke.mjs                 ← опциональный Playwright smoke-тест
.github/workflows/deploy.yml   ← автодеплой на GitHub Pages
.github/workflows/ci.yml       ← verify + build на каждый push/PR
.github/workflows/release.yml  ← zip-артефакт на тег vX.Y.Z
docs/                          ← архитектура, уровни, мобильный слой, тестирование, деплой
Makefile · package.json · vite.config.js · vercel.json · netlify.toml · _headers
```

## Проверка сборки

```bash
make verify     # скобки во всех <script>, DOM-id, 31 уровень, суммы deliveryPattern,
                # обязательные системы, PWA/SEO/safe-area, наличие файлов
make size       # вес публикации
make test       # = verify
node test/smoke.mjs   # опционально: реальный запуск в chromium (Playwright)
```

## Деплой

| Площадка | Действие |
|---|---|
| **GitHub Pages** | уже настроено (`deploy.yml`). Settings → Pages → Source: **GitHub Actions** |
| **Vercel** | `vercel` — build command пустой, output `.` |
| **Netlify** | drag&drop папки или `netlify deploy --prod` |
| **Cloudflare Pages** | build: пусто, output: `/` (+ `_headers` подхватится) |
| **Любой статик-хостинг** | достаточно `index.html`, `public/`, `manifest.webmanifest` |

## Дорожная карта

- [ ] полноценный mobile UI redesign (следующая итерация)
- [ ] haptics и дополнительные action-кнопки
- [ ] offline-кэш (Service Worker) — сейчас намеренно отключён, чтобы не мешать обновлениям
- [ ] культурная верификация орнаментов и терминологии с представителями ненецкого сообщества
- [ ] локализация (EN)

## Лицензия

[MIT](LICENSE)

Ненецкая тема использована уважительно и стилизованно: персонажи — нейтральные роли
(«Оленевод», «Следопыт», «Хранитель стада», «Проводник»), орнаменты — обобщённо-северные
геометрические мотивы. Перед коммерческим релизом рекомендуется культурная верификация.
