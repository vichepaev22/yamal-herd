# Архитектура

Единый файл `index.html`, разделённый на секции-комментарии.

```
CONFIG        UPGRADE_CONFIG · SENSE_CONFIG · COLLECTIBLE_CONFIG · MAP_PULSE
              CHILDMODE_CONFIG · CALM_STATES · DOG_CONFIG · CHAPTERS · LEVELS · WEATHER · QP
MODELS        fuseParts() — слияние примитивов в одну геометрию с vertex colors
              → 1 draw call на модель. Олень, оленевод, чум, нарты, собака, ягоды, декор.
AUDIO         процедурный WebAudio: ветер (noise+LPF+LFO), дрон, пентатоника,
              шаги, лай, подбор, доставка, победа. Запуск строго по user gesture.
INPUT         InputController ← KeyboardInput / TouchInput / GamepadInput
              на выходе: { moveX, moveY, sprint, pause(edge), restart(edge) }
ENGINE        buildWorld() — seeded-генерация (mulberry32): terrain, obstacles, ice,
              deep snow, decor, deer spawns, collectibles, dog
              update(dt): weather → player → path → herd → free deer → dog →
              collectibles → delivery → calm → particles → tracks → tutorial → win
HERD          path history (шаг 0.22 м) + slotAt(dist) → позиция каждого оленя;
              unsettled-олень догоняет плавно (без телепортов)
DOG           FSM: REST_AT_CAMP · WANDER_AT_CAMP · WATCH_PLAYER · WARN · RUN_OUT ·
              PLAY_WITH_REINDEER · HERD_ASSIST · RETURN_HOME
RENDERER      sky-dome (shader) · aurora (shader) · graded terrain (1 mesh, зоны
              detail→far) · instanced декор · camp · actors · snow (points shader) ·
              trails (instanced) · bursts (instanced) · camera rig
HUD           syncHUD() ~12 Гц · drawMap() ~18 Гц · Objective · MathCard · DogInd
FLOW          screens: menu / chars / upgrade / levels / chapter / howto / settings /
              pause / complete / game
SAVE          localStorage v4 + миграция v1..v3
```

## Ключевые инварианты
- Собака **никогда** не взаимодействует с `DELIVERED`.
- Одновременно отвлечён максимум 1 олень (`maxDistracted`).
- Отвлечённый олень всегда возвращается в игру (DISTRACTED → IDLE у текущей позиции).
- `curMin()` не может превысить число оставшихся оленей → soft-lock невозможен.
- Движение camera-relative: `right = forward × worldUp`, `mapX = dot(pos,right)`,
  `mapY = -dot(pos,forward)` → радар совпадает с экраном.
- NaN-guard у собаки и у всех сущностей; clamp по `lim` у игрока, оленей и собаки.
