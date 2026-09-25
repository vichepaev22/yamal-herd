# Вклад в проект

## Локальная разработка
```bash
git clone https://github.com/<USER>/yamal-herd.git
cd yamal-herd
python3 -m http.server 8080     # или: npm install && npm run dev
```

## Правила
1. Вся игра живёт в `index.html` — правьте секции по комментариям-разделителям:
   `CONFIG` · `MODELS` · `AUDIO` · `INPUT` · `ENGINE` · `RENDERER` · `HUD` · `FLOW` · `BOOT`.
2. Баланс выносится в конфиги: `UPGRADE_CONFIG`, `COLLECTIBLE_CONFIG`, `DOG_CONFIG`,
   `MAP_PULSE`, `CHILDMODE_CONFIG`, `minimapConfig`, `QP`, `WEATHER`, `LEVELS`.
3. Перед коммитом обязательно: `make verify`.
4. Не увеличивайте максимум оленей на уровне выше 26 — сложность добавляется
   комбинациями механик (собака, план рейсов, погода, calm, видимость), а не количеством.
5. Новые уровни: сумма `pattern` должна равняться `count`.

## Проверки
```bash
make verify          # статика
make size            # вес
node test/smoke.mjs  # запуск в chromium (нужен playwright)
```
