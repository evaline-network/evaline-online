# EVA-LINE services, domains, LLM agents & knowledge base (EN summary)

## Web services
- **evabot.online** — main platform + EvaBot chat (SPA: chat, voice, face).
- **evaline.online** — corporate website.
- **evaline.network** — services ecosystem.
- **evaline.com.ua** — product site (mirror in KB: `knowledge-base/evaline-com-ua/site`, langs uk/en/ru/ro/de/pl).
- **business.evaline.online** — business portal (Telemetry & Status) via GCP load balancer; /api proxied to backend.
- **Cloud Run business-tier-api** — separate B2B API with tiers & billing.

## Public sections (evabot.online / face)
- `/face` — Eva 3D face; `/docs` — documentation; `/voice` — voice settings (persona Eva/Adam, autosend, TTS).

## API surface (backend :3000)
- `POST /api/chat`, `/api/chat/stream` — chat (unary / SSE). Params: message, model, history, persona, lang, role, provider, apiKey, useKnowledgeBase, sessionId.
- `POST /api/consilium` — multi-model deliberation (modes: solo, broadcast, dialogue, consilium).
- `POST /api/tts` + `/api/tts/status` — speech synthesis (Cloud TTS, cap 900 000 chars/month, only-free policy; edge-tts fallback: ru→Svetlana/DmitryNeural, uk→Polina/OstapNeural, en→Aria/GuyNeural).
- `POST /api/stt` — speech recognition.
- `/api/kb/search`, `/api/kb/docs` — knowledge base search (SQLite FTS5 + memory).
- `/api/status`, `/api/db`, `/api/config` — diagnostics.

## Cloud Run business tier (B2B)
- Routes: `/health`, `/v1/api-keys`, `/v1/api-keys/{key_id}`, `/v1/billing/checkout`, `/v1/tiers`, `/v1/usage/record`, `/v1/usage/summary`, `/v1/webhooks/stripe`. All `/v1` require an API key (401 MISSING_API_KEY otherwise).
- Tiers: free (10 rpm, burst 20, 10000 daily_tokens, gemini-1.5-flash), starter, pro, enterprise.
- Stripe integration planned (env currently placeholder).

## LLM agents & models
- **EvaBot** — main assistant (Node `evabot-brain`, :3000).
- **Consilium** — multi-model deliberation engine (Node `src/core/ConsiliumEngine.ts`; Python port `backend/app/consilium.py`). Modes: solo, broadcast, dialogue, consilium.
- **AntiGravity CLI `agy`**, **OpenCode**, **KiloCode** — agent CLIs, same 21-server MCP suite.
- **CorporateRoles** — eva/adam/dual + corporate roles, KnowledgeBaseConnector for RAG injection.
- **UniversalLlmClient** — single LLM entry (45 s attempt deadline). `resolveProvider`: `openrouter/*`/`*:free` → OpenRouter, `omni/*` → OmniRoute, `opencode/*` → OpenCode. `model: "auto"`/`default` → treated as unset (AutoModelRouter/Config.defaultModel).
- **ModelRatings policy**: Gemini (2.x/3.x) RESERVED FOR DEVELOPMENT, never used at runtime chat/fallback. Runtime trusted fleet = OpenRouter free + omni/* (e.g. openrouter/free, omni/cf-gpt-oss-120b, nvidia/nemotron-3-super-120b-a12b:free, dots-3-note-preview:free, cohere/north-mini-code:free, ling-3.0-flash-sante:free, poolside/laguna-s-2.1:free, google/gemma-4-31b-it:free). Free quotas reset at UTC midnight; exhaustion → 429 (site was glitchy on 2026-09-08 exactly because of this).

## Knowledge base (shared by all LLMs)
- Stores: SQLite FTS5 (`knowledge-base/evaline-knowledge-base/fts_index.db`) + in-memory documents + ChromaDB `evaline_knowledge`.
- Sources: site mirror `evaline-com-ua/site` (6 langs), repo `/home/evabot/evaline-online/docs` (+ KANBAN, MANIFESTO, release notes), user `/add` docs.
- Builder: `build_knowledge_base.py` (header-based chunks ≤1200 chars); runtime inject via `KnowledgeBase.loadEvalineOnline`; idempotent by file_path.
- New docs: drop .md into `/home/evabot/evaline-online/docs/` (e.g. company/) — auto-loaded on evabot-brain restart (memory + FTS).

## Company facts
- ТОВ «ЕВА-ЛАЙН» (EVA-LINE), ЄДРПОУ 40484497, m. Chornomorsk, Odesa oblast, Ukraine.
- Business: production & sale of EVA foam (ethylene-vinyl acetate, closed-cell). 23 SKUs. Capital 16 000 000 UAH.
- EVA properties: 4–5x lighter than rubber, elasticity/ammortization, "shape memory", -50..+75 °C, CE/REACH, hygienic.
- KB scale claim: 1688 documents; company dossier `knowledge-base/evaline-company-dossier.md`.