# LLM-агенты, модели и маршрутизация EVA-LINE

## Агенты
- **ЕваБот (EvaBot)** — основной ИИ-ассистент сайта evabot.online (бэкенд Node `evabot-brain`, порт 3000). Весь чат, голос, консилиум, работа с базой знаний.
- **Consilium** — мультимодельный движок совещания нескольких моделей (Node-порт в `src/core/ConsiliumEngine.ts`, также Python-порт `backend/app/consilium.py`). Режимы: solo, broadcast, dialogue, consilium. Синтезирует общее решение из ответов нескольких LLM.
- **Антигравити (AntiGravity CLI `agy`)** и **OpenCode / KiloCode** — агентские CLI на виртуальной машине, работают с тем же MCP-набором.
- **CorporateRoles** — ролевая система (eva, adam, dual и корпоративные роли) с KnowledgeBaseConnector для инжекции знаний.

## Единый LLM-клиент
- `UniversalLlmClient` (Node и Python-порт): единая точка вызова моделей с дедлайном попытки 45 с.
- `resolveProvider`: `openrouter/*` → OpenRouter, `*:free` → OpenRouter free, `omni/*` → OmniRoute (LiteLLM), `opencode/*` → OpenCode.
- `model: "auto"` (или `default`) трактуется как «не задано» → берётся модельный роутер (AutoModelRouter / Config.defaultModel), чтобы не зависнуть на мёртвом id.

## Модельный флот и политика (ModelRatings)
- **Gemini (2.x/3.x)**: RESERVED FOR DEVELOPMENT — никогда не используется в рантайм-чате или фолбэке.
- **Trusted fleet (рантайм)**: OpenRouter free-модели и omni/* (Cloudflare Workers). Примеры: `openrouter/free`, `omni/cf-gpt-oss-120b`, nvidia/nemotron-3-super-120b-a12b:free, dots-studio/dots-3-note-preview:free, cohere/north-mini-code:free, inclusionai/ling-3.0-flash-sante:free, poolside/laguna-s-2.1:free, google/gemma-4-31b-it:free.
- Free-квоты сбрасываются по UTC-полуночи; при исчерпании провайдеры отвечают 429 (у сайта были «глюки» 2026-09-08 именно из-за этого).

## База знаний (общая для всех LLM)
- Хранилище: SQLite FTS5 (`knowledge-base/evaline-knowledge-base/fts_index.db`) + in-memory документы + ChromaDB-коллекция `evaline_knowledge` (для векторного поиска).
- Источники: зеркало сайта `evaline-com-ua/site` (языки en/uk/ru/pl/ro/de), репозиторий `/home/evabot/evaline-online/docs` (+ KANBAN, MANIFESTO, релиз-ноуты), пользовательские `/add`-документы.
- Индексация: сборщик `build_knowledge_base.py` (чанки по заголовкам, до 1200 символов), раннетаймовый инжект через `KnowledgeBase.loadEvalineOnline`; идемпотентно по file_path.
- Новые документы: положить .md в `/home/evabot/evaline-online/docs/` (или его подпапки, например company/) — подхватятся при старте evabot-brain автоматически (память + FTS).

## Модели и стоимость
- ModelRegistry (Python) / ModelRatings (Node) считают токены и стоимость по модели.
- OmniRoute (LiteLLM, порт 20128) — свой шлюз для omni/* моделей.