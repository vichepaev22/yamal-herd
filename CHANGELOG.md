# Changelog

## [4.2.0] - 2026-09-25
### Fixed
- **Критично**: лишняя `}` в `Engine.objective()` преждевременно закрывала класс →
  SyntaxError во всём модуле → игра не запускалась (чёрный экран).
- Загрузка three.js больше не зависит от `importmap` (не поддерживается Safari < 16.4):
  dynamic import с 4 fallback-CDN.
- Добавлены экран загрузки и видимая панель ошибки вместо «тихого» чёрного экрана.
- Собака: ретаргет в `RUN_OUT`, если цель уже собрана игроком; guard от ежескадрового
  повторного `startDogEvent`.
- ESC обрабатывается одним источником (InputController) — раньше дублировался, пауза не работала.
- Touch: чистая dead-zone (14 %) + аналоговая скорость без мёртвого дублирующего кода.

### Added
- Глава II и III: уровни 11–30 (всего tutorial + 30).
- Собака стойбища: FSM (REST/WANDER/WATCH_PLAYER/WARN/RUN_OUT/PLAY_WITH_REINDEER/
  HERD_ASSIST/RETURN_HOME), PLAYFUL → MIXED → HELPER.
- Состояние оленя DISTRACTED + повторный сбор без потерь.
- Delivery patterns и полоса плана рейсов в Objective Panel.
- Погодные фазы внутри уровня (clear → snow → night).
- Погода «fog» (туман) для уровня 19.
- InputController: Keyboard / Touch / Gamepad.
- Плавающий виртуальный джойстик + кнопка БЕГ, safe-area, orientation-hint.
- Adaptive quality (3 шага, cooldown), PWA manifest, иконки.
- Child Mode: Math Card на подбор (`n+1`) и на доставку (`a+b`).
- Радар: импульсная детекция свободных оленей, точка собаки вне стойбища.
- Северные collectibles (морошка/клюква/мешочек/морс) + 4 ветки развития.
- CI: GitHub Pages deploy, verify + build, release-артефакты на теги.

### Verified
- Статический сканер скобок: Engine / сцены / HUD / flow / boot — OK.
- Симуляция ядра: HerdManager без телепортов (≤ 0.57 м/кадр), NaN = 0.
- Инварианты собаки на L11/L17/L24/L26/L30: DELIVERED защищён, ≤ 1 отвлечённый,
  0 выходов за bounds, все уровни завершаются.
- over-delivery не наказуется; анти-softlock `curMin()` работает.
- Математика ввода и радара: 8/8 направлений + стрелка heading.
