# Мобильный слой

## Обнаружение устройства
`detectTouch()` = `(pointer: coarse) || (hover: none)` **+** `ontouchstart/maxTouchPoints`
**+** короткая сторона viewport < 900. Не полагается на user-agent.
Результат: класс `body.touch`, переопределяется на `orientationchange`.

## Ввод
`InputController` опрашивает `KeyboardInput`, `TouchInput`, `GamepadInput` и отдаёт
геймплею один нормализованный state. Приоритет: последний источник с ненулевым вектором.
Sprint — логическое ИЛИ всех источников. Pause/restart — детектор фронта (edge).

## Джойстик
- Плавающий: база появляется в точке касания внутри зоны (правый нижний сектор).
- Зона: `width: min(46vw, 320px)`, `height: 44vh`, `touch-action: none`.
- Dead zone 14 %, далее аналоговая нормировка `(m - dead) / (1 - dead)`.
- Направление: `y = -dy` (палец вверх → вверх экрана) → дальше camera-relative.
- `setPointerCapture` + проверка `pointerId` → мультитач не ломает управление.
- Кнопка БЕГ (84×84 px) слева от зоны, отдельные pointer-события.

## HUD
| Элемент | Desktop | Mobile |
|---|---|---|
| Уровень / ветер / dog-toast | top-left | top-left |
| Таймер | top-center | top-center |
| Очки / ягоды | top-right | top-right (под паузой) |
| Objective | bottom-center | **top-center** (ниже таймера) |
| Radar + СТАДО + ДОСТАВЛЕНО + Calm | bottom-right | **поднят выше**, scale .88 |
| Выносливость | bottom-left | bottom-left |
| Джойстик / БЕГ | скрыты | bottom-right |

Все отступы через `calc(... + env(safe-area-inset-*))`. Тач-цели ≥ 44 px.
Portrait не блокируется — мягкая подсказка «поверните телефон» с кнопкой закрытия.

## Производительность
- `devicePixelRatio` ограничен: desktop ≤ 2, mobile ≤ 1.5.
- Пресет по умолчанию на touch: MEDIUM (HIGH понижается автоматически).
- Adaptive quality: замер FPS каждые 2 с, при < 30 fps шаг деградации
  (1: dpr ×0.78 → 2: тени off → 3: снег −55 % и следы off), cooldown 8 с, максимум 3 шага.
- Instancing: декор, лёд, следы, частицы, кольца, лапы/руки персонажей.
- Террейн — один graded-mesh (детальность падает с расстоянием), дальний декор без теней.

## Тестовые размеры
390×844 · 430×932 · 844×390 · 932×430 · 768×1024 · 1024×768.
