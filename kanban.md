# EvaLine Manifesto — Kanban задач

> Все задачи из чата. Приоритеты: P0 (критично) → P2. Статус: pending / in-progress / done / blocked.

---

## P0 — Сокращение до 3 оформлений (по заказу из чата)

- [x] **P0.1** Переключатель тем: оставить ТОЛЬКО 3 кнопки — `raw` (без стилей), `terminal` (идентичен красивому терминалу), `web` (полноценный веб поверх терминального стиля). Убрать `cyber`, `paper`, `neon3d`.
  - [x] 1.1 `nav_and_hero.py` — кнопки: web/terminal/raw
  - [x] 1.2 `footer_and_scripts.py` — setTheme под 3 темы + маппинг legacy localStorage
  - [x] 1.3 `style.css` — удалены блоки `paper` и `neon3d` + `neon3dAurora`/`#neon3d-canvas`
- [x] **P0.2** «web» = полноценный веб ПОВЕРХ терминального стиля: `:root` → терминальная палитра (зелёный фосфор `#00ff88`, тёмно-зелёный фон, `--font-display` → Roboto Mono), аккордеоны/инфографика/ROI/модели сохранены.
- [x] **P0.3** ASCII-арт не нужен в веб-версии: `.hero-ascii` и `.ascii-toggle` скрыты в web (`display:none` + JS `isAsciiAllowed`), показываются только в `terminal`/`raw`; в web — только Mermaid-диаграммы.
- [x] **P0.4** Raw (`без стилей`): чистая семантика подтверждена в w3m/lynx.

## P0 — Проверка и приведение всех вариантов к единому знаменателю

- [x] **P0.5** Проверено через `w3m -dump` и `lynx -dump` raw + index: текст читается, ASCII-логотип/таблицы/кнопки/ссылки корректны.
- [x] **P0.6** Единый знаменатель: web = терминальная палитра + графика (карточки, KPI, Mermaid, ROI), terminal = чистый CRT, raw = чистый HTML.
- [x] **P0.7** Мобильная оптимизация: добавлены media-блоки 768px/480px/360px (toolbar скролл, мелкие кнопки, компактные hero/kpi/model-line, скрытие меток).

## P0 — Регресс-проверка корректности сайта

- [x] **P0.8** Пересборка 675KB; аккордеоны 9/1 открыт, sub-accordion 0/35, ascii-toggle 10, темы 3, JS-синтаксис OK, mermaid CDN (three.js удалён).
- [x] **P0.9** Сервер live: `/` 200, `/manifesto.html` 200, `/api/health` online (78 models).
- [x] **P0.10** Модели: 114 строк (94+20), даты release/lastUpdate на месте (66 блоков), дубликаты топ отсутствуют.

## P1 — Доработки по ходу

- [x] **P1.1** Убран весь 3D-движок (detect3dTier/sync3dLayer/initThreeParticles/initCanvas2d) и `three@CDN`.
- [x] **P1.2** Экспорт/кнопки: ANSI TXT (`/manifesto.txt`) и Markdown (`/MANIFESTO.md`) работают; `MANIFESTO.md` теперь синкается в `public/` компилятором (был 404).
- [x] **P1.3** `manifesto.txt` синкается (public, repo root, pages/) — проверено.
- [x] **P1.4** Локальный сервер отдаёт все артефакты (200): `/`, `/manifesto.html`, `/manifesto.txt`, `/MANIFESTO.md`, `/api/health`. Микро-узел (live) получает через deploy-sync (процесс не запускался).
- [x] **P1.5** Адаптивность схем/визуализаций под портретные смартфоны (mermaid + markmapjs):
  - mindmap (секции 02, 09) → markmapjs (zoom/pan, `d3@7` + `markmap-view@0.18.12` CDN); конвертер `_mindmap_tree()` в `infographics_builder.py` (mermaid mindmap → JSON-дерево), HTML-entities экранирование апострофов в `data-tree`.
  - `renderMarkmaps()` в footer_and_scripts.py: рендер только видимых (offsetParent), повтор на смене языка через `renderVisibleDiagrams()`.
  - Мобильный переворот: `flipHorizontalFlowcharts()` — `flowchart LR → flowchart TD` при innerWidth ≤ 768 (до mermaid.run); верифицировано headless-chromium (viewBox 3185×306 desktop → 1465×854 mobile).
  - Mermaid init: `useMaxWidth` (flowchart/mindmap/sequence/gantt), `wrappingWidth: 140`, `fontSize: 13px`.
  - CSS: `.markmap` 460px (380px ≤480px), touch-action none, подсказка pan/zoom, цвет текста #e6edf3.
  - Фикс пре-существующего бага парсера: edge-label со скобками `(129ms)` → обёрнут в кавычки (инфографика 07).
  - Проверено: headless chromium mobile 390px + desktop — 0 ошибок консоли, markmap 41 нода, JS `node --check` OK, w3m читаем.

## P2 — Мелочи / проверка на проде

- [x] **P2.1** `public/manifesto-*.html` согласованы (все 1 web-кнопка, 114+ model-line, даты).
- [x] **P2.2** Печать (`@media print`) — блок присутствует и попадает в сборку.
- [x] **P2.3** `localStorage` тема: legacy-значения (`neon3d`/`paper`) мапятся на `web` (стр. 89-90 footer_and_scripts.py).

---

## Статусы текущих выполненных ранее задач (не входит в текущий цикл)

- [x] Аккордеоны: все закрыты, кроме problem-statement (helpers.py + секции 01–09) — **done**
- [x] Построчный список 94 моделей + топ-20 + даты release/lastUpdate — **done** (могут потребовать фикса после тем)
- [x] ASCII-логотип figlet `slant` EVALINE — **done** (в terminal/raw)